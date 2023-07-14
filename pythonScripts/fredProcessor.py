import pandas as pd
import numpy as np
import openpyxl
import xlsxwriter
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool 


data_frames = {}

def read_data_summary(file_path):
    data_summary = pd.read_csv(file_path)
    return data_summary

def process_data(frequency, data, window_size, period):

    # if data=='TOTALSL':
    #     print(window_size, period, data) 
    
    try:
        data_frames[frequency][data] = pd.to_numeric(data_frames[frequency][data])
        if window_size and window_size!=0:
            data_frames[frequency][data]= data_frames[frequency][data].astype(float).rolling(int(window_size)).mean()
        elif period and period!=0:
            data_frames[frequency][data]= data_frames[frequency][data].astype(float).pct_change(periods=int(period), fill_method='ffill')
 
 
    except Exception as e:
        print(f"An error occurred for index {data}: {e}")



def excel_to_sql(excel_file):
    fred_sheets = pd.read_excel( excel_file, sheet_name = None)
    fred_sheets['Quarterly'].replace([np.inf, -np.inf], 0, inplace=True)
    engine = create_engine('mysql://admin:Ascentris2023@database-1.cyoglzeje94r.us-east-1.rds.amazonaws.com/Ascentris_database', poolclass=NullPool )


    for table_name in fred_sheets.keys():
        fred_sheets[table_name].to_sql(table_name, if_exists="replace", con=engine)
    engine.dispose()

    
     	
    
 
def run_fred_processor():
    # file_path_scrapper = "fred_scrapper_output.xlsx"
    file_path_scrapper=  "output/fred_scrapper_output.xlsx"

  

    data_frames["Daily"] = pd.read_excel(file_path_scrapper, sheet_name="Daily", index_col=False)  # Replace with your actual Daily data
    data_frames["Monthly"] = pd.read_excel(file_path_scrapper, sheet_name="Monthly", index_col=False)  # Replace with your actual Monthly data
    data_frames["Quarterly"] = pd.read_excel(file_path_scrapper, sheet_name="Quarterly", index_col=False)  # Replace with your actual Quarterly data

    data_summary = read_data_summary("input/DataSummary.csv")
    # print(data_summary)


    data_frames["Daily"]=data_frames["Daily"].dropna(thresh=4).replace('.', 0).drop('Unnamed: 0', axis=1).set_index('Dates')
    data_frames["Monthly"]=data_frames["Monthly"].dropna(thresh=16).replace('.', 0).drop('Unnamed: 0', axis=1).set_index('Dates')
    data_frames["Quarterly"]=data_frames["Quarterly"].dropna(thresh=15).replace('.', 0).drop('Unnamed: 0', axis=1).set_index('Dates')

    # test1=data_frames['Monthly']['CPIAUCSL'].astype(float).pct_change(periods=int(12), fill_method='ffill')
    # test1.to_csv("test1.csv")
    

    writer = pd.ExcelWriter("output/processed_data.xlsx", engine="xlsxwriter")


    # frequency="Monthly"
    # referenced_df=data_frames[frequency]
    
    # processed_df = process_data(referenced_df, 'CPIAUCSL', 0 , 12)



    for index, row in data_summary.iterrows():

        

        data = row['Data']
        window_size = row['Window_Size']
        period = row['Period']
        frequency = row['Frequency']
      
        process_data(frequency, data, window_size , period)
        print(f"Processing {data} variable")

      

    
    # Save each DataFrame separately
    data_frames["Daily"].to_excel(writer, sheet_name="Daily")
    data_frames["Monthly"].to_excel(writer, sheet_name="Monthly")
    data_frames["Quarterly"].to_excel(writer, sheet_name="Quarterly")

    writer.close()
    
    excel_to_sql('output/processed_data.xlsx')
    print("Successfully added processed data to the database")



if __name__ == "__main__":
    run_fred_processor()
