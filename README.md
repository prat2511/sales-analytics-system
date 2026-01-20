# Sales Analytics System

Project Overview

This project implements a Sales Analytics System using Python.
It reads sales transactions from a text file, cleans and validates the data, performs analytical computations, enriches records using an external API, and generates formatted output reports.

The implementation strictly follows the assignment requirements for File Handling, Data Processing, API Integration, and Report Generation.

Functional Coverage (Mapped to Assignment)

	Part 1: File Handling & Preprocessing
		-Reads pipe-delimited sales data from data/sales_data.txt
		-Handles encoding issues (utf-8, latin-1, cp1252)
		-Skips headers and empty rows
		-Parses records into dictionaries
		-Validates transactions using business rules
		-Supports optional filtering by region and transaction amount

	Part 2: Data Processing & Analytics
		-Calculates total revenue
		-Performs region-wise sales analysis
		-Identifies top-selling products
		-Analyzes customer purchase behavior
		-Computes daily sales trends and peak sales day
		-Identifies low-performing products

	Part 3: API Integration
		-Fetches product data from DummyJSON API
		-Supports:
		-Products with ID range 1–100 (API limit constraint)
		-Additional fetch for IDs 101–200 to match sales ProductIDs
		-Enriches sales data with:
		-API category
		-Brand
		-Rating
		-Saves enriched data to file

	Part 4: Report Generation
		-Generates a comprehensive formatted text report including:
		-Overall summary
		-Region-wise performance
		-Top products and customers
		-Daily trends
		-API enrichment summary

	Part 5: Main Application Flow
		-Orchestrates the complete workflow
		-Displays progress steps in console
		-Uses structured error handling
		-Produces all required output files

## Project Structure

		sales-analytics-system/
		├── main.py
		├── requirements.txt
		├── utils/
		│   ├── file_handler.py
		│   ├── data_processor.py
		│   ├── api_handler.py
		│   └── report_generator.py
		├── data/
		│   ├── sales_data.txt
		│   └── enriched_sales_data.txt
		└── output/
			├── analysis_report.txt
			└── sales_report.txt


## How to Run
	pip install -r requirements.txt
	python main.py


##External API Used

	-DummyJSON Products API   : https://dummyjson.com/products

	-Note:
		-API returns IDs 1–100 by default (limit=100)

		-Additional fetch implemented for IDs 101–200 to align with sales ProductIDs

