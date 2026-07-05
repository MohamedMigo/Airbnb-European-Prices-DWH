# European Airbnb Market Analysis - DWH Project

## Overview
This project builds an end-to-end Data Warehouse for analyzing over 52,000 Airbnb listings across 10 European cities. The architecture follows the **Medallion Architecture** (Bronze, Silver, Gold).

## Project Structure
- **`1_bronze_layer/`**: Raw CSV data ingestion.
- **`2_silver_layer/`**: Data cleaning, handling missing values, and building the master dataset.
- **`3_gold_layer/`**: SQL scripts defining the Star Schema (Fact and Dimension tables).
- **`4_powerbi_dashboard/`**: The final interactive Power BI dashboard.
- **`other_scripts/`**: Additional exploratory and web scraping scripts.

## How to Run
1. Start with the `1_bronze_layer` to view the raw ingestion.
2. Run the cleaning scripts in the `2_silver_layer`.
3. Execute `star_schema.sql` in the `3_gold_layer` on your preferred data warehouse (e.g., Snowflake, PostgreSQL).
4. Open the `.pbix` file in the `4_powerbi_dashboard` folder to view the insights.