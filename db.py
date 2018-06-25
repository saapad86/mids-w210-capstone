from pymongo import MongoClient
from urllib.parse import quote_plus

def mongoConnect():
	params = {
		'username': quote_plus('w210_db_user'),
		'password': quote_plus('q1w2e3r4'),
		'url': '198.11.212.212:27017/w210_db'
	}
	conn = MongoClient('mongodb://{username}:{password}@{url}'.format(**params))
	return conn