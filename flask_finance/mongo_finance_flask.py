from flask import Flask,render_template
from pymongo import MongoClient
from flask import jsonify
import json

app = Flask(__name__)

client = MongoClient('localhost',27017)
collectionES = client.test_database.tick_test 
collectionNL = client.test_database.tick_NL
collectionFR = client.test_database.tick_FR
collect_dic= {0:collectionES,1:collectionNL,2:collectionFR}

@app.route('/')
def home_page():
	return render_template('index.html')

@app.route('/finance/<date0>/', methods=['GET'])
def finance(date0):
	tick = collectionES
	output = []
	for s in tick.find({'date':date0}):
		output.append({'instrument':s['instrument'],'date':s['date'],'hms':s['hms'],
					'ask' : s['ask'], 'bid' : s['bid']})
	return jsonify({'finance': output})

@app.route('/<int:id>/<date0>/', methods=['GET'])
def eurusd(id,date0):
	tick = collect_dic[id]
	output = []
	for s in tick.find({'date':date0}):
		output.append({'instrument':s['instrument'],'date':s['date'],'hms':s['hms'],
					'ask' : s['ask'], 'bid' : s['bid']})
	return jsonify({'finance': output})

if __name__ == '__main__':
	app.run(debug=True)