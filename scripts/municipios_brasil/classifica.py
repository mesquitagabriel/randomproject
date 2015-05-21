from pymongo import MongoClient
from bson.objectid import ObjectId
from collections import Counter

client = MongoClient('localhost', 27017)

db = client.test
collection = db.frases

db_municipios = client.municipios
municipios = db_municipios.municipios

article = collection.find({"_id" : ObjectId("5267d7826fc3c94fa629672b")})
def verifica(municipio, frase, idx):
	verf = True
	for idx2, palavra in enumerate(municipio['outros']):
		try:		
			if not palavra == frase[idx+idx2+1]:
				verf = False
		except Exception:
			verf = False
	return verf
def classifica(article):
	result = []
	article = list(article)[0]
	for frase in article['frases']:
		for idx, palavra in enumerate(frase):
			encontrados = list(municipios.find({ 'primeiro': palavra }))
			if encontrados:
				for municipio in encontrados:
					if not municipio['outros']:
						result.append(municipio['primeiro'])
					else:
						if verifica(municipio, frase, idx):
							result.append(' '.join([municipio['primeiro']]+municipio['outros']))
	return Counter(result).most_common()

print(classifica(article))
