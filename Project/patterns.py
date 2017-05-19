import pandas as pd
import datetime
import calendar
data = pd.read_csv("Lekagul Sensor Data.csv")
weekdays = []
for index, row in data.iterrows():
	timestamp = datetime.datetime.strptime(row['Timestamp'], "%Y-%m-%d %H:%M:%S")
	weekdays.append(calendar.day_name[timestamp.weekday()])
data['Weekday'] = weekdays
print data