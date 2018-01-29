from flask import Flask, request
from flask_restful import Resource, Api
from urllib.parse import urlparse
import os
import psycopg2

app = Flask(__name__)
api = Api(app)

def herokuDBConnect():
	# urlparse.uses_netloc.append("postgres")
	url = urlparse(os.environ["postgres://obhapecrmxysab:6cf517838bcdbf7f82915bcf05bbe4dca597e373cc1a055e54bba23dbcd1a779@ec2-54-225-103-255.compute-1.amazonaws.com:5432/df9d9q2tejj4e2"])
	conn = psycopg2.connect(
    	dbname=url.path[1:],
    	user=url.username,
    	password=url.password,
    	host=url.hostname,
    	port=url.port)
	return conn

# @app.route('/', methods=['POST'])
# def requestHandler():
# 	return "Received"

class AddHandler(Resource):
	def post(self):
		compound = request.json['compound']
		properties = request.json['properties']
		return "Add Received"

	def buildAddQuery(self):
		pass

class SearchHandler(Resource):
	def post(self):
		return "Search Received"

### Extra command handlers go here
class CreateHandler(Resource):
	def post(self):
		conn = herokuDBConnect()
		tablename = request.json['tableName']
		conn.execute("CREATE TABLE "+tablename)
		return {'status':'success'}
###

api.add_resource(AddHandler, '/data/add')
api.add_resource(SearchHandler, '/data/search')
api.add_resource(CreateHandler, '/data/create')

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)