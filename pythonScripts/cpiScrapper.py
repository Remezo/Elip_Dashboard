import requests
import json
import pandas as pd
import config
from IPython.display import JSON
import time
from openpyxl import load_workbook
import traceback
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool 


def make_api_request(series_id):
    """
    Makes an API request to retrieve data for the given series ID.

    Args:
    - series_id: The ID of the series to retrieve data for.

    Returns:
    - A dictionary containing the JSON response data.
    
    """

    headers = {
        'Content-type': 'application/json',
        'X-API-Key': config.API_KEY  # Replace 'config.API_KEY' with the actual variable or string containing your API key
    }

    data = json.dumps({"seriesid": series_id, "startyear": config.START_YEAR, "endyear": config.END_YEAR})
    response = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
    json_data = json.loads(response.text)
    
    
    return json_data

def process_raw_data(json_data):
    """
    Processes the raw data obtained from the API response.

    Args:
    - json_data: A dictionary containing the JSON response data.

    Returns:
    - A Pandas DataFrame containing the processed data.
    """
    results = json_data['Results']['series']
    table_data = {}

    for result in results:
        series_id = result['seriesID']
        series_data = result['data']

        for entry in series_data:
            period = entry['periodName'] + '-' + entry['year']
            value = float(entry['value'])
            table_data.setdefault(period, {})[series_id] = value

    
    df = pd.DataFrame.from_dict(table_data, orient='index')# Create a DataFrame from the table data
    df.index = pd.to_datetime(df.index, format='%B-%Y')# Convert the period column to datetime format and set it as the index
    item_codes_df = pd.read_csv(config.CPI_ItemCodes)    # Load the item codes from the CSV file
    item_names = item_codes_df.set_index('serie_id')['Item_Name'].to_dict()# Create a dictionary mapping series_id to item name
    df.rename(columns=item_names, inplace=True)# Replace the column names in the main DataFrame
    df.sort_index(ascending=True, inplace=True)# Sort the DataFrame by the period index in ascending order
    df.index = df.index.strftime('%b-%Y')

    return df





def calculate_percent_change():
    """
    Calculates the percent change for each item in the processed data.

    Returns:
    - A Pandas DataFrame containing the percent change values.
    """
    # Load the DataFrame from the Excel file
    df = pd.read_excel('output/CPI_Data.xlsx', sheet_name='Processed', index_col=0)

    # Calculate percent change for each column (item) going back one year
    for column in df.columns:
        df[column] = df[column].pct_change(periods=12).fillna(0)
        df[column] *= 100

    # Fill any remaining NaN values with 0
    df.fillna(0, inplace=True)
    # df = df.iloc[::-1]  # Reverse the order

    # Write the updated DataFrame to the same Excel file
    with pd.ExcelWriter('output/CPI_Data.xlsx', engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        df.to_excel(writer, sheet_name='percentChange')
        


def apply_weighted_transformation():
    """
    Applies a weighted transformation to the percent change data.

    The weighted transformation multiplies the percent change values by the relative importance
    of each item and saves the result in a new sheet.

    Returns:
    - None
    """
    
    df_percent_change = pd.read_excel('output/CPI_Data.xlsx', sheet_name='percentChange', index_col=0)# Load the DataFrame from the Excel file (Processed sheet)
    item_codes_df = pd.read_csv(config.CPI_ItemCodes)# Load the DataFrame with item names and relative importance

    
    item_importance = item_codes_df.set_index('Item_Name')['Relative_Importance'].to_dict()# Create a dictionary mapping item names to relative importance
    df_weighted_change = df_percent_change.mul(df_percent_change.columns.to_series().map(item_importance))# Multiply the percent change values by the relative importance
    df_weighted_change /= 100# Divide the weighted percent change values by 100
    threshold = 4
    df_cleaned = df_weighted_change.dropna(thresh=df_weighted_change.shape[1]-threshold+1).iloc[12:]


    # Save the cleaned DataFrame to an Excel file
 

    # Save the weighted percent change DataFrame to a new sheet named 'Weighted Change'
    with pd.ExcelWriter('output/CPI_Data.xlsx', engine='openpyxl', mode='a') as writer:
        df_cleaned.to_excel(writer, sheet_name='Weighted Change')
        

 
   





def excel_to_sql(excel_file):
    fred_sheets = pd.read_excel( excel_file, sheet_name = None)
    
    engine = create_engine('mysql://admin:Ascentris2023@database-1.cyoglzeje94r.us-east-1.rds.amazonaws.com/Ascentris_database', poolclass=NullPool )


    for table_name in fred_sheets.keys():
        if table_name == 'Weighted Change':
            fred_sheets[table_name].to_sql('CPIWeightedChange', if_exists="replace", con=engine)
    engine.dispose()	
	






def main():
    # Make API request
    series_df=pd.read_csv(config.CPI_ItemCodes)
    series_id=list(series_df['serie_id'])

    json_data = make_api_request(series_id)
    if json_data:
        print("API request successful.")
    else:
        print("API request failed.")
        return
    


    # Process raw data
    df_processed = process_raw_data(json_data)

    if not df_processed.empty:
        print("Data processing successful.")
    else:
        print("Data processing failed.")
        return
  

    # Write processed data to Excel
    df_processed.to_excel('output/CPI_Data.xlsx', sheet_name='Processed')
    
    print("Processed data saved to 'Processed' sheet in CPI_Data.xlsx.")



    # Calculate percent change
    calculate_percent_change()
    print("Percent change calculation successful.")


 
    apply_weighted_transformation()
    print("Weighted transformation successful.")

    
    excel_to_sql("output/CPI_Data.xlsx")
    
    print("All functions executed successfully and weighted change uploaded to the database")

# Execute the main function
if __name__ == "__main__":
    main()