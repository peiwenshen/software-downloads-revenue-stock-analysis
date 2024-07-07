import json
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from mpl_toolkits import axisartist
from mpl_toolkits.axes_grid1 import host_subplot

# Load JSON data from files
def load_json_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    df = pd.DataFrame(data)
    df['num_downloads'] = df['num_downloads'].astype(int)
    return df

# Fetch stock data
def get_stock_data(ticker, start_date, end_date):
    stock = yf.Ticker(ticker)
    return stock.history(start=start_date, end=end_date)

# Fetch quarterly revenue data
def get_revenue_data(ticker):
    stock = yf.Ticker(ticker)
    financials = stock.quarterly_financials.T
    if 'Total Revenue' in financials.columns:
        revenue_data = financials[['Total Revenue']].copy()
        revenue_data.reset_index(inplace=True)
        revenue_data.rename(columns={'index': 'quarter', 'Total Revenue': 'revenue'}, inplace=True)
        revenue_data['quarter'] = pd.to_datetime(revenue_data['quarter'])
        return revenue_data
    else:
        return pd.DataFrame(columns=['quarter', 'revenue'])

# Plot data using axisartist
def plot_data(download_data, revenue_data, price_data, package, ticker):
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Plot stock price
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Stock Price', color='tab:blue')
    ax1.plot(price_data[package].index, price_data[package]['Close'], color='tab:blue', label='Stock Price')
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    # Create a second y-axis for downloads
    ax2 = ax1.twinx()
    ax2.set_ylabel('Downloads', color='tab:green')
    ax2.plot(download_data[package].index, download_data[package]['num_downloads'], color='tab:green', label='Downloads')
    ax2.tick_params(axis='y', labelcolor='tab:green')

    # Create a third y-axis for revenue
    ax3 = ax1.twinx()
    ax3.spines['right'].set_position(('outward', 80))
    ax3.set_ylabel('Revenue', color='tab:orange')
    ax3.plot(revenue_data[package].index, revenue_data[package]['revenue'], color='tab:orange', label='Revenue')
    ax3.tick_params(axis='y', labelcolor='tab:orange')

    # Format y-axis labels
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x):,}'))
    ax3.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x):,}'))

    # Combine legends
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    lines3, labels3 = ax3.get_legend_handles_labels()
    ax1.legend(lines + lines2 + lines3, labels + labels2 + labels3, loc='upper left', bbox_to_anchor=(0.1, 0.9))

    fig.suptitle(f"{ticker} Stock Price, {package} Downloads, and Revenue")
    fig.tight_layout()
    plt.show()


# Main function
def main():
    packages = {
        # 'stripe': 'stripe',
        'confluent-kafka': 'CFLT',
        'pymongo': 'MDB',
        'datadog': 'DDOG',
        'snowflake-connector-python': 'SNOW',
        'elasticsearch': 'ESTC',
        'twilio': 'TWLO',
    }
    
    # Load and prepare download data
    download_data = {}
    for package in packages.keys():
        file_path = f"{package}.json"
        df = load_json_data(file_path)
        df['month'] = pd.to_datetime(df['month'])
        df.set_index('month', inplace=True)
        df = df.iloc[1:]
        download_data[package] = df

    
    # Fetch stock data and prepare price data
    price_data = {}
    for package, ticker in packages.items():
        start_date = download_data[package].index.min()
        end_date = download_data[package].index.max()
        stock_data = get_stock_data(ticker, start_date, end_date)
        stock_data['month'] = stock_data.index.to_period('M').to_timestamp()
        stock_data = stock_data[['month', 'Close']].copy()
        stock_data = stock_data.drop_duplicates('month')
        stock_data.set_index('month', inplace=True)  # Set month as index
        price_data[package] = stock_data
    
    
    # Fetch quarterly revenue data
    revenue_data = {}
    for package, ticker in packages.items():
        print(ticker)
        revenue_df = get_revenue_data(ticker)
        revenue_df.set_index('quarter', inplace=True)
        revenue_data[package] = revenue_df

    # Plot data
    for package, ticker in packages.items():
        plot_data(download_data, revenue_data, price_data, package, ticker)
    
    
if __name__ == "__main__":
    main()