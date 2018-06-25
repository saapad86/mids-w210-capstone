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

credentials = paths['user_dir'] + ".db/creds.json"
db = dbToolsRedshift(credentials=credentials)
db.connect(profile_name='cmh-redshift-analyst')
db.useConnection('cmh-redshift-analyst')

app = Flask(__name__)
Bootstrap(app)

@app.route("/")
@app.route("/summary")
def summary():
	return render_template('summary.html')

@app.route("/_summary_data1")
def summary_data1():
	# select data from db
	# df = sql
	# return jsonify(df1.to_dict(orient='records'))

@app.route("/campaign-reporting/detail/<int:symbol>")
def detail_data1(symbol):
	# select data about symbol
	db.reset()
	# dump to json
	data1 = json.dumps(db.sql(sql,params).to_dict(orient='records'))
	# render template
	return render_template('campaign-reporting-detail.html',data1=data1)

if (__name__ == "__main__"):
	parser = argparse.ArgumentParser()
	parser.add_argument('--port',type=int,default=7999)
	args = parser.parse_args()
	app.run(port = args.port, debug = True, host = '0.0.0.0', passthrough_errors= True)