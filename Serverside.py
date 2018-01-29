from flask import Flask, request
from flask_restful import Resource, Api
from urllib.parse import urlparse
import os
import psycopg2

app = Flask(__name__)
api = Api(app)

def herokuDBConnect():
	urlparse.uses_netloc.append("postgres")
	url = urlparse.urlparse(os.environ["DATABASE_URL"])
	conn = psycopg2.connect(
    	database=url.path[1:],
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
		return "Add Received"

class SearchHandler(Resource):
	def post(self):
		return "Search Received"

api.add_resource(AddHandler, '/data/add')
api.add_resource(SearchHandler, '/data/search')

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)