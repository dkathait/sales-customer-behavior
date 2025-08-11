# sales-customer-behavior
Data Analytics project: ETL, analysis, and reporting using Python, MySQL, Google Sheets, and Power BI.
# Sales Customer Behavior Project

This project demonstrates an end-to-end data analytics workflow:
- Extract data from Google Sheets using Python
- Load cleaned data into MySQL database
- Perform analysis and visualization with Python (matplotlib, pandas)
- Generate a professional Excel report combining tables and charts
- Prepare data aggregates for Power BI visualizations

## Tech stack
- Python (pandas, SQLAlchemy, gspread, openpyxl)
- MySQL
- Google Sheets API
- Power BI (for dashboards)

## How to use
1. Setup Google Cloud service account and share your Google Sheet with it
2. Configure MySQL database and update `.env` file with credentials
3. Run `etl.py` to load data from Google Sheets to MySQL
4. Run `analyze_data.py` to create charts and view analysis
5. Run `create_report.py` to generate Excel report with charts
6. Use Power BI to connect to MySQL or import CSVs for dashboards

## Sample Data
Included `sample_data.csv` to help create your Google Sheet for testing.

## Project Structure
- `etl.py`: Extract, transform, load script
- `analyze_data.py`: Analysis and visualization
- `create_report.py`: Excel report generation
- `schema.sql`: MySQL database schema
- `plots/`: Saved charts images
- `.env.example`: Sample environment variables (don't commit real secrets)
- `requirements.txt`: Python dependencies

---



