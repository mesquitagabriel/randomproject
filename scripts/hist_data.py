import datetime
import pandas as pd
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.test
collection = db.frases

enddata = datetime.datetime.now() - datetime.timedelta(days=70)
startdata = enddata.replace(hour=0, minute=0, second=0, microsecond=0) - datetime.timedelta(days=2) #last 3 days

df = pd.DataFrame(columns=['data','count'])
for article in collection.find({'published':{'$gte': startdata, '$lte': enddata}}):
	df2 = pd.DataFrame([[article['published'], 1]], columns=['data','count'])
	df = df.append(df2)
df = df.set_index('data')
df = df.resample(rule = 'D', how = 'sum')

data_hist = []
for row in df.to_csv().split('\n')[1:-1]:
	d = row.split(',')[0]
	d = datetime.datetime.strptime(d,'%Y-%m-%d')
	data_hist.append({'dataX':d.strftime('%d/%m'), 'dataY':int(row.split(',')[1][0:-2])})

print(data_hist)
