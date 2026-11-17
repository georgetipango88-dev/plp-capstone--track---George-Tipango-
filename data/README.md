# Duka Electronics Sales & Customer Dataset (H1 2026)

## 1. Overview & Data Source
This dataset comprises sales transactions, retail inventory, customer records, and branch operations for **Duka Electronics Kenya Ltd.**, a premier electronics and computing retailer operating omnichannel operations across Kenya.

- **Data Track**: Track A (Retail and E-commerce Performance Analysis)
- **Time Horizon**: January 1, 2026 – June 30, 2026 (H1 2026)
- **Data Source**: Enterprise Transaction Database & Store POS logs via the course-aligned synthetic data generator (`generate_data.py`).
- **Date Accessed / Generated**: November 17, 2026
- **License**: Creative Commons Attribution 4.0 International (CC BY 4.0) for educational and research evaluation within the Power Learn Project (PLP) Data Analytics Capstone.

---

## 2. Table Specifications and Grain

The dataset consists of five related relational tables:

| Table | File Name | Grain (Primary Key) | Foreign Keys | Approximate Rows | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Stores** | `raw_stores.csv` | `store_id` | - | 7 | Retail brick-and-mortar branches and online platform details. |
| **Products** | `raw_products.csv` | `product_id` | - | 25 | Catalog of electronics, SKU pricing, unit costs, and categories. |
| **Customers** | `raw_customers.csv` | `customer_id` | - | 2,825 | Customer demographic profiles, onboarding dates, and tiers. |
| **Orders** | `raw_orders.csv` | `order_id` | `customer_id`, `store_id` | 9,435 | Transaction header records, payment channels, dates, and order status. |
| **Order Items** | `raw_order_items.csv`| `order_item_id` | `order_id`, `product_id` | 14,878 | Line-item details with quantities, discounts, line totals, and margins. |

---

## 3. Ethics and Privacy Statement (Section 4.13 Compliance)

In compliance with the **Kenya Data Protection Act (KDPA) 2019**, the **General Data Protection Regulation (GDPR)** principles, and PLP curriculum Section 4.13 standards, customer privacy and commercial sensitivity have been addressed through strict data governance:

### Personal and Sensitive Fields Identified:
1. `customer_name`: Full real names of individuals (Personally Identifiable Information - PII).
2. `email`: Direct personal and workplace email addresses.
3. `phone`: Mobile numbers (MSISDN) containing telecom carrier routing prefixes.
4. `county`: Geographic residence information (quasi-identifier when joined with transaction timestamps).

### Anonymization and Pseudonymization Protocol (`src/cleaning.py`):
- **Cryptographic Pseudonymization**: The original primary identifier is irreversibly mapped using salted SHA-256 cryptographic hashing to generate surrogate pseudonymous keys (`pseudo_customer_id`).
- **PII Stripping & Redaction**: Plaintext `customer_name` is purged from all analytical tables and production SQLite database layers.
- **Masking / Truncation**:
  - `phone` numbers are masked preserving only the country prefix and telecom identifier while zeroing personal subscriber digits (e.g., `+254701234567` -> `+254-70X-XXX-567`).
  - `email` addresses are redacted into generic masked domain strings (e.g., `k****@gmail.com`).
- **Data Aggregation**: All public-facing reports, dashboards, executive summaries, and presentation decks present insights aggregated at county, segment, cohort, category, and monthly/quarterly levels. No individual transaction or customer can be re-identified from the published deliverables.

---

## 4. Data Quality Dimensions Audited (Phase 3)

The raw data contains intentional real-world anomalies across the six core data-quality dimensions to validate the cleaning pipeline:
1. **Completeness**: Evaluates missing phone numbers and null promotional discounts.
2. **Uniqueness**: Identifies and deduplicates repeat order headers and customer records.
3. **Consistency**: Normalizes casing and nomenclature across payment methods (e.g., `mpesa`, `M_PESA` -> `M-Pesa`) and branch channels.
4. **Timeliness**: Screens for dates out of analytical scope (e.g., future timestamp anomalies).
5. **Validity**: Removes negative quantities, invalid discount percentages (>100%), and corrupted identifiers.
6. **Accuracy**: Re-verifies line item calculations (`line_total_kes = quantity * unit_price_kes * (1 - discount_pct)`) and reconciles header order totals.

---

## 5. How to Re-generate the Raw Data

To regenerate the raw synthetic files from scratch:
```bash
python data/generate_data.py
```
This produces all five CSV files deterministically with a random seed of `42`.

