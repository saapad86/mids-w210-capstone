import os
import sys
import pandas as pd
import numpy as np
from pymongo import MongoClient
from urllib.parse import quote_plus

class dbToolsMongo(object):
	def __init__(self):
		params = {
			'username': quote_plus('w210_db_user'),
			'password': quote_plus('q1w2e3r4$'),
			'url': '198.11.212.212:27017/w210_db'
		}
		self.conn = MongoClient('mongodb://{username}:{password}@{url}'.format(**params))
		self.db = self.conn.w210_db

	def toDF(self,collection,filters={}):
		result = self.db[collection].find(filters)

		data = []
		for i,row in enumerate(result):
		    data.append(row)
		return pd.DataFrame(data)