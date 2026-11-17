-- =====================================================================
-- Duka Electronics Kenya Ltd. - Analytical SQL Queries
-- Author: George Tipango
-- Track: Track A - Retail & E-Commerce Performance (H1 2026)
-- Target Database: SQLite (database/duka_sales.db)
-- =====================================================================

-- ---------------------------------------------------------------------
-- QUERY 1: Branch Performance & Margin Analysis (JOIN & Aggregation)
-- Business Question: Which branches drive top-line revenue, and how do their
-- gross profit margins compare across brick-and-mortar vs digital channels?
-- ---------------------------------------------------------------------
SELECT 
    s.store_id,
    s.store_name,
    s.county,
    s.region,
    s.channel,
    COUNT(o.order_id) AS total_orders,
    SUM(o.items_count) AS total_units_sold,
    ROUND(SUM(o.order_total_kes), 2) AS total_revenue_kes,
    ROUND(SUM(o.order_profit_kes), 2) AS total_profit_kes,
    ROUND(AVG(o.order_total_kes), 2) AS aov_kes,
    ROUND((SUM(o.order_profit_kes) * 100.0 / SUM(o.order_total_kes)), 2) AS gross_margin_pct
FROM fct_orders o
INNER JOIN dim_stores s ON o.store_id = s.store_id
WHERE o.order_status = 'Completed'
GROUP BY s.store_id, s.store_name, s.county, s.region, s.channel
ORDER BY total_revenue_kes DESC;


-- ---------------------------------------------------------------------
-- QUERY 2: Quarter-over-Quarter Regional Growth (Window Function: LAG)
-- Business Question: What is the quarter-over-quarter revenue growth for each
-- branch, and which branches accelerated or declined from Q1 to Q2?
-- ---------------------------------------------------------------------
WITH QuarterlyBranchSales AS (
    SELECT 
        s.store_name,
        s.region,
        CASE 
            WHEN strftime('%m', o.order_date) IN ('01', '02', '03') THEN 'Q1-2026'
            ELSE 'Q2-2026'
        END AS sales_quarter,
        ROUND(SUM(o.order_total_kes), 2) AS quarter_revenue_kes
    FROM fct_orders o
    INNER JOIN dim_stores s ON o.store_id = s.store_id
    WHERE o.order_status = 'Completed'
    GROUP BY s.store_name, s.region, sales_quarter
)
SELECT 
    store_name,
    region,
    sales_quarter,
    quarter_revenue_kes,
    LAG(quarter_revenue_kes, 1) OVER (
        PARTITION BY store_name 
        ORDER BY sales_quarter
    ) AS prev_quarter_revenue_kes,
    ROUND(
        (quarter_revenue_kes - LAG(quarter_revenue_kes, 1) OVER (PARTITION BY store_name ORDER BY sales_quarter)) * 100.0 /
        LAG(quarter_revenue_kes, 1) OVER (PARTITION BY store_name ORDER BY sales_quarter),
        2
    ) AS qoq_growth_pct
FROM QuarterlyBranchSales
ORDER BY store_name, sales_quarter;


-- ---------------------------------------------------------------------
-- QUERY 3: High-Performing Product Categories (GROUP BY with HAVING)
-- Business Question: Which product categories generate over KES 10,000,000
-- in completed sales, and what is their average profitability per unit?
-- ---------------------------------------------------------------------
SELECT 
    p.category,
    COUNT(DISTINCT oi.order_id) AS distinct_orders,
    SUM(oi.quantity) AS total_quantity_sold,
    ROUND(SUM(oi.line_total_kes), 2) AS category_revenue_kes,
    ROUND(SUM(oi.profit_kes), 2) AS category_profit_kes,
    ROUND((SUM(oi.profit_kes) * 100.0 / SUM(oi.line_total_kes)), 2) AS category_margin_pct,
    ROUND(SUM(oi.profit_kes) / SUM(oi.quantity), 2) AS profit_per_unit_kes
FROM fct_order_items oi
INNER JOIN dim_products p ON oi.product_id = p.product_id
INNER JOIN fct_orders o ON oi.order_id = o.order_id
WHERE o.order_status = 'Completed'
GROUP BY p.category
HAVING SUM(oi.line_total_kes) >= 10000000.00
ORDER BY category_revenue_kes DESC;


-- ---------------------------------------------------------------------
-- QUERY 4: Top 3 SKUs per Category (Window Function: DENSE_RANK)
-- Business Question: Within each product line, what are the top 3 revenue-
-- generating products that drive category performance?
-- ---------------------------------------------------------------------
WITH RankedProducts AS (
    SELECT 
        p.category,
        p.product_id,
        p.product_name,
        SUM(oi.quantity) AS units_sold,
        ROUND(SUM(oi.line_total_kes), 2) AS total_sales_kes,
        ROUND(SUM(oi.profit_kes), 2) AS total_profit_kes,
        DENSE_RANK() OVER (
            PARTITION BY p.category 
            ORDER BY SUM(oi.line_total_kes) DESC
        ) AS rank_in_category
    FROM fct_order_items oi
    INNER JOIN dim_products p ON oi.product_id = p.product_id
    INNER JOIN fct_orders o ON oi.order_id = o.order_id
    WHERE o.order_status = 'Completed'
    GROUP BY p.category, p.product_id, p.product_name
)
SELECT 
    category,
    rank_in_category,
    product_id,
    product_name,
    units_sold,
    total_sales_kes,
    total_profit_kes
FROM RankedProducts
WHERE rank_in_category <= 3
ORDER BY category, rank_in_category;


-- ---------------------------------------------------------------------
-- QUERY 5: Customer RFM Behavioral Metric Base (Multi-table Aggregation)
-- Business Question: What are the base Recency (days since last purchase),
-- Frequency (order count), and Monetary (lifetime spend) values per customer?
-- ---------------------------------------------------------------------
SELECT 
    c.pseudo_customer_id,
    c.county,
    c.initial_tier,
    COUNT(o.order_id) AS total_orders,
    SUM(o.items_count) AS total_units_bought,
    ROUND(SUM(o.order_total_kes), 2) AS lifetime_spend_kes,
    ROUND(AVG(o.order_total_kes), 2) AS avg_spend_per_order_kes,
    MAX(o.order_date) AS last_order_date,
    CAST((julianday('2026-06-30') - julianday(MAX(o.order_date))) AS INTEGER) AS recency_days
FROM dim_customers c
INNER JOIN fct_orders o ON c.pseudo_customer_id = o.pseudo_customer_id
WHERE o.order_status = 'Completed'
GROUP BY c.pseudo_customer_id, c.county, c.initial_tier
ORDER BY lifetime_spend_kes DESC
LIMIT 50;


-- ---------------------------------------------------------------------
-- QUERY 6: Promotional Elasticity and Margin Erosion Analysis
-- Business Question: How does increasing promotional discount percentage
-- impact average order value and erode net gross margin percentage?
-- ---------------------------------------------------------------------
SELECT 
    CAST(ROUND(discount_pct * 100, 0) AS INTEGER) AS discount_tier_pct,
    COUNT(order_id) AS total_orders,
    ROUND(SUM(order_total_kes), 2) AS total_sales_kes,
    ROUND(AVG(order_total_kes), 2) AS avg_order_value_kes,
    ROUND(SUM(order_profit_kes), 2) AS total_profit_kes,
    ROUND((SUM(order_profit_kes) * 100.0 / SUM(order_total_kes)), 2) AS realized_profit_margin_pct
FROM fct_orders
WHERE order_status = 'Completed'
GROUP BY discount_tier_pct
ORDER BY discount_tier_pct ASC;


-- ---------------------------------------------------------------------
-- QUERY 7: Payment Channel Market Share and Transaction Value
-- Business Question: What is the transaction volume and revenue share
-- across payment channels (M-Pesa, Card, Bank, Cash)?
-- ---------------------------------------------------------------------
SELECT 
    payment_method,
    COUNT(order_id) AS transaction_count,
    ROUND(COUNT(order_id) * 100.0 / (SELECT COUNT(*) FROM fct_orders WHERE order_status = 'Completed'), 2) AS tx_volume_share_pct,
    ROUND(SUM(order_total_kes), 2) AS total_volume_kes,
    ROUND(SUM(order_total_kes) * 100.0 / (SELECT SUM(order_total_kes) FROM fct_orders WHERE order_status = 'Completed'), 2) AS revenue_share_pct,
    ROUND(AVG(order_total_kes), 2) AS avg_ticket_size_kes
FROM fct_orders
WHERE order_status = 'Completed'
GROUP BY payment_method
ORDER BY total_volume_kes DESC;
