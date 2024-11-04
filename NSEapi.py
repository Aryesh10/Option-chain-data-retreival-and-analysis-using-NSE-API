import requests
import pandas as pd
import time

def get_option_chain_data_nse_json(instrument_name: str, side: str) -> pd.DataFrame:
    url = f"https://www.nseindia.com/api/option-chain-indices?symbol={instrument_name.upper()}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": f"https://www.nseindia.com/get-quotes/derivatives?symbol={instrument_name.upper()}",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "application/json, text/plain, */*",
        "Connection": "keep-alive"
    }

    # Start a session and set headers
    session = requests.Session()
    session.headers.update(headers)

    # Perform a preliminary GET request to establish session cookies
    session.get("https://www.nseindia.com", headers=headers)
    time.sleep(1)  # Add a short delay to avoid being blocked

    # Now make the actual request to the JSON API
    response = session.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()

    # Parse options data with checks for missing keys
    options_data = []
    for record in data['records']['data']:
        if side in record:
            option = record[side]
            print(record)  # Debug: Print the entire record to inspect the JSON structure
            strike_price = option.get('strikePrice', 0)
            # Try multiple keys for the price
            price = option.get('askPrice' if side == "CE" else 'bidPrice', option.get('lastPrice', 0))
            options_data.append({
                "instrument_name": instrument_name,
                "strike_price": strike_price,
                "side": side,
                "bid/ask": price
            })
    
    # Convert to DataFrame and find highest bid/ask
    df = pd.DataFrame(options_data)
    if not df.empty:
        max_price = df['bid/ask'].max()
        df = df[df['bid/ask'] == max_price]
    
    return df



def calculate_margin_and_premium(data: pd.DataFrame, lot_size: int = 1) -> pd.DataFrame:
    """
    Calculates the margin required and premium earned for each option in the DataFrame.
    
    Parameters:
    - data (pd.DataFrame): DataFrame containing option chain data with bid/ask prices.
    - lot_size (int): The lot size for each option contract (default is 1).
    
    Returns:
    - pd.DataFrame: DataFrame with additional columns for margin_required and premium_earned.
    """
    margins = []
    premiums = []
    
    # Simulated margin rate (example: 20% of strike price for demonstration)
    margin_rate = 0.20

    for _, row in data.iterrows():
        # Simulated margin calculation based on strike price and margin rate
        margin_required = row["strike_price"] * margin_rate
        margins.append(margin_required)
        
        # Calculate premium earned (bid/ask price * lot size)
        premium_earned = row["bid/ask"] * lot_size
        premiums.append(premium_earned)
    
    # Add calculated columns to DataFrame
    data["margin_required"] = margins
    data["premium_earned"] = premiums
    return data

# Example usage
df = get_option_chain_data_nse_json("NIFTY", "CE")
#print(df)
df_with_calculations = calculate_margin_and_premium(df, lot_size=75)  # Example lot size is 75
print(df_with_calculations)
