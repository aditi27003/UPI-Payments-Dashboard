# UPI Payments Revolution: Power BI Dashboard

An interactive Power BI dashboard on how India's **Unified Payments Interface (UPI)** grew from zero to more than **24 billion transactions a month**. It covers who wins the app war, which banks carry the load, where people spend, and which states are adopting fastest.

All data is official, from the **National Payments Corporation of India (NPCI)**.

---

## Headline numbers (September 2026)

| Metric | Value |
|---|---|
| Monthly transactions | **24.07 billion** |
| Monthly value | **₹29.37 lakh crore** |
| Year-on-year volume growth | **+22.6%** |
| Average ticket size | **₹1,220** (down from ₹1,828 in Sep 2020) |
| Banks live on UPI | **756** |

## Key insights

1. **Hyper-growth:** volume went from 1.8 bn transactions a month (Sep 2020) to 24.1 bn (Sep 2026), about 13x in six years. FY2025-26 alone processed **241.6 bn transactions worth ₹314 lakh crore**.
2. **UPI is going small-ticket:** the average payment fell from ₹1,828 to ₹1,220 as UPI replaced cash for everyday spending.
3. **Merchants took over:** person-to-merchant (P2M) payments rose from **41% to 63%** of volume between Apr 2022 and Aug 2026. A typical P2M payment is ~₹577, against ~₹2,319 for person-to-person.
4. **A duopoly:** PhonePe (45.9%) and Google Pay (32.4%) handle **78% of all UPI transactions** (Aug 2026).
5. **Paytm's fall:** its share dropped from 15.0% (Apr 2022) to ~8% after the RBI's action on Paytm Payments Bank in early 2024.
6. **New challengers:** Navi went from nothing to **4.4%** share in about two years. super.money and BHIM are also growing fast.
7. **Public-sector banks dominate:** State Bank of India alone sends **6.2 bn** UPI transactions a month, more than the next three banks combined.
8. **Everyday spending:** groceries (4.0 bn transactions a month) far outrank every other merchant category.

## Dashboard pages

| Page | What it shows |
|---|---|
| **Overview** | KPI cards, monthly volume trend since 2016, value by financial year, average ticket trend, P2M share trend, financial-year slicer |
| **App Wars** | Market-share donut, share trend for key apps, app leaderboard with YoY growth, month slicer |
| **Banks & Merchants** | Top remitter banks, bank scorecard (share, YoY growth, avg ticket), top merchant categories, P2P vs P2M ticket size |
| **States** | Transactions by state and a state scorecard with YoY growth and average ticket |

## Repository structure

```
├── UPI_Payments_Dashboard.pbix            # Finished dashboard (open in Power BI Desktop)
├── UPI_Payments_Dashboard_Template.pbit   # Same report as a template (loads data on open)
├── data/
│   ├── UPI_Data.xlsx                      # Clean dataset used by the dashboard (7 tables)
│   └── csv/                               # Same tables as CSV files
├── model/
│   ├── DAX_Measures.md                    # Every DAX measure, documented
│   └── UPI_model.tmdl                     # Full semantic model as a TMDL script
└── scripts/
    ├── build_dataset.py                   # Builds UPI_Data.xlsx from the raw NPCI extracts
    └── raw/                               # Raw extracts from NPCI statistics pages
```

## Data model

A star schema with a shared **Date_Table** (monthly, Indian financial year April–March) joined one-to-many to six fact tables:

| Table | Grain | Coverage |
|---|---|---|
| Monthly_Totals | Month | Apr 2016 – Sep 2026 |
| App_Share | Month × App (top 12 + Others) | Apr 2022 – Aug 2026 |
| P2P_P2M | Month × Transaction type | Apr 2022 – Aug 2026 |
| Top_Banks | Month × Bank (top 25 remitter banks) | Aug 2024, Aug 2025, Aug 2026 |
| States | Month × State | Aug 2025, Aug 2026 |
| Merchant_Categories | Merchant category (MCC) | Aug 2026 |

Units: **volume in million transactions**, **value in ₹ crore** (1 lakh crore = 100,000 crore).

## How to open

1. Install [Power BI Desktop](https://powerbi.microsoft.com/desktop/) (free, Windows).
2. Download this repository (**Code → Download ZIP**) and extract it.
3. Open `UPI_Payments_Dashboard.pbix`.
4. To refresh the data, point the queries at your copy of the Excel file: **Transform data → Data source settings → Change Source**, select `data/UPI_Data.xlsx`, then click **Refresh**.

## Data notes

- Source: [NPCI UPI Product Statistics](https://www.npci.org.in/product/upi/product-statistics) and [NPCI UPI Ecosystem Statistics](https://www.npci.org.in/product/ecosystem-statistics/upi).
- "Paytm Payments Bank App" and "Paytm (OCL)" are merged as **Paytm**. FamPay name variants are merged as **FamApp by Trio**.
- App-wise totals add up to within ±2.5% of NPCI's monthly totals, because they count customer-initiated transactions only.
- "Unclassified" in state data is volume NPCI could not map to a state. It is excluded from state shares.

## Tools used

Power BI Desktop · DAX · Power Query (M) · Python (pandas, openpyxl) · Excel

---

**Author:** Aditi Srivastava, MBA (2025–27), Graphic Era (Deemed to be University), Dehradun
