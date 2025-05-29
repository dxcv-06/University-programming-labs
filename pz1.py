#!/usr/bin/env python3
"""
Euro Exchange Rate Analyzer - PZ 1
Retrieves Euro exchange rates from NBU API and displays data with charts
"""

import datetime as dt
import matplotlib.pyplot as plt
import pytz
import requests

def main() -> None:
    """Fetch and display Euro exchange rates for the previous week"""
    
    # Setup timezone and date range
    kyiv_tz = pytz.timezone("Europe/Kiev")
    current_time = dt.datetime.now(kyiv_tz)
    week_start = (current_time - dt.timedelta(days=7)).strftime("%Y%m%d")
    week_end = current_time.strftime("%Y%m%d")
    
    # Build API URL
    api_url = f"https://bank.gov.ua/NBU_Exchange/exchange_site?start={week_start}&end={week_end}&valcode=eur&json"
    
    # Fetch exchange data
    try:
        api_response = requests.get(api_url, timeout=30)
        api_response.raise_for_status()
        exchange_data = api_response.json()
    except requests.RequestException as error:
        print(f"Error fetching data: {error}")
        return
    except ValueError as error:
        print(f"Error parsing JSON: {error}")
        return
    
    # Check if data exists
    if not exchange_data:
        print("No data available for the given date range.")
        return
    
    # Display exchange rates with dates
    print("="*40)
    print("EURO TO UAH EXCHANGE RATES")
    print("="*40)
    for record in exchange_data:
        exchange_date = record["exchangedate"]
        exchange_rate = record["rate"]
        print(f"Date: {exchange_date} | Rate: {exchange_rate} UAH")
    print("="*40)
    
    # Prepare data for chart
    chart_dates = [dt.datetime.strptime(record["exchangedate"], "%d.%m.%Y").replace(tzinfo=kyiv_tz) 
                   for record in exchange_data]
    chart_rates = [record["rate"] for record in exchange_data]
    
    # Create and show chart
    plt.figure(figsize=(10, 6))
    plt.plot(chart_dates, chart_rates, marker="o", linestyle="-", color="purple", linewidth=2)
    plt.title("Euro to UAH Exchange Rate - Previous Week", fontsize=14, fontweight="bold")
    plt.xlabel("Date")
    plt.ylabel("Exchange Rate (UAH)")
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
