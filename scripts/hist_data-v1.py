import datetime
import pandas as pd
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.test
collection = db.frases

enddata = datetime.datetime.now() - datetime.timedelta(days=70)
startdata = enddata.replace(hour=0, minute=0, second=0, microsecond=0) - datetime.timedelta(days=14) #last 15 days

df = pd.DataFrame(list(collection.find({'published':{'$gte': startdata, '$lte': enddata}}, {'published': 1})))
df = df.set_index('published')
df.columns = ['count']
df = df.resample(rule = 'D', how= 'count')

data_hist = []
for row in df.to_csv().split('\n')[1:-1]:
    d = row.split(',')[0]
    d = datetime.datetime.strptime(d,'%Y-%m-%d')
    data_hist.append({'dataX':d.strftime('%d/%m'), 'dataY':int(row.split(',')[1])})

print(data_hist)