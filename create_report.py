import os
import pandas as pd
from openpyxl import Workbook
from openpyxl.drawing.image import Image
from openpyxl.utils.dataframe import dataframe_to_rows
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_PORT = os.getenv('MYSQL_PORT')
MYSQL_DB = os.getenv('MYSQL_DB')

PLOT_DIR = "plots"
REPORT_FILE = "Sales_Report.xlsx"

def get_engine():
    conn_str = f'mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}'
    return create_engine(conn_str)

def create_excel_report():
    engine = get_engine()
    df = pd.read_sql("SELECT * FROM sales_data", engine)

    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.to_period('M')
    df['Month'] = df['Month'].astype(str)  # Convert Period to string

    wb = Workbook()
    ws = wb.active
    ws.title = "Summary"

    # Write a title
    ws['A1'] = "Sales & Customer Behavior Report"

    # Add summary data frames
    # 1. Sales by Region
    region_sales = df.groupby('Region')['Price'].sum().sort_values(ascending=False).reset_index()
    ws.append([])
    ws.append(['Sales by Region'])
    for r in dataframe_to_rows(region_sales, index=False, header=True):
        ws.append(r)

    # Insert sales by region chart image
    img = Image(os.path.join(PLOT_DIR, "sales_by_region.png"))
    img.anchor = 'E3'
    ws.add_image(img)

    # 2. Monthly Sales Trend table
    monthly_sales = df.groupby('Month')['Price'].sum().reset_index()
    ws.append([])
    ws.append(['Monthly Sales Trend'])
    for r in dataframe_to_rows(monthly_sales, index=False, header=True):
        ws.append(r)

    img2 = Image(os.path.join(PLOT_DIR, "monthly_sales.png"))
    img2.anchor = 'E15'
    ws.add_image(img2)

    # 3. Top Products by Revenue
    top_products = df.groupby('Product')['Price'].sum().sort_values(ascending=False).head(5).reset_index()
    ws.append([])
    ws.append(['Top 5 Products by Revenue'])
    for r in dataframe_to_rows(top_products, index=False, header=True):
        ws.append(r)

    img3 = Image(os.path.join(PLOT_DIR, "top_products.png"))
    img3.anchor = 'E27'
    ws.add_image(img3)

    # 4. Top Customers by Purchases
    customer_orders = df.groupby('Customer_Name').size().sort_values(ascending=False).head(5).reset_index(name='Orders')
    ws.append([])
    ws.append(['Top 5 Customers by Purchases'])
    for r in dataframe_to_rows(customer_orders, index=False, header=True):
        ws.append(r)

    img4 = Image(os.path.join(PLOT_DIR, "top_customers.png"))
    img4.anchor = 'E39'
    ws.add_image(img4)

    wb.save(REPORT_FILE)
    print(f"Excel report saved as: {REPORT_FILE}")

if __name__ == "__main__":
    create_excel_report()
