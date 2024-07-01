import pytz
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from google.cloud import firestore
from solarpowermodel.solarpowermodel import SolarPowerModel
def fetch_electricity_prices():
    """
    Fetches the electricity prices from the Elexys website and returns as a DataFrame.
    
    Returns:
        pd.DataFrame: A DataFrame containing the electricity prices with timestamps.
    """
    # URL of the page to scrape
    url = 'https://my.elexys.be/MarketInformation/SpotBelpex.aspx'
    
    # Send a GET request to fetch the HTML content
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code != 200:
        raise Exception(f"Failed to fetch page content: {response.status_code}")
    
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the table with the data
    table = soup.find('table', {'id': 'contentPlaceHolder_belpexFilterGrid_DXMainTable'})
    
    # Debugging: Print the table to ensure it is found
    #print("Table found:", table is not None)
    #print("HTML content:", soup.prettify())
    
    # Return if table is not found
    #if table is None:
        #raise Exception("Failed to find the table in the HTML content")

    # Initialize lists to store the dates and prices
    datetimes = []
    prices = []
    
    rows = table.find_all('tr', class_='dxgvDataRow_Office2010Blue')
    if rows is None or len(rows) == 0:
        return "No data rows found in the table"
    
    for row in rows:
        cols = row.find_all('td', class_='dxgv')
        if len(cols) == 2:
            datetimes.append(cols[0].get_text(strip=True))
            prices.append(cols[1].get_text(strip=True))

    # Create a DataFrame
    df = pd.DataFrame({
        'DateTime': datetimes,
        'Price': prices
    })
    
    return df


"""
model=SolarPowerModel()
model.set_load_df()
model.set_belpex_df()
model.PV_generated_power_SPP()
model.power_flow()
model.dual_tariff()
model.dynamic_tariff()
model.get_grid_cost_total()
"""