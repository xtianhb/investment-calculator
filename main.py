

import yfinance as yf
import yaml
import matplotlib.pyplot as plt
import pandas as pd

def calculate_historical_returns(ticker_symbol, start_date, end_date, initial_contribution, periodic_contribution):

    etf = yf.Ticker(ticker_symbol)
    historical_data = etf.history(start=start_date, end=end_date)
    
    if historical_data.empty:
        raise ValueError("No data found for the given ETF and time range.")
    
    # Get adjusted close prices
    historical_data = historical_data[['Close']].copy()
    historical_data['Date'] = historical_data.index
    historical_data.reset_index(drop=True, inplace=True)

    # Initialize investment details
    capital_contribution = initial_contribution
    shares = initial_contribution / historical_data['Close'].iloc[0]
    total_contribution = []
    total_value = []
    interest_gained = []

    # Simulate growth over time
    for index, row in historical_data.iterrows():
        if index > 0:
            # Add periodic contribution (if any)
            capital_contribution += periodic_contribution
            shares += periodic_contribution / row['Close']

        # Calculate total value and interest
        current_value = shares * row['Close']
        total_contribution.append(capital_contribution)
        total_value.append(current_value)
        interest_gained.append(current_value - capital_contribution)
    
    # Add results to DataFrame
    historical_data['Capital Contribution'] = total_contribution
    historical_data['Total Value'] = total_value
    historical_data['Interest Gained'] = interest_gained

    return historical_data

def print_returns(historical_data):
    start_price = historical_data['Close'].iloc[0]
    end_price = historical_data['Close'].iloc[-1]
    capital_contribution = historical_data['Capital Contribution'].iloc[-1]
    interest_gained = historical_data['Interest Gained'].iloc[-1]
    shares_purchased = historical_data['Total Value'].iloc[-1] / historical_data['Close'].iloc[-1]
    return_percentage = (interest_gained / capital_contribution) * 100
    initial_contribution = historical_data['Capital Contribution'].iloc[0]
    
    print(f"Start price: ${start_price:.1f}")
    print(f"End price: ${end_price:.1f}")
    print(f"Shares purchased: {shares_purchased:.1f}")
    print(f"Return percentage: {return_percentage:.1f}%")
    print(f"Initial contribution: ${initial_contribution:.1f}")
    print(f"Total capital contribution: ${capital_contribution:.1f}")
    print(f"Total gained in returns: ${interest_gained:.1f}")

def plot_investment_growth(data):
    """
    Plot the capital contribution and interest gained over time.

    :param data: A DataFrame with the calculated investment details.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(data['Date'], data['Capital Contribution'], label="Capital Contribution", color="blue")
    plt.plot(data['Date'], data['Interest Gained'], label="Interest Gained", color="green")
    plt.fill_between(data['Date'], data['Capital Contribution'], data['Total Value'], color='lightgreen', alpha=0.3)
    
    plt.title("Investment Growth Over Time", fontsize=14)
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Value (USD)", fontsize=12)
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()
    
def parse_yaml():
    with open("invest-config.yaml", "r") as file:
        data = yaml.safe_load(file)
    
    experiments=data["experiments"]

    return experiments


def run_experiment(ticker_symbol, start_date, end_date, investment_amount, periodic_contribution):
    try:
        results = calculate_historical_returns(ticker_symbol, start_date, end_date, initial_contribution, periodic_contribution)
        plot_investment_growth(results)
        results.describe()
        print_returns(results)
    except ValueError as e:
        print(e)


experiments = parse_yaml()

for exp_key, exp_data in experiments.items():
    experiment_name = exp_key
    ticker_symbol=exp_data["ticker_symbol"]
    start_date=exp_data["start_date"]
    end_date=exp_data["end_date"]
    initial_contribution=exp_data["initial_contribution"]
    periodic_contribution=exp_data["periodic_contribution"]
    run_experiment(ticker_symbol, start_date, end_date, initial_contribution, periodic_contribution)
