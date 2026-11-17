"""
Duka Electronics Data Quality and Cleaning Pipeline
Author: George Tipango
Track: Track A - Retail and E-commerce Performance Analysis
Module: src/cleaning.py

Implements a reusable six-dimension data quality audit, cleaning,
pseudonymization (Section 4.13 KDPA/GDPR compliance), and SQLite export.
"""

import os
import re
import hashlib
import sqlite3
import numpy as np
import pandas as pd


def hash_identifier(identifier: str, salt: str = "Duka2026SecureSalt") -> str:
    """Generate salted SHA-256 pseudonymized hash for customer identifiers."""
    if pd.isna(identifier):
        return "ANON_UNKNOWN"
    raw_str = f"{salt}_{str(identifier).strip()}"
    return "CUST_HASH_" + hashlib.sha256(raw_str.encode("utf-8")).hexdigest()[:12].upper()


def mask_phone(phone_val: str) -> str:
    """Mask phone numbers to preserve routing code while protecting identity."""
    if pd.isna(phone_val) or not str(phone_val).strip() or str(phone_val).strip().lower() == "nan":
        return "UNKNOWN"
    s = str(phone_val).strip()
    if len(s) >= 9:
        prefix = s[:6]
        suffix = s[-3:]
        return f"{prefix}XXX{suffix}"
    return "MASKED_PHONE"


def mask_email(email_val: str) -> str:
    """Mask email preserving provider domain while redacting local identifier."""
    if pd.isna(email_val) or "@" not in str(email_val):
        return "unknown@domain.local"
    parts = str(email_val).strip().split("@")
    user, domain = parts[0], parts[1]
    if len(user) <= 2:
        masked_user = user[0] + "***"
    else:
        masked_user = user[0] + "***" + user[-1]
    return f"{masked_user}@{domain}"


def clean_duka_data(data_dir: str = "data", db_path: str = "database/duka_sales.db"):
    """
    Execute end-to-end data auditing, cleaning, privacy transformations,
    and SQLite ingestion for Duka Electronics sales data.

    Returns:
        dict: Clean DataFrames ('stores', 'products', 'customers', 'orders', 'order_items')
              and 'cleaning_log' containing audit audit records.
    """
    log_records = []
    step_num = 1

    def add_log(dimension, table, column, issue, action, rows_affected):
        nonlocal step_num
        log_records.append({
            "step": step_num,
            "dimension": dimension,
            "table": table,
            "column": column,
            "issue_description": issue,
            "action_taken": action,
            "rows_affected": int(rows_affected)
        })
        step_num += 1

    # 1. Load Raw CSV Data
    stores_path = os.path.join(data_dir, "raw_stores.csv")
    products_path = os.path.join(data_dir, "raw_products.csv")
    customers_path = os.path.join(data_dir, "raw_customers.csv")
    orders_path = os.path.join(data_dir, "raw_orders.csv")
    order_items_path = os.path.join(data_dir, "raw_order_items.csv")

    df_stores = pd.read_csv(stores_path)
    df_products = pd.read_csv(products_path)
    df_customers = pd.read_csv(customers_path)
    df_orders = pd.read_csv(orders_path)
    df_order_items = pd.read_csv(order_items_path)

    # ----------------------------------------------------
    # Dimension 1: UNIQUENESS (Deduplication)
    # ----------------------------------------------------
    # Customer duplicates
    cust_dup_count = df_customers.duplicated(subset=["customer_id"]).sum()
    if cust_dup_count > 0:
        df_customers = df_customers.drop_duplicates(subset=["customer_id"], keep="first").reset_index(drop=True)
    add_log("Uniqueness", "customers", "customer_id",
            f"Found {cust_dup_count} duplicate customer records",
            "Removed duplicate rows, retaining first appearance", cust_dup_count)

    # Order duplicates
    order_dup_count = df_orders.duplicated(subset=["order_id"]).sum()
    if order_dup_count > 0:
        df_orders = df_orders.drop_duplicates(subset=["order_id"], keep="first").reset_index(drop=True)
    add_log("Uniqueness", "orders", "order_id",
            f"Found {order_dup_count} duplicate order header records",
            "Deduplicated order headers based on unique order_id", order_dup_count)

    # Order item duplicates
    item_dup_count = df_order_items.duplicated(subset=["order_item_id"]).sum()
    if item_dup_count > 0:
        df_order_items = df_order_items.drop_duplicates(subset=["order_item_id"], keep="first").reset_index(drop=True)
    add_log("Uniqueness", "order_items", "order_item_id",
            f"Found {item_dup_count} duplicate order line item records",
            "Deduplicated line items", item_dup_count)

    # ----------------------------------------------------
    # Dimension 2: COMPLETENESS (Missing Value Imputation)
    # ----------------------------------------------------
    # Missing phone in customers
    null_phone = df_customers["phone"].isna().sum()
    df_customers["phone"] = df_customers["phone"].fillna("UNKNOWN")
    add_log("Completeness", "customers", "phone",
            f"{null_phone} missing customer phone numbers",
            "Imputed null phone records with 'UNKNOWN'", null_phone)

    # Missing county in customers
    null_county = df_customers["county"].isna().sum()
    df_customers["county"] = df_customers["county"].fillna("Nairobi")  # modal imputation
    add_log("Completeness", "customers", "county",
            f"{null_county} missing customer county locations",
            "Imputed missing counties with dominant mode 'Nairobi'", null_county)

    # Missing discount_pct in orders
    null_disc = df_orders["discount_pct"].isna().sum()
    df_orders["discount_pct"] = df_orders["discount_pct"].fillna(0.0)
    add_log("Completeness", "orders", "discount_pct",
            f"{null_disc} null promotional discount percentages",
            "Imputed null discounts with standard 0.00 (no discount)", null_disc)

    # ----------------------------------------------------
    # Dimension 3: CONSISTENCY (Standardization & Casing)
    # ----------------------------------------------------
    # Inconsistent payment methods in orders
    def normalize_payment(pm):
        if pd.isna(pm):
            return "M-Pesa"
        val = str(pm).strip().lower().replace("_", "-")
        if "mpesa" in val or "m-pesa" in val:
            return "M-Pesa"
        elif "card" in val:
            return "Credit Card"
        elif "bank" in val or "transfer" in val:
            return "Bank Transfer"
        elif "cash" in val:
            return "Cash"
        return "M-Pesa"

    orig_pms = df_orders["payment_method"].copy()
    df_orders["payment_method"] = df_orders["payment_method"].apply(normalize_payment)
    inconsistent_pm_count = (orig_pms != df_orders["payment_method"]).sum()
    add_log("Consistency", "orders", "payment_method",
            f"{inconsistent_pm_count} inconsistently cased or formatted payment methods",
            "Standardized to canonical set: ['M-Pesa', 'Credit Card', 'Bank Transfer', 'Cash']",
            inconsistent_pm_count)

    # Store channel formatting
    df_stores["channel"] = df_stores["channel"].astype(str).str.title().replace({
        "Retail_Store": "Retail Store",
        "Retail Store": "Retail Store",
        "E-Commerce": "E-Commerce"
    })
    add_log("Consistency", "stores", "channel",
            "Inconsistent casing in channel names",
            "Standardized string format to Title Case", len(df_stores))

    # ----------------------------------------------------
    # Dimension 4: TIMELINESS (Scope Boundary Validation)
    # ----------------------------------------------------
    # Convert order_date to datetime and filter for H1 2026 (2026-01-01 to 2026-06-30)
    df_orders["order_date"] = pd.to_datetime(df_orders["order_date"], errors="coerce")
    min_date = pd.Timestamp("2026-01-01")
    max_date = pd.Timestamp("2026-06-30")
    
    out_of_bounds = (~df_orders["order_date"].between(min_date, max_date)) | df_orders["order_date"].isna()
    out_of_bounds_count = out_of_bounds.sum()
    df_orders = df_orders[~out_of_bounds].copy().reset_index(drop=True)
    add_log("Timeliness", "orders", "order_date",
            f"{out_of_bounds_count} orders outside analytical H1 2026 window (future or historical anomalies)",
            "Filtered out records outside 2026-01-01 to 2026-06-30", out_of_bounds_count)

    # Format date back to ISO string for SQLite
    df_orders["order_date"] = df_orders["order_date"].dt.strftime("%Y-%m-%d")

    # ----------------------------------------------------
    # Dimension 5: VALIDITY (Business Rule Constraints)
    # ----------------------------------------------------
    # Negative quantity in order items
    invalid_qty_count = (df_order_items["quantity"] <= 0).sum()
    df_order_items = df_order_items[df_order_items["quantity"] > 0].copy().reset_index(drop=True)
    add_log("Validity", "order_items", "quantity",
            f"{invalid_qty_count} line items with invalid non-positive quantity (<= 0)",
            "Purged invalid negative/zero quantity transaction records", invalid_qty_count)

    # Unrealistic discounts (> 50%)
    invalid_disc = (df_orders["discount_pct"] > 0.50) | (df_orders["discount_pct"] < 0.0)
    invalid_disc_count = invalid_disc.sum()
    df_orders.loc[invalid_disc, "discount_pct"] = 0.00
    add_log("Validity", "orders", "discount_pct",
            f"{invalid_disc_count} orders with invalid discount percentages (>50% or <0%)",
            "Reset invalid promotional discount values to standard 0.00", invalid_disc_count)

    # Referential integrity: Keep order_items only for existing valid orders
    valid_order_ids = set(df_orders["order_id"])
    orphaned_items = ~df_order_items["order_id"].isin(valid_order_ids)
    orphaned_count = orphaned_items.sum()
    df_order_items = df_order_items[~orphaned_items].copy().reset_index(drop=True)
    add_log("Validity", "order_items", "order_id",
            f"{orphaned_count} orphaned line items referencing deleted or invalid orders",
            "Enforced foreign key referential integrity; dropped orphaned items", orphaned_count)

    # ----------------------------------------------------
    # Dimension 6: ACCURACY (Reconciliation of Metrics)
    # ----------------------------------------------------
    # Join with products to verify pricing and reconcile totals
    prod_map = df_products.set_index("product_id")[["unit_cost_kes", "unit_price_kes"]].to_dict(orient="index")
    order_disc_map = df_orders.set_index("order_id")["discount_pct"].to_dict()

    df_order_items["unit_price_kes"] = df_order_items["product_id"].map(lambda pid: prod_map[pid]["unit_price_kes"])
    df_order_items["unit_cost_kes"] = df_order_items["product_id"].map(lambda pid: prod_map[pid]["unit_cost_kes"])
    df_order_items["discount_pct"] = df_order_items["order_id"].map(lambda oid: order_disc_map.get(oid, 0.0))

    # Accurate line total and line profit formulas
    df_order_items["line_gross_kes"] = df_order_items["quantity"] * df_order_items["unit_price_kes"]
    df_order_items["line_discount_kes"] = df_order_items["line_gross_kes"] * df_order_items["discount_pct"]
    df_order_items["line_total_kes"] = np.round(df_order_items["line_gross_kes"] - df_order_items["line_discount_kes"], 2)
    df_order_items["line_cost_kes"] = df_order_items["quantity"] * df_order_items["unit_cost_kes"]
    df_order_items["profit_kes"] = np.round(df_order_items["line_total_kes"] - df_order_items["line_cost_kes"], 2)

    # Reconcile orders header totals from line items
    item_sums = df_order_items.groupby("order_id").agg(
        calc_total=("line_total_kes", "sum"),
        calc_profit=("profit_kes", "sum"),
        items_count=("quantity", "sum")
    ).reset_index()

    df_orders = df_orders.merge(item_sums, on="order_id", how="inner")
    reconciliation_mismatches = (df_orders["order_total_kes"] != df_orders["calc_total"]).sum()
    df_orders["order_total_kes"] = np.round(df_orders["calc_total"], 2)
    df_orders["order_profit_kes"] = np.round(df_orders["calc_profit"], 2)
    df_orders = df_orders.drop(columns=["calc_total", "calc_profit"])

    add_log("Accuracy", "orders", "order_total_kes",
            f"{reconciliation_mismatches} orders with header-to-line total discrepancy",
            "Recalculated and reconciled header totals directly from audited line items",
            reconciliation_mismatches)

    # ----------------------------------------------------
    # Privacy & Pseudonymization (Section 4.13 KDPA / GDPR)
    # ----------------------------------------------------
    # Apply pseudonymization hash to customer identifier
    df_customers["pseudo_customer_id"] = df_customers["customer_id"].apply(hash_identifier)
    cust_id_to_pseudo = df_customers.set_index("customer_id")["pseudo_customer_id"].to_dict()
    df_orders["pseudo_customer_id"] = df_orders["customer_id"].map(cust_id_to_pseudo)

    # Mask phone and email
    df_customers["phone_masked"] = df_customers["phone"].apply(mask_phone)
    df_customers["email_masked"] = df_customers["email"].apply(mask_email)

    # Create analytical customer table without direct PII
    df_customers_clean = df_customers[[
        "pseudo_customer_id", "county", "signup_date", "initial_tier",
        "phone_masked", "email_masked"
    ]].copy()

    add_log("Privacy/Compliance", "customers", "customer_name, email, phone",
            "Plaintext PII presents compliance risk under Section 4.13 KDPA 2019",
            "Irreversibly hashed customer_id into pseudo_customer_id; masked email/phone; purged raw names",
            len(df_customers))

    # Reorder and finalize tables
    df_orders_clean = df_orders[[
        "order_id", "pseudo_customer_id", "store_id", "order_date",
        "payment_method", "order_status", "discount_pct", "items_count",
        "order_total_kes", "order_profit_kes"
    ]].copy()

    df_order_items_clean = df_order_items[[
        "order_item_id", "order_id", "product_id", "quantity",
        "unit_price_kes", "unit_cost_kes", "discount_pct",
        "line_total_kes", "profit_kes"
    ]].copy()

    df_products_clean = df_products.copy()
    df_stores_clean = df_stores.copy()

    df_cleaning_log = pd.DataFrame(log_records)

    # ----------------------------------------------------
    # SQLite Export
    # ----------------------------------------------------
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    
    df_stores_clean.to_sql("dim_stores", conn, if_exists="replace", index=False)
    df_products_clean.to_sql("dim_products", conn, if_exists="replace", index=False)
    df_customers_clean.to_sql("dim_customers", conn, if_exists="replace", index=False)
    df_orders_clean.to_sql("fct_orders", conn, if_exists="replace", index=False)
    df_order_items_clean.to_sql("fct_order_items", conn, if_exists="replace", index=False)
    df_cleaning_log.to_sql("log_cleaning_audit", conn, if_exists="replace", index=False)
    
    conn.close()

    return {
        "stores": df_stores_clean,
        "products": df_products_clean,
        "customers": df_customers_clean,
        "orders": df_orders_clean,
        "order_items": df_order_items_clean,
        "cleaning_log": df_cleaning_log
    }


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    db_path = os.path.join(base_dir, "database", "duka_sales.db")
    
    result = clean_duka_data(data_dir=data_dir, db_path=db_path)
    print("=== Duka Cleaning Pipeline Executed Successfully ===")
    print(f"Database saved to: {db_path}")
    print("\nCleaning Log Summary:")
    print(result["cleaning_log"][["dimension", "table", "action_taken", "rows_affected"]])

