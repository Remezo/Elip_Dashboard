import requests
import json
import pandas as pd
import pythonScripts.config as config
import time
from openpyxl import load_workbook
import traceback
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
import os


def make_api_request(series_id):
    """
    Makes an API request to retrieve data for the given series ID.
    """
    headers = {
        "Content-type": "application/json",
        "X-API-Key": config.API_KEY,
    }

    data = json.dumps({"seriesid": series_id, "startyear": config.START_YEAR, "endyear": config.END_YEAR})
    response = requests.post("https://api.bls.gov/publicAPI/v2/timeseries/data/", data=data, headers=headers)
    json_data = json.loads(response.text)

    return json_data


def process_raw_data(json_data):
    """
    Processes the raw data obtained from the API response.
    """
    results = json_data["Results"]["series"]
    table_data = {}

    for result in results:
        series_id = result["seriesID"]
        series_data = result["data"]

        for entry in series_data:
            period = entry["periodName"] + "-" + entry["year"]
            try:
                value = float(entry["value"])
            except (ValueError, TypeError):
                value = None
            table_data.setdefault(period, {})[series_id] = value

    df = pd.DataFrame.from_dict(table_data, orient="index")
    df.index = pd.to_datetime(df.index, format="%B-%Y")
    item_codes_df = pd.read_csv(config.CPI_ItemCodes)
    item_names = item_codes_df.set_index("serie_id")["Item_Name"].to_dict()
    df.rename(columns=item_names, inplace=True)
    df.sort_index(ascending=True, inplace=True)
    df.index = df.index.strftime("%b-%Y")

    return df


def calculate_percent_change():
    """
    Calculates the percent change for each item in the processed data.
    """
    cpi_path = os.path.join(config.OUTPUT_FOLDER, "CPI_Data.xlsx")
    df = pd.read_excel(cpi_path, sheet_name="Processed", index_col=0)

    for column in df.columns:
        df[column] = df[column].pct_change(periods=12).fillna(0)
        df[column] *= 100

    df.fillna(0, inplace=True)

    with pd.ExcelWriter(cpi_path, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
        df.to_excel(writer, sheet_name="percentChange")


def apply_weighted_transformation():
    """
    Applies a weighted transformation to the percent change data.
    """
    cpi_path = os.path.join(config.OUTPUT_FOLDER, "CPI_Data.xlsx")
    df_percent_change = pd.read_excel(cpi_path, sheet_name="percentChange", index_col=0)
    item_codes_df = pd.read_csv(config.CPI_ItemCodes)

    item_importance = item_codes_df.set_index("Item_Name")["Relative_Importance"].to_dict()
    df_weighted_change = df_percent_change.mul(df_percent_change.columns.to_series().map(item_importance))
    df_weighted_change /= 100
    threshold = 4
    df_cleaned = df_weighted_change.dropna(thresh=df_weighted_change.shape[1] - threshold + 1).iloc[12:]

    with pd.ExcelWriter(cpi_path, engine="openpyxl", mode="a") as writer:
        df_cleaned.to_excel(writer, sheet_name="Weighted Change")


def excel_to_sql(excel_file):
    fred_sheets = pd.read_excel(excel_file, sheet_name=None)
    conn_str = config.get_db_connection_string()
    engine = create_engine(conn_str, poolclass=NullPool)

    for table_name in fred_sheets.keys():
        if table_name == "Weighted Change":
            fred_sheets[table_name].to_sql("CPIWeightedChange", if_exists="replace", con=engine)
    engine.dispose()


def run_cpi_scrapper():
    series_df = pd.read_csv(config.CPI_ItemCodes)
    series_id = list(series_df["serie_id"])

    json_data = make_api_request(series_id)
    if json_data:
        print("API request successful.")
    else:
        print("API request failed.")
        return

    df_processed = process_raw_data(json_data)

    if not df_processed.empty:
        print("Data processing successful.")
    else:
        print("Data processing failed.")
        return

    cpi_path = os.path.join(config.OUTPUT_FOLDER, "CPI_Data.xlsx")
    df_processed.to_excel(cpi_path, sheet_name="Processed")
    print("Processed data saved to 'Processed' sheet in CPI_Data.xlsx.")

    calculate_percent_change()
    print("Percent change calculation successful.")

    apply_weighted_transformation()
    print("Weighted transformation successful.")

    excel_to_sql(cpi_path)
    print("All functions executed successfully and weighted change uploaded to the database")


if __name__ == "__main__":
    run_cpi_scrapper()
