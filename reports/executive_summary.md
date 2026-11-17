# Executive Summary: Duka Electronics Retail & E-Commerce Sales Performance (H1 2026)

**To**: Grace Muthoni, Chief Commercial Officer (CCO) & Executive Committee  
**From**: George Tipango, Lead Commercial Data Analyst  
**Date**: November 17, 2026  
**Track**: Track A – Retail and E-Commerce Performance Analysis  
**Repository**: [plp-capstone-trackA-george-tipango](https://github.com/georgetipango88-dev/plp-capstone--track---George-Tipango-)  
**Interactive Dashboard**: [Looker Studio Live Dashboard](https://lookerstudio.google.com/reporting/plp-capstone-duka-electronics-george-tipango)

---

## 1. The Big Idea
**Duka Electronics delivered KES 1.01 Billion in gross sales across H1 2026 (+6.1% vs target), but enterprise profitability was severely undermined by unconstrained promotional discounting and regional misallocation.** While Nairobi branches generate 53% of baseline revenue, **Eldoret surged +50% Quarter-over-Quarter (QoQ)**, establishing itself as Kenya's highest-velocity retail growth corridor. Concurrently, high promotional discount tiers (15%–20%) failed to stimulate proportional basket volume while collapsing realized gross margins from **20.8% down to 6.4%**. 

By capping promotional discounting at 10%, reallocating KES 8.0M of the H2 commercial budget to Eldoret inventory expansion, and activating automated retention workflows for high-value RFM customer segments, Duka Electronics can capture an estimated **KES 42.5 Million in incremental gross profit** in H2 2026.

---

## 2. Key Analytical Findings

1. **Regional Polarization & The Eldoret Growth Frontier**:
   - **Nairobi Dominance**: The Nairobi CBD Flagship and Westlands Hub contributed a combined **KES 538.5M (53.4%)** of gross revenue and KES 99.8M in gross profit.
   - **Eldoret Acceleration**: Eldoret Highland Mall accelerated from KES 34.2M in Q1 to **KES 51.3M in Q2 (+50.0% QoQ growth)**, outpacing all other branches.
   - **Coast & Rift Valley Contractions**: Mombasa Old Port Mall and Nakuru Rift Hub contracted by **-24.8%** and **-26.1% QoQ** respectively, driven by stock-outs in mid-tier computing and local supply disruptions.

2. **The Computing Pareto Phenomenon**:
   - **Laptops & Computing** generated **KES 584.5M (58.0% of total enterprise revenue)** while accounting for only **22.3% of total unit transaction volume**.
   - Conversely, **Accessories & Peripherals** represented **26.4% of total unit volume** but contributed merely **6.8% of gross revenue**. Cross-selling attachment rates remain low at **1.83 Units per Transaction (UPT)**.

3. **Promotional Elasticity & Margin Dilution (Statistical Proof)**:
   - Full-price transactions (0% discount) delivered a robust **20.8% gross margin** and KES 116,006 Average Order Value (AOV).
   - Orders discounted at 15% and 20% experienced catastrophic margin compression to **10.9%** and **6.4%** respectively.
   - An independent two-sample t-test confirmed that undiscounted transactions yield statistically significant and substantially superior gross margins ($t = 118.42, p < 0.0001, \text{Cohen's } d = 2.45$). Price elasticity analysis reveals that steep discounts attract margin-eroding single-item purchases rather than basket expansion.

4. **Customer Behavioral Concentration (RFM Segmentation)**:
   - **Champions & Loyalists** (32.1% of customer base) accounted for **68.3% of cumulative revenue (KES 688.3M)** with an average lifetime spend of KES 784,000.
   - **At-Risk High-Value Customers** (11.8% of revenue, 324 customers) have not transacted in $>60$ days, representing KES 118.9M in vulnerable recurring revenue.

5. **Payment Rail Dynamics**:
   - **M-Pesa** remains the undisputed lifeblood of settlement, capturing **66.8% of completed transactions** and **67.5% of total value (KES 680.6M)**. Credit/Debit Cards accounted for 18.2%, and Bank Transfers represented 10.1% (predominantly corporate B2B bulk purchases).

---

## 3. Strategic Recommendations & Action Plan

| Priority | Strategic Initiative | Actionable Directives | Target Stakeholder | Projected Financial Impact |
| :---: | :--- | :--- | :--- | :--- |
| **P1** | **Eldoret Showroom Expansion** | Reallocate KES 8.0M of H2 expansion capex to expand showroom floor space and double computing inventory in Eldoret Highland Mall. | Retail Operations / Supply Chain | +KES 22.0M in H2 gross revenue |
| **P2** | **Discount Guardrails & Bundling** | Eliminate cash discounts $>10\%$. Replace steep markdowns with margin-accretive accessory bundles (e.g., Laptop Sleeve + Mouse at 35% margin). | Head of Merchandising / CCO | +KES 18.5M gross margin recovery |
| **P3** | **At-Risk Customer Retention** | Deploy automated, personalized WhatsApp/SMS re-engagement offers featuring exclusive hardware trade-in vouchers to the 324 At-Risk customers. | CRM & Digital Marketing | KES 12.0M churn mitigation |
| **P4** | **Safaricom Merchant Tier Optimization** | Renegotiate merchant settlement fees based on KES 680M+ annualized transaction throughput, lowering processing costs by 25 bps. | Finance / Treasury | +KES 1.7M annual operational savings |

---

## 4. Projected Business Impact
Implementing these directives for H2 2026 will transform commercial efficiency:
- **Net Profit Expansion**: Recapturing diluted margin from the 15% and 20% discount tiers expands enterprise gross margin from **18.7% to 21.4%**, generating **KES 27.2M** in recovered trading margin.
- **Revenue Acceleration**: Capitalizing on Eldoret's momentum and revitalizing Mombasa/Nakuru inventory generates **+KES 35.0M** in incremental regional gross sales.
- **Combined H2 Financial Lift**: Estimated **KES 42.5 Million in incremental gross trading profit**.

---

## 5. Limitations & Risk Factors
1. **Macroeconomic FX Fluctuations**: As an electronics retailer importing SKUs denominated in USD, depreciation of the Kenya Shilling (KES) represents an unhedged margin risk on computing inventory.
2. **Attribution of Cash Transactions**: Walk-in retail transactions settling via cash (4.9% of volume) lacked persistent phone identifiers, requiring conservative modal imputation during customer profiling.
3. **Six-Month Observation Horizon**: Analysis is bounded within H1 2026; macroeconomic seasonality associated with Q4 Black Friday and Christmas cycles will require iterative model recalibration.
4. **Competitor Pricing Visibility**: The dataset does not incorporate real-time scraper feeds from competitors (e.g., Jumia, Hotpoint), limiting external price elasticity benchmarking.

