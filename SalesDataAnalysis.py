# Importing necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def open_and_clean_file(file_name):
    """
    Opens the dataset and cleans missing values.
    Returns a cleaned dataframe.
    """
    print("Reading the data file...")
    data = pd.read_csv(file_name, encoding="ISO-8859-1")
    print("\nSample of raw data:")
    print(data.head())

    print("\nMissing values in each column:")
    print(data.isnull().sum())

    # Fix the missing values
    data.fillna(data.median(numeric_only=True), inplace=True)  # Fill numeric missing data
    data.dropna(inplace=True)  # Remove rows with missing non-numeric values

    print("\nData after cleaning:")
    print(data.head())
    return data

def calculate_data_statistics(dataframe, columns):
    """
    Calculates basic statistics for the given columns.
    Returns the statistics as a dictionary.
    """
    stats = {}
    for col in columns:
        if col in dataframe.columns:
            stats[col] = {
                "Mean": round(dataframe[col].mean(), 2),
                "Median": round(dataframe[col].median(), 2),
                "Standard Deviation": round(dataframe[col].std(), 2),
                "Mode": round(dataframe[col].mode()[0], 2),
            }
    return stats

def create_sales_graph(data):
    """
    Displays a line graph showing sales trends over time.
    """
    if "ORDERDATE" in data.columns:
        data["ORDERDATE"] = pd.to_datetime(data["ORDERDATE"], errors="coerce")
        data.dropna(subset=["ORDERDATE"], inplace=True)
        data["YearMonth"] = data["ORDERDATE"].dt.to_period("M")

        monthly_sales = data.groupby("YearMonth")["SALES"].sum()

        plt.figure(figsize=(10, 5))
        monthly_sales.plot(marker="o", color="blue")
        plt.title("Monthly Sales Over Time")
        plt.xlabel("Year-Month")
        plt.ylabel("Total Sales")
        plt.grid()
        plt.show()

def show_monthly_sales(data):
    """
    Plots a bar chart showing sales for each month.
    """
    if "ORDERDATE" in data.columns:
        data["Month"] = data["ORDERDATE"].dt.month
        month_sales = data.groupby("Month")["SALES"].sum()

        plt.figure(figsize=(10, 5))
        sns.barplot(x=month_sales.index, y=month_sales.values, color="green")
        plt.title("Sales Per Month")
        plt.xlabel("Month")
        plt.ylabel("Total Sales")
        plt.show()

def find_top_products(data):
    """
    Creates a bar chart for the top 10 products based on total sales.
    """
    if "PRODUCTCODE" in data.columns:
        top_products = data.groupby("PRODUCTCODE")["SALES"].sum().sort_values(ascending=False).head(10)

        plt.figure(figsize=(10, 6))
        sns.barplot(y=top_products.index, x=top_products.values, color="purple")
        plt.title("Top 10 Products by Sales")
        plt.xlabel("Sales Amount")
        plt.ylabel("Product Code")
        plt.show()

def main():
    """
    Main function to run the sales analysis.
    """
    # Specify the data file
    file_name = "Sales Data.csv"

    # Step 1: Clean file and load data
    sales_data = open_and_clean_file(file_name)

    # Step 2: Calculate statistics
    important_columns = ["SALES", "QUANTITYORDERED"]
    statistics = calculate_data_statistics(sales_data, important_columns)
    print("\nStatistics for the data:")
    for col_name, col_stats in statistics.items():
        print(f"\n{col_name}:")
        for stat, value in col_stats.items():
            print(f"{stat}: {value}")

    # Step 3: Visualizations
    create_sales_graph(sales_data)  # Sales trends over time
    show_monthly_sales(sales_data)  # Monthly sales patterns
    find_top_products(sales_data)  # Top products

# Start the program
if __name__ == "__main__":
    main()
