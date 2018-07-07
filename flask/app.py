import os
import sys
paths = {
	'dbtools': '/Users/saad.padela/notebooks/jupyterhub/spadela/dbtools/',
	'user_dir': '/Users/saad.padela/notebooks/jupyterhub/spadela/',
	'cra': '/home/spadela/jupyter-server/campaign-reporting-automation/'
}

for k,v in paths.items():
	sys.path.insert(0, v)

from flask import Flask,render_template,json,Response,jsonify,request,url_for
from flask_bootstrap import Bootstrap
import json
import argparse
import pandas as pd

import urllib.parse
from pymongo import MongoClient

username = urllib.parse.quote_plus('w210_db_user')
password = urllib.parse.quote_plus('q1w2e3r4$')
conn = MongoClient('mongodb://%s:%s@198.11.212.212:27017/w210_db' % (username, password))
db = conn.w210_db

app = Flask(__name__)
Bootstrap(app)

@app.route("/")
@app.route("/summary")
def summary():
	return render_template('summary.html')

@app.route("/_summary_data1")
def summary_data1():
	# Select all records from icotracker table
	result = db['icotracker_ico'].find({})

	data = []
	for i,row in enumerate(result):
		data.append(row)
	df1 = pd.DataFrame(data)[['company_url','description','ico_dates','ico_sold_status','name','owner_name','owner_linkedin_profile','tracker_url','whitepaper','status']]
	df1['name_url'] = df1.apply(lambda x: str(x['name']) + '|' + '/detail/' + x['name'],axis=1)
	df1['owner_url'] = df1.apply(lambda x: str(x['owner_name']) + '|' + str(x['owner_linkedin_profile']),axis=1)
	def make_link(label,url):
		return "<a href='{url}'>{label}</url>".format(label=label,url=url)

	df1['links'] = df1.apply(lambda x: '<br/>'.join([make_link('URL',x['company_url']),make_link('Tracker',x['tracker_url']), \
		make_link('Whitepaper',x['whitepaper']),make_link('Reddit',x['status'])]),axis=1)
	df1 = df1[['name_url','owner_url','links','description','ico_dates','ico_sold_status']]
	df1.columns = ['ICO Name','Founder','Links','Description','Key Dates','Status']
	return jsonify(df1.fillna('').to_dict(orient='records'))

@app.route("/campaign-reporting/detail/<string:name>")
def detail_data1(symbol):
	# select data about symbol
	db.reset()
	# dump to json
	data1 = json.dumps(db.sql(sql,params).to_dict(orient='records'))
	# render template
	return render_template('campaign-reporting-detail.html',data1=data1)

if (__name__ == "__main__"):
	parser = argparse.ArgumentParser()
	parser.add_argument('--port',type=int,default=8010)
	args = parser.parse_args()
	app.run(port = args.port, debug = True, host = '0.0.0.0', passthrough_errors= True)