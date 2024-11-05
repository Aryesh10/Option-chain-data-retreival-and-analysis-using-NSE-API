# NSE Options Chain Data Retrieval and Analysis

This script interacts with the National Stock Exchange of India (NSE) API to retrieve options chain data for specific instruments, filter data based on parameters like call/put options, and calculate margin requirements and premium earnings based on strike prices. The script includes two primary functions: one for fetching and processing options data and another for calculating financial metrics related to options trading.

## Prerequisites

Ensure that the required libraries are installed:
```bash
pip install requests pandas
```

### Dependencies
- `requests` - For handling HTTP requests to the NSE API.
- `pandas` - For structuring and analyzing the retrieved data
- `time` - For managing delay to avoid being blocked by the NSE server.

## Code Structure and Functionality

### 1. `get_option_chain_data_nse_json(instrument_name: str, side: str) -> pd.DataFrame`

**Function**: Retrieves options chain data for a specified instrument (e.g., "NIFTY") and option side (either "CE" for call or "PE" for put options) from the NSE API, processes it, and returns a DataFrame containing options information.

- **Assumptions**:
  - The NSE API is accessible, and appropriate headers are set to avoid being blocked.
  - The instrument name is a valid NSE symbol, and the side parameter is either "CE" or "PE".

- **How It Works**:
  - The function starts a `requests` session with headers to simulate a legitimate browser request.
  - A preliminary GET request to `https://www.nseindia.com` establishes session cookies.
  - The function then queries the NSE options chain API for the specified instrument name.
  - After receiving the JSON response, it iterates over records in `data['records']['data']`, filtering based on the provided option side (`CE` or `PE`).
  - Extracts fields like `strike_price` and the corresponding bid or ask price (based on `side`).
  - Finally, the function returns a `pandas` DataFrame, filtered to include only the highest bid/ask price for the specified side.

**Example API Response**:
```json
{
  "records": {
    "data": [
      {
        "CE": {
          "strikePrice": 17000,
          "bidPrice": 182.35,
          "askPrice": 183.5,
          "lastPrice": 182.75
        },
        "PE": {
          "strikePrice": 17000,
          "bidPrice": 192.0,
          "askPrice": 193.0,
          "lastPrice": 191.5
        }
      },
      {
        "CE": {
          "strikePrice": 17500,
          "bidPrice": 150.1,
          "askPrice": 150.75,
          "lastPrice": 150.25
        },
        "PE": {
          "strikePrice": 17500,
          "bidPrice": 195.5,
          "askPrice": 196.0,
          "lastPrice": 195.25
        }
      }
    ]
  }
}
```

**Data Processing Example**:
For `side="CE"`, the function filters out CE (Call Options) records, extracts the `strike_price` and `askPrice`, and identifies the highest `askPrice` across the DataFrame.

**Output DataFrame**:
| instrument_name | strike_price | side | bid/ask |
|-----------------|--------------|------|---------|
| NIFTY           | 17000        | CE   | 183.5   |

### 2. `calculate_margin_and_premium(data: pd.DataFrame, lot_size: int = 1) -> pd.DataFrame`

**Function**: Calculates margin requirements and premium earnings for each option based on the retrieved data.

- **Assumptions**:
  - The data parameter is a valid `DataFrame` containing `strike_price` and `bid/ask` columns.
  - The `lot_size` represents the number of contracts per lot (default is 1).

- **How It Works**:
  - For each option record, the function calculates a `margin_required` as 20% of the strike price (simulated margin rate).
  - Calculates `premium_earned` by multiplying the bid/ask price by the `lot_size`.
  - Appends these calculations to the `DataFrame` and returns it.

**Example Calculation**:
Given a `strike_price` of 17000, `bid/ask` of 183.5, and `lot_size` of 75:
  - `margin_required` = 17000 * 0.20 = 3400
  - `premium_earned` = 183.5 * 75 = 13762.5

**Output DataFrame**:
| instrument_name | strike_price | side | bid/ask | margin_required | premium_earned |
|-----------------|--------------|------|---------|-----------------|----------------|
| NIFTY           | 17000        | CE   | 183.5   | 3400            | 13762.5        |

### Example Usage

```python
# Fetch the option chain data for NIFTY call options (CE)
df = get_option_chain_data_nse_json("NIFTY", "CE")

# Calculate margin and premium for the options data with a specified lot size
df_with_calculations = calculate_margin_and_premium(df, lot_size=75)
print(df_with_calculations)
```

## Security and Usage Considerations

- **API Rate Limiting**: NSE may block requests if rate limits are exceeded. Implementing delays and avoiding frequent requests is recommended.
- **Data Validity**: Ensure the retrieved data structure matches expectations; NSE API may change structure over time.
- **Credentials**: NSE's API does not require credentials but may limit or block access for high-volume requests.

## AI Tools Used

- Used ChatGPT for refining the code and detecting errors
- Used ChatGPT for learning about the working of NSE api
- Used ChatGPT for refining my readme document
