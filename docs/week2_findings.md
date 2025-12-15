## Week 2 Data Processing and Feature Engineering Summary

The findings from Week 2 primarily focus on data cleaning, data storage optimization, and early feature engineering insights essential for building a robust recommendation system.

### 1. Feature Insight: Rank vs. Popularity

A key finding relates to the nature of the core scoring metrics:

* **Orthogonal Signals:** **Rank** and **Popularity** were identified as **orthogonal signals** (statistically independent of one another). 
* **Modeling Strategy:** This means they represent distinct aspects: **Rank** is a signal of inherent *quality* (high score, few viewers needed), while **Popularity** is a signal of *exposure* and mainstream appeal. By explicitly modeling both, the system can be designed to **balance new discovery** (high rank, low popularity) with **mainstream appeal** (high popularity, potentially lower rank) under real-world data constraints.

### 2. Data Persistence & Cleaning

Several critical decisions were made regarding data structure and integrity:

* **JSONB Adoption Avoided:** The use of the PostgreSQL JSONB data type for complex fields (like alternate_titles) was considered due to the mix of special characters in the tiles but ultimately decided against. This was due to concerns that while JSONB simplified upfront data cleanup, the long-term trade-off of potentially slower query times was deemed too high for the production database.
* **Data Integrity:** All **duplicate anime entries** were identified and removed from the dataset to ensure unique records.
* **Data Type Correction:** Columns containing numerical integers (e.g., `year`, `episodes`) were correctly saved as `INT` data types, resolving issues where the presence of NaN values forced Pandas to default them to less efficient `float` types.
* **Alternate Titles:** The structure of the `alternate_titles` column was reformatted to ensure consistency and utility for searching or matching, supporting the JSONB adoption.