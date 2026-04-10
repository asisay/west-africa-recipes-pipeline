# West African Recipe Data Pipeline

## Overview

This project is an end-to-end data engineering pipeline that extracts recipe data from XML sitemaps, processes it using PySpark in Databricks, and loads the cleaned data into PostgreSQL.

## Architecture

```
Sitemap (XML)
   ↓
Python Scraper (requests, BeautifulSoup)
   ↓
Raw Data (CSV)
   ↓
Databricks (PySpark)
   ↓
Delta Table (recipes_enriched)
   ↓
Export (CSV/Parquet)
   ↓
PostgreSQL
```

## Tech Stack

* Python
* PySpark (Databricks)
* Delta Lake
* PostgreSQL
* Requests / BeautifulSoup
* CSV / Parquet

## Pipeline Steps

1. Extract recipe URLs from XML sitemap
2. Transform and clean recipe titles
3. Deduplicate records
4. Process data using PySpark in Databricks
5. Store processed data as Delta tables
6. Export structured data to CSV/Parquet
7. Load into PostgreSQL database

## How to Run

```bash
git clone https://github.com/asisay/west-africa-recipes-pipeline.git
cd recipe-data-pipeline
pip install -r requirements.txt
python main.py
```

## Features

* Modular ETL pipeline design
* Distributed data processing with Spark
* Automated workflows using Databricks
* Structured data storage in PostgreSQL

## Future Improvements

* Integrate AWS S3 for data lake storage
* Add Airflow for orchestration
* Implement incremental data loading
* Add data quality validation checks
