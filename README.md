# Sales Analytics System

A small Python-based sales analytics system that:
- Loads pipe-delimited sales records from `data/sales_data.txt`
- Cleans invalid records based on validation rules
- Computes analytics (revenue by product/category key, top-selling product, region-wise distribution)
- Fetches real-time product details from DummyJSON API
- Writes a report to `output/analysis_report.txt`

## Project Structure

```text
sales-analytics-system/
├── main.py
├── requirements.txt
├── utils/
│   ├── file_handler.py
│   ├── data_processor.py
│   └── api_handler.py
├── data/
│   └── sales_data.txt
└── output/
    └── analysis_report.txt

