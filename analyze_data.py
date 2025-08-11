import os
import matplotlib
matplotlib.use('MacOSX')  # Use MacOSX backend for macOS graphical support

import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from sqlalchemy import create_engine
from tabulate import tabulate

load_dotenv()

MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_PORT = os.getenv('MYSQL_PORT')
MYSQL_DB = os.getenv('MYSQL_DB')

PLOT_DIR = "plots"
os.makedirs(PLOT_DIR, exist_ok=True)

def get_engine():
    connection_string = f'mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}'
    return create_engine(connection_string)

def save_plot(fig, filename):
    filepath = os.path.join(PLOT_DIR, filename)
    fig.savefig(filepath, bbox_inches='tight')
    print(f"Saved plot: {filepath}")
    plt.close(fig)

def analyze_sales_data():
    engine = get_engine()
    df = pd.read_sql("SELECT * FROM sales_data", engine)
    
    print("\n===== DATA OVERVIEW =====")
    print(tabulate(df.head(), headers="keys", tablefmt="psql"))
    print("\nRows:", len(df), "| Columns:", len(df.columns))

    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.to_period('M')

    total_sales = df['Price'].sum()

    # 1. Sales by Region
    region_sales = df.groupby('Region')['Price'].sum().sort_values(ascending=False)
    print("\n===== SALES BY REGION =====")
    print(tabulate(region_sales.reset_index(), headers=['Region', 'Total Sales'], tablefmt="psql"))
    fig, ax = plt.subplots()
    region_sales.plot(kind='bar', ax=ax, title='Sales by Region', color='skyblue')
    ax.set_ylabel('Total Sales')
    save_plot(fig, "sales_by_region.png")
    plt.show(block=True)

    # 2. Monthly Sales Trend
    monthly_sales = df.groupby('Month')['Price'].sum()
    fig, ax = plt.subplots()
    monthly_sales.plot(kind='line', marker='o', ax=ax, title='Monthly Sales Trend', color='green')
    ax.set_ylabel('Total Sales')
    save_plot(fig, "monthly_sales.png")
    plt.show(block=True)

    # 3. Top Products by Revenue
    top_products = df.groupby('Product')['Price'].sum().sort_values(ascending=False).head(5)
    print("\n===== TOP 5 PRODUCTS BY REVENUE =====")
    print(tabulate(top_products.reset_index(), headers=['Product', 'Revenue'], tablefmt="psql"))
    fig, ax = plt.subplots()
    top_products.plot(kind='bar', ax=ax, title='Top 5 Products', color='orange')
    ax.set_ylabel('Revenue')
    save_plot(fig, "top_products.png")
    plt.show(block=True)

    # 4. Customer Purchase Frequency
    customer_orders = df.groupby('Customer_Name').size().sort_values(ascending=False).head(5)
    print("\n===== TOP 5 CUSTOMERS BY PURCHASES =====")
    print(tabulate(customer_orders.reset_index(), headers=['Customer', 'Orders'], tablefmt="psql"))
    fig, ax = plt.subplots()
    customer_orders.plot(kind='bar', ax=ax, title='Top Customers', color='purple')
    ax.set_ylabel('Orders')
    save_plot(fig, "top_customers.png")
    plt.show(block=True)

    # Executive Summary
    print("\n===== EXECUTIVE SUMMARY =====")
    print(f"Total Sales: ₹{total_sales:,.2f}")
    print(f"Best Performing Region: {region_sales.idxmax()} (₹{region_sales.max():,.2f})")
    print(f"Best Selling Product: {top_products.idxmax()} (₹{top_products.max():,.2f})")
    print(f"Top Customer by Purchases: {customer_orders.idxmax()} ({customer_orders.max()} orders)")
    print("All plots saved in the 'plots/' folder.")

if __name__ == "__main__":
    analyze_sales_data()
