import csv
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.municipios
collection = db.municipios

with open('municipios_openstreet.csv', newline='') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',')
	for row in spamreader:
		i=0
		others=[]
		for word in row[1].split(' '):
			if i==0:
				first = word.lower()
				i=1
			else:
				others.append(word.lower())
		collection.insert({'primeiro': first, 'outros':others})
