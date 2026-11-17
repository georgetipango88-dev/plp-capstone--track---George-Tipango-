"""
Data Generator for Duka Electronics Kenya Ltd. (H1 2026 Capstone Project)
Track A: Retail and E-commerce Performance Analysis
Author: George Tipango
Date: November 2026
"""

import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Set seeds for 100% reproducibility
np.random.seed(42)
random.seed(42)

def generate_duka_dataset(output_dir="data"):
    os.makedirs(output_dir, exist_ok=True)
    
    # ----------------------------------------------------
    # 1. Stores / Branches
    # ----------------------------------------------------
    stores_data = [
        {"store_id": "STR-001", "store_name": "Nairobi CBD Flagship", "county": "Nairobi", "region": "Nairobi", "channel": "Retail Store", "square_meters": 450},
        {"store_id": "STR-002", "store_name": "Nairobi Westlands Hub", "county": "Nairobi", "region": "Nairobi", "channel": "Retail Store", "square_meters": 320},
        {"store_id": "STR-003", "store_name": "Mombasa Old Port Mall", "county": "Mombasa", "region": "Coast", "channel": "Retail Store", "square_meters": 280},
        {"store_id": "STR-004", "store_name": "Kisumu Mega Plaza", "county": "Kisumu", "region": "Western", "channel": "Retail Store", "square_meters": 220},
        {"store_id": "STR-005", "store_name": "Nakuru Rift Hub", "county": "Nakuru", "region": "Rift Valley", "channel": "Retail Store", "square_meters": 190},
        {"store_id": "STR-006", "store_name": "Eldoret Highland Mall", "county": "Uasin Gishu", "region": "Rift Valley", "channel": "Retail Store", "square_meters": 210},
        {"store_id": "STR-007", "store_name": "Duka E-Commerce Portal", "county": "Nairobi", "region": "Online", "channel": "E-Commerce", "square_meters": 0},
    ]
    df_stores = pd.DataFrame(stores_data)
    
    # ----------------------------------------------------
    # 2. Products Catalog
    # ----------------------------------------------------
    products_data = [
        {"product_id": "PRD-101", "product_name": "HP Pavilion 15 Core i5 16GB", "category": "Laptops & Computing", "unit_cost_kes": 68000, "unit_price_kes": 85000},
        {"product_id": "PRD-102", "product_name": "Dell Latitude 5420 Core i7", "category": "Laptops & Computing", "unit_cost_kes": 84000, "unit_price_kes": 105000},
        {"product_id": "PRD-103", "product_name": "MacBook Air M2 256GB", "category": "Laptops & Computing", "unit_cost_kes": 125000, "unit_price_kes": 155000},
        {"product_id": "PRD-104", "product_name": "Lenovo IdeaPad Slim 3", "category": "Laptops & Computing", "unit_cost_kes": 42000, "unit_price_kes": 52000},
        {"product_id": "PRD-105", "product_name": "Asus TUF Gaming A15", "category": "Laptops & Computing", "unit_cost_kes": 110000, "unit_price_kes": 138000},
        
        {"product_id": "PRD-201", "product_name": "Samsung Galaxy S24 Ultra", "category": "Smartphones & Tablets", "unit_cost_kes": 130000, "unit_price_kes": 160000},
        {"product_id": "PRD-202", "product_name": "iPhone 15 Pro 128GB", "category": "Smartphones & Tablets", "unit_cost_kes": 142000, "unit_price_kes": 175000},
        {"product_id": "PRD-203", "product_name": "Redmi Note 13 Pro 256GB", "category": "Smartphones & Tablets", "unit_cost_kes": 26000, "unit_price_kes": 34000},
        {"product_id": "PRD-204", "product_name": "Samsung Galaxy A54 5G", "category": "Smartphones & Tablets", "unit_cost_kes": 35000, "unit_price_kes": 44000},
        {"product_id": "PRD-205", "product_name": "iPad 10th Gen 64GB WiFi", "category": "Smartphones & Tablets", "unit_cost_kes": 48000, "unit_price_kes": 60000},
        
        {"product_id": "PRD-301", "product_name": "Sony WH-1000XM5 ANC Headphones", "category": "Audio & Wearables", "unit_cost_kes": 32000, "unit_price_kes": 42000},
        {"product_id": "PRD-302", "product_name": "JBL Flip 6 Bluetooth Speaker", "category": "Audio & Wearables", "unit_cost_kes": 11000, "unit_price_kes": 15500},
        {"product_id": "PRD-303", "product_name": "Apple AirPods Pro 2nd Gen", "category": "Audio & Wearables", "unit_cost_kes": 26000, "unit_price_kes": 33000},
        {"product_id": "PRD-304", "product_name": "Samsung Galaxy Watch 6", "category": "Audio & Wearables", "unit_cost_kes": 22000, "unit_price_kes": 29000},
        {"product_id": "PRD-305", "product_name": "Oraimo FreePods 4 ANC", "category": "Audio & Wearables", "unit_cost_kes": 3200, "unit_price_kes": 4800},
        
        {"product_id": "PRD-401", "product_name": "LG 55 Inch 4K UHD Smart TV", "category": "Home Entertainment", "unit_cost_kes": 55000, "unit_price_kes": 72000},
        {"product_id": "PRD-402", "product_name": "Samsung 65 Inch QLED 4K TV", "category": "Home Entertainment", "unit_cost_kes": 98000, "unit_price_kes": 128000},
        {"product_id": "PRD-403", "product_name": "Hisense 43 Inch FHD Smart TV", "category": "Home Entertainment", "unit_cost_kes": 24000, "unit_price_kes": 32000},
        {"product_id": "PRD-404", "product_name": "Sony HT-S20R 5.1ch Soundbar", "category": "Home Entertainment", "unit_cost_kes": 21000, "unit_price_kes": 28000},
        {"product_id": "PRD-405", "product_name": "PlayStation 5 Slim Console", "category": "Home Entertainment", "unit_cost_kes": 64000, "unit_price_kes": 79000},
        
        {"product_id": "PRD-501", "product_name": "Logitech MX Master 3S Mouse", "category": "Accessories & Peripherals", "unit_cost_kes": 9500, "unit_price_kes": 13500},
        {"product_id": "PRD-502", "product_name": "SanDisk Extreme 1TB NVMe SSD", "category": "Accessories & Peripherals", "unit_cost_kes": 11500, "unit_price_kes": 16000},
        {"product_id": "PRD-503", "product_name": "Anker 65W GaN Fast Charger", "category": "Accessories & Peripherals", "unit_cost_kes": 3800, "unit_price_kes": 5500},
        {"product_id": "PRD-504", "product_name": "Dell 24 Inch IPS FHD Monitor", "category": "Accessories & Peripherals", "unit_cost_kes": 16000, "unit_price_kes": 22000},
        {"product_id": "PRD-505", "product_name": "TP-Link Deco S7 Mesh WiFi 3-Pack", "category": "Accessories & Peripherals", "unit_cost_kes": 14000, "unit_price_kes": 19500},
    ]
    df_products = pd.DataFrame(products_data)
    
    # ----------------------------------------------------
    # 3. Customers
    # ----------------------------------------------------
    first_names = [
        "Kevin", "Faith", "Brian", "Cynthia", "Emmanuel", "Mercy", "John", "Grace",
        "Dennis", "Sharon", "Peter", "Joyce", "Samuel", "Esther", "David", "Beatrice",
        "Victor", "Mary", "George", "Lilian", "James", "Sarah", "Paul", "Eunice",
        "Joseph", "Alice", "Daniel", "Jane", "Anthony", "Jackline", "Moses", "Winnie",
        "Stephen", "Gladys", "Patrick", "Caroline", "Evans", "Brenda", "Collins", "Rose"
    ]
    last_names = [
        "Ochieng", "Mwangi", "Kiprono", "Wanjiku", "Mutua", "Kamau", "Otieno", "Njoroge",
        "Kariuki", "Chebet", "Odhiambo", "Maina", "Koech", "Karanja", "Ndung'u", "Wambui",
        "Rotich", "Kimani", "Achieng", "Muthoni", "Barasa", "Wafula", "Ouma", "Cheruiyot",
        "Githinji", "Nyambura", "Kipkorir", "Mueni", "Makori", "Mogaka", "Lagat", "Kilonzo"
    ]
    counties_weights = {
        "Nairobi": 0.42, "Kiambu": 0.14, "Mombasa": 0.11, "Nakuru": 0.09,
        "Uasin Gishu": 0.08, "Kisumu": 0.07, "Machakos": 0.05, "Kajiado": 0.04
    }
    
    num_customers = 2800
    customers = []
    
    start_signup = datetime(2024, 1, 1)
    end_signup = datetime(2026, 6, 1)
    signup_span = (end_signup - start_signup).days
    
    for i in range(1, num_customers + 1):
        c_id = f"CUST-{i:05d}"
        fn = random.choice(first_names)
        ln = random.choice(last_names)
        name = f"{fn} {ln}"
        county = np.random.choice(list(counties_weights.keys()), p=list(counties_weights.values()))
        domain = random.choice(["gmail.com", "yahoo.com", "outlook.com", "icloud.com", "africaonline.co.ke"])
        clean_ln = ln.lower().replace("'", "")
        email = f"{fn.lower()}.{clean_ln}{random.randint(10, 999)}@{domain}"
        prefix = random.choice(["+25470", "+25471", "+25472", "+25479", "+25411"])
        phone = f"{prefix}{random.randint(100000, 999999)}"
        signup_date = (start_signup + timedelta(days=random.randint(0, signup_span))).strftime("%Y-%m-%d")
        
        # Segment tier at onboarding
        initial_tier = np.random.choice(["Standard", "Silver", "Gold", "Corporate VIP"], p=[0.60, 0.22, 0.13, 0.05])
        
        customers.append({
            "customer_id": c_id,
            "customer_name": name,
            "email": email,
            "phone": phone,
            "county": county,
            "signup_date": signup_date,
            "initial_tier": initial_tier
        })
        
    df_customers = pd.DataFrame(customers)
    
    # ----------------------------------------------------
    # 4. Orders & Order Items (Jan 1, 2026 to Jun 30, 2026)
    # ----------------------------------------------------
    # Store sales weights reflecting business reality:
    # Nairobi CBD (36%), Westlands (18%), Mombasa (12%), Kisumu (9%), Nakuru (8%), Eldoret (9% overall, surging in Q2), Online (8%)
    store_ids = df_stores["store_id"].tolist()
    
    # Q1 vs Q2 trend parameters:
    # Eldoret: grew +50% in Q2 vs Q1
    # Mombasa & Nakuru: dropped ~25% in Q2 vs Q1
    # Nairobi: steady leader
    
    start_date = datetime(2026, 1, 1)
    end_date = datetime(2026, 6, 30)
    total_days = (end_date - start_date).days + 1
    
    order_id_counter = 10001
    item_id_counter = 50001
    
    orders = []
    order_items = []
    
    # Products lookup
    prod_lookup = {r["product_id"]: r for r in products_data}
    
    # Generate ~9,500 orders
    target_orders = 9400
    
    for _ in range(target_orders):
        order_day_offset = random.randint(0, total_days - 1)
        curr_date = start_date + timedelta(days=order_day_offset)
        curr_quarter = 1 if curr_date.month <= 3 else 2
        date_str = curr_date.strftime("%Y-%m-%d")
        
        # Adjust store probabilities based on quarter
        if curr_quarter == 1:
            p_stores = [0.35, 0.18, 0.14, 0.09, 0.10, 0.06, 0.08]
        else:
            # Q2: Eldoret (+50% relative growth), Mombasa and Nakuru drop ~25%
            p_stores = [0.36, 0.19, 0.10, 0.09, 0.07, 0.11, 0.08]
            
        store_id = np.random.choice(store_ids, p=p_stores)
        cust_id = random.choice(df_customers["customer_id"].tolist())
        
        # Payment method
        payment_method = np.random.choice(
            ["M-Pesa", "Credit Card", "Bank Transfer", "Cash"],
            p=[0.67, 0.18, 0.10, 0.05]
        )
        
        # Order status: 95% Completed, 3% Returned, 2% Cancelled
        status = np.random.choice(["Completed", "Returned", "Cancelled"], p=[0.95, 0.03, 0.02])
        
        # Promotional discount: 0% (65%), 5% (15%), 10% (12%), 15% (5%), 20% (3%)
        discount_pct = np.random.choice([0.00, 0.05, 0.10, 0.15, 0.20], p=[0.65, 0.15, 0.12, 0.05, 0.03])
        
        order_id = f"ORD-{order_id_counter}"
        order_id_counter += 1
        
        # Number of line items: 1 to 4 items per order
        num_items = np.random.choice([1, 2, 3, 4], p=[0.60, 0.25, 0.11, 0.04])
        
        # Product selection weighting:
        # Laptops represent ~22% of line items but ~58% of revenue
        prod_weights = []
        for p in products_data:
            if p["category"] == "Laptops & Computing":
                prod_weights.append(0.24 / 5) # 24% total for laptops
            elif p["category"] == "Smartphones & Tablets":
                prod_weights.append(0.30 / 5) # 30% for phones
            elif p["category"] == "Accessories & Peripherals":
                prod_weights.append(0.26 / 5) # 26% for accessories
            elif p["category"] == "Audio & Wearables":
                prod_weights.append(0.12 / 5) # 12% for audio
            else:
                prod_weights.append(0.08 / 5) # 8% for TV/consoles
                
        chosen_prods = np.random.choice(products_data, size=num_items, replace=False, p=prod_weights)
        
        order_subtotal = 0
        order_profit = 0
        
        for p in chosen_prods:
            item_id = f"ITM-{item_id_counter}"
            item_id_counter += 1
            
            p_id = p["product_id"]
            u_cost = p["unit_cost_kes"]
            u_price = p["unit_price_kes"]
            
            # Quantity: mostly 1, occasionally 2 or 3 (accessories)
            if p["category"] in ["Accessories & Peripherals", "Audio & Wearables"]:
                qty = np.random.choice([1, 2, 3], p=[0.70, 0.22, 0.08])
            else:
                qty = np.random.choice([1, 2], p=[0.92, 0.08])
                
            line_gross = qty * u_price
            line_discount = line_gross * discount_pct
            line_net = line_gross - line_discount
            line_cost = qty * u_cost
            line_profit = line_net - line_cost
            
            order_subtotal += line_net
            order_profit += line_profit
            
            order_items.append({
                "order_item_id": item_id,
                "order_id": order_id,
                "product_id": p_id,
                "quantity": qty,
                "unit_price_kes": u_price,
                "unit_cost_kes": u_cost,
                "discount_pct": discount_pct,
                "line_total_kes": round(line_net, 2),
                "profit_kes": round(line_profit, 2)
            })
            
        orders.append({
            "order_id": order_id,
            "customer_id": cust_id,
            "store_id": store_id,
            "order_date": date_str,
            "payment_method": payment_method,
            "order_status": status,
            "discount_pct": discount_pct,
            "order_total_kes": round(order_subtotal, 2),
            "order_profit_kes": round(order_profit, 2)
        })
        
    df_orders = pd.DataFrame(orders)
    df_order_items = pd.DataFrame(order_items)
    
    # ----------------------------------------------------
    # 5. Inject Controlled Data Quality Anomalies (for Audit)
    # ----------------------------------------------------
    # A. Duplicates (Uniqueness dimension)
    dup_custs = df_customers.sample(n=25, random_state=42)
    df_customers_raw = pd.concat([df_customers, dup_custs], ignore_index=True)
    
    dup_orders = df_orders.sample(n=35, random_state=42)
    df_orders_raw = pd.concat([df_orders, dup_orders], ignore_index=True)
    
    # B. Missing values (Completeness dimension)
    df_customers_raw.loc[df_customers_raw.sample(n=60, random_state=10).index, "phone"] = np.nan
    df_customers_raw.loc[df_customers_raw.sample(n=30, random_state=11).index, "county"] = np.nan
    df_orders_raw.loc[df_orders_raw.sample(n=45, random_state=12).index, "discount_pct"] = np.nan
    
    # C. Casing / Inconsistency (Consistency dimension)
    pm_inconsistent = df_orders_raw["payment_method"].copy()
    idx_mpesa = pm_inconsistent[pm_inconsistent == "M-Pesa"].sample(n=150, random_state=13).index
    pm_inconsistent.loc[idx_mpesa] = np.random.choice(["mpesa", "M_PESA", "M-pesa"], size=len(idx_mpesa))
    idx_card = pm_inconsistent[pm_inconsistent == "Credit Card"].sample(n=80, random_state=14).index
    pm_inconsistent.loc[idx_card] = np.random.choice(["card", "CARD", "credit_card"], size=len(idx_card))
    df_orders_raw["payment_method"] = pm_inconsistent
    
    # Store name inconsistency
    df_stores_raw = df_stores.copy()
    df_stores_raw.loc[0, "channel"] = "retail_store"
    df_stores_raw.loc[1, "channel"] = "RETAIL STORE"
    
    # D. Timeliness & Out of Range Dates (Timeliness dimension)
    idx_future = df_orders_raw.sample(n=12, random_state=15).index
    df_orders_raw.loc[idx_future, "order_date"] = "2027-12-31" # Future date anomaly
    
    idx_old = df_orders_raw.sample(n=8, random_state=16).index
    df_orders_raw.loc[idx_old, "order_date"] = "2021-05-15" # Pre-historical anomaly
    
    # E. Invalid Values (Validity dimension)
    df_order_items_raw = df_order_items.copy()
    idx_neg_qty = df_order_items_raw.sample(n=10, random_state=17).index
    df_order_items_raw.loc[idx_neg_qty, "quantity"] = -1 # Typo negative quantity
    
    idx_bad_disc = df_orders_raw.sample(n=8, random_state=18).index
    df_orders_raw.loc[idx_bad_disc, "discount_pct"] = 1.50 # Invalid discount 150%
    
    # F. Calculation mismatch (Accuracy dimension)
    idx_bad_total = df_orders_raw.sample(n=15, random_state=19).index
    df_orders_raw.loc[idx_bad_total, "order_total_kes"] = -9999.00
    
    # Save raw files
    df_stores_raw.to_csv(os.path.join(output_dir, "raw_stores.csv"), index=False)
    df_products.to_csv(os.path.join(output_dir, "raw_products.csv"), index=False)
    df_customers_raw.to_csv(os.path.join(output_dir, "raw_customers.csv"), index=False)
    df_orders_raw.to_csv(os.path.join(output_dir, "raw_orders.csv"), index=False)
    df_order_items_raw.to_csv(os.path.join(output_dir, "raw_order_items.csv"), index=False)
    
    print(f"Generated Raw Datasets in {output_dir}/:")
    print(f" - Stores: {len(df_stores_raw)} rows")
    print(f" - Products: {len(df_products)} rows")
    print(f" - Customers: {len(df_customers_raw)} rows")
    print(f" - Orders: {len(df_orders_raw)} rows")
    print(f" - Order Items: {len(df_order_items_raw)} rows")

if __name__ == "__main__":
    generate_duka_dataset("C:/Users/georg/.gemini/antigravity/scratch/plp-capstone--track---George-Tipango-/data")
