import requests
import pandas as pd
import openpyxl
from openpyxl import load_workbook
import json
import numpy as np
import datetime
from datetime import timedelta
import holidays
import os
from pyquery import PyQuery as pq
import math
import sys
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool 
# import pymysql
# pymysql.install_as_MySQLdb()

np.set_printoptions(threshold=sys.maxsize)


path = os.getcwd()

def convert_yyyyq(dates):
	years = dates.values // 10
	months = (dates.values % 10) * 3 - 2
	date = [datetime.datetime(year=years[i], month=months[i], day=1) for i in range(0, len(years))]
	
	date = pd.to_datetime(date)
	return date.date

def pull_data(data):

	us_holidays = holidays.US(years=range(1940, pd.to_datetime("today").year)).keys()

	m = []
	q = []
	d = []
	y = []

	
	for i, row in data.iterrows():
		if (row.Frequency == "Monthly"):
			m.append(row.Data)
		elif (row.Frequency == "Daily" or row.Frequency == "Weekly"):
			d.append(row.Data)
		elif (row.Frequency == "Quarterly"):
			q.append(row.Data)
		else:
			y.append(row.Data)
	

	monthly = pd.DataFrame(columns=np.insert(m, 0, "Dates"))
	monthly["Dates"] = pd.date_range(start="01/01/1940", end=pd.to_datetime("today"), freq="MS").date

	weekmask = 'Mon Tue Wed Thu Fri'
	daily = pd.DataFrame(columns=np.insert(d, 0, "Dates"))
	daily["Dates"] = pd.bdate_range(start="01/01/1940", end=pd.to_datetime("today"), freq="C", weekmask=weekmask, holidays=us_holidays).date

	quarterly = pd.DataFrame(columns=np.insert(q, 0, "Dates"))
	quarterly["Dates"] = pd.bdate_range(start="01/01/1940", end=pd.to_datetime("today"), freq="QS").date

	count = 0
	for i, row in data.iterrows():
		
		pulled = False
		"""
		PULL DATA FROM SPECIFIC SOURCE
		"""
		if (row.Source == "FRED"):
			print("Retrieving %s from FRED" % row.Data)

			file = requests.get("https://api.stlouisfed.org/fred/series/observations?series_id={}&api_key={}&file_type={}".format(row.Data,"387a905393cc2ed7a711a24149359f52","json"))

			if file.status_code != 200:
				# This means something went wrong.
				print("ERROR ON %s" % row.Data)
				raise Exception('GET https://api.stlouisfed.org/fred/series/observations {}'.format(file.status_code))

			t = [i['date'] for i in file.json()['observations']]
			dates = pd.to_datetime([i['date'] for i in file.json()['observations']]).date
			values = np.array([i['value'] for i in file.json()['observations']])
			pulled = True			

		if (row.Source == "Yale"):
			print("Retrieving %s from Yale" % row.Data)

			yale_data_download = 0
			while(yale_data_download == 0):
				try:
					yale_data_download = requests.get("http://www.econ.yale.edu/~shiller/data/ie_data.xls")
				except requests.exceptions.ConnectionError:
					print("Error connecting to source, trying again")


			wb = open("Yale.xls", "wb")
			wb.write(yale_data_download.content)
			wb.close()

			yale = pd.read_excel("Yale.xls", sheet_name="Data", usecols="A,M", header=7).dropna()
			
			dates = pd.to_datetime([datetime.datetime.strptime(d, "%Y.%m") for d in yale["Date"].values.astype(str)]).date
			spl = np.round(yale["Date"].values % 1,2)
			mask = spl == 0.1
			dates[mask] = [d.month + 9 for d in dates[mask]]
			values = yale["CAPE"].to_numpy().astype(str)
			pulled = True


		"""
		ADD DATA TO DATAFRAME TO SAVE TO EXCEL LATER
		"""
		if (pulled):
			if (row.Frequency == "Monthly"):
				mask = monthly.Dates.isin(dates).values
				mask2 = np.isin(dates, monthly.Dates.values)
				monthly[row.Data].mask(mask, values[mask2], inplace=True)

			elif (row.Frequency == "Daily" or row.Frequency == "Weekly"):
				mask = daily.Dates.isin(dates).values
				mask2 = np.isin(dates, daily.Dates.values)
				daily[row.Data].mask(mask, values[mask2], inplace=True)

			elif (row.Frequency == "Quarterly"):
				mask = quarterly.Dates.isin(dates).values
				mask2 = np.isin(dates, quarterly.Dates.values)
				quarterly[row.Data].mask(mask, values[mask2], inplace=True)

			count += 1

	return daily, monthly, quarterly, count

def excel_to_sql(excel_file):

	fred_sheets = pd.read_excel( excel_file, sheet_name = None) # read all sheets
	# print(fred_sheets.keys())
	engine = create_engine('mysql://admin:Ascentris2023@database-1.cyoglzeje94r.us-east-1.rds.amazonaws.com/Ascentris_database', poolclass=NullPool )

	print(fred_sheets.keys())

	for table_name in fred_sheets.keys():
		fred_sheets[table_name].to_sql(f"raw_{table_name}", if_exists="replace", con=engine)
	
	engine.dispose()		
	

	
			



def run_fred_scrapper():

	# xls = pd.ExcelFile("DataSummary.xlsx")
	# data = pd.read_excel(xls, "Sheet1", usecols="B:F").dropna()
	data= pd.read_csv("/home/ubuntu/airflow/Elip_Dashboard/input/DataSummary.csv")
	# print(data)

	daily, monthly, quarterly, count = pull_data(data)
	#date = datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")
	#date = datetime.now().strftime("%Y_%m_%d_%M")
	
	
	# file_path="fred_scrapper_output.xlsx"
	file_path="/home/ubuntu/airflow/Elip_Dashboard/output/fred_scrapper_output.xlsx"
	
	



	with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
		daily.to_excel(writer, sheet_name="Daily")
		monthly.to_excel(writer, sheet_name="Monthly")
		quarterly.to_excel(writer, sheet_name="Quarterly")

	print("%d fields populated in output file, '%s'" % (count, file_path))
	excel_to_sql('/home/ubuntu/airflow/Elip_Dashboard/output/fred_scrapper_output.xlsx')
	print("Successfully added to the database")


if __name__ == '__main__':
	run_fred_scrapper()


#Login with username: admin  password: z352P7ZgGTSEGxvn
