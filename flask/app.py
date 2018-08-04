import os
import sys
paths = {
    'helpers': '/home/spadela/mids-w210-capstone'
}
for k,v in paths.items():
    sys.path.insert(0, v)
    
import requests
import pandas as pd
import numpy as np
import datetime
from copy import deepcopy
	
from bs4 import BeautifulSoup
from flask import Flask,render_template,json,Response,jsonify,request,url_for
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View

import argparse

### Set Up Mongo Connection
from db import dbToolsMongo
db = dbToolsMongo()

import time
import urllib.parse

app = Flask(__name__, static_folder='static')
Bootstrap(app)

nav = Nav()

@nav.navigation()
def mynavbar():
    return Navbar(
        'Decrypto',
        View('Upcoming ICOs', 'upcoming'),
        View('About', 'about')
    )

# ...

nav.init_app(app)

@app.route("/")
@app.route("/upcoming")
def upcoming():
	return render_template('upcoming.html')

@app.route("/upcoming2")
def upcoming2():
	return render_template('index.html')

@app.route("/_upcoming1")
def _upcoming1():
	df1 = db.toDF('sp_upcoming_summary_v2')
	df1 = df1[['symbol','name_url','hype_score','risk_score','owner_url','links','description','ico_start_date','ico_end_date','ico_sold_status','sparkline_example']]
	df1.columns = ['Symbol','ICO Name','Hype Score','Risk Score','Founder','Links','Description','Start Date','End Date','Status','Price History']
	df1.sort_values(by=['Symbol','Hype Score'],ascending=[False,False])
	return jsonify(df1.fillna('').to_dict(orient='records'))

# @app.route("/summary")
# def summary():
# 	return render_template('html/index.html')

# @app.route("/_summary_data1/limit/<int:limit>")
# def summary_data1(limit=0):
# 	# Select all records from icotracker table
# 	result = db['icotracker_ico'].find({})

# 	data = []
# 	for i,row in enumerate(result):
# 		data.append(row)
# 		# Add support for optional limit

# 		if limit != 0 and i >= limit:
# 			break
# 	df1 = pd.DataFrame(data)[['company_url','description','ico_dates','ico_sold_status','name','owner_name','owner_linkedin_profile','tracker_url','whitepaper','status']]
# 	df1['name_url'] = df1.apply(lambda x: str(x['name']) + '|' + '/detail/' + x['name'],axis=1)
# 	df1['owner_url'] = df1.apply(lambda x: str(x['owner_name']) + '|' + str(x['owner_linkedin_profile']),axis=1)
# 	def make_link(label,url):
# 		return "<a href='{url}'>{label}</url>".format(label=label,url=url)

# 	df1['links'] = df1.apply(lambda x: '<br/>'.join([make_link('URL',x['company_url']),make_link('Tracker',x['tracker_url']), \
# 		make_link('Whitepaper',x['whitepaper']),make_link('Reddit',x['status'])]),axis=1)

# 	df1['sparkline_example'] = df1.apply(lambda x: 'Jan-18:500, Feb-18:600, Mar-18:800',axis=1)
# 	df1 = df1[['name_url','owner_url','links','description','ico_dates','ico_sold_status','sparkline_example']]
# 	df1.columns = ['ICO Name','Founder','Links','Description','Key Dates','Status','Price History']
# 	return jsonify(df1.fillna('').to_dict(orient='records'))

@app.route("/detail/<string:name>")
def detail(name):
	# # select data about symbol
	# filters = {'name': name}
	# df1 = db.toDF('sp_price_history',filters)
	# dump to json
	# data1 = json.dumps(db.sql(sql,params).to_dict(orient='records'))
	# render template
	return render_template('detail.html',ico_name=name)

@app.route("/_detail/<string:name>")
def _detail1(name):
	filters = {'name': name}
	df1 = db.toDF('sp_upcoming_summary_v2',filters)
	df1 = df1[['symbol','name','hype_score','risk_score','sentiment_score','volatility_score','owner_url','links','description','ico_start_date','ico_end_date','ico_sold_status','bonus_details','twitter_followers','facebook_followers']]
	# df1.columns = ['Symbol','ICO Name','Hype Score','Risk Score','Sentiment Score','Volatilty Score,'Founder','Links','Description','Start Date','End Date','Status','Price History']
	return jsonify(df1.fillna('').to_dict(orient='records')[0])

@app.route("/about")
def about():
	return render_template('about.html')

@app.route("/similar/<string:name>")
def similar(name):
	# return data on similar Cryptos
	filters = {'name': name}
	df1 = db.toDF('sp_similar_icos',filters)
	return jsonify(df1.fillna('').to_dict(orient='records'))

if (__name__ == "__main__"):
	parser = argparse.ArgumentParser()
	parser.add_argument('--port',type=int,default=8010)
	args = parser.parse_args()
	app.run(port = args.port, debug = True, host = '0.0.0.0', passthrough_errors= True)