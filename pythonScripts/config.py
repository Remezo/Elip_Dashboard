import datetime


API_KEY="e04cd03600d84bcf8d7ca6e6028bb076"

END_YEAR = datetime.date.today().year # should be replaced by Datetime.Year function
START_YEAR = END_YEAR-9
INPUT_FOLDER = 'input/'
PROCESSED_DATA = 'output/processed_data.csv'
EXCEL_FILE="output/CPI Weighted.xlsm"
EXCEL_TAB="processed_data"
CPI_ItemCodes='/home/ubuntu/airflow/Elip_Dashboard/input/CPIitemCodes.csv'
Data_summary="/home/ubuntu/airflow/Elip_Dashboard/input/DataSummary.csv"

