from decimal import Decimal
from flask import Flask, request
from flask_restful import Resource, Api
from psycopg2.extras import RealDictCursor
from urllib.parse import urlparse
import json
import os
import psycopg2

app = Flask(__name__)
api = Api(app)
active_table = "comp_data"

def herokuDBConnect():
	# urlparse.uses_netloc.append("postgres")
	url = urlparse(os.environ["DATABASE_URL"])
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
		conn = herokuDBConnect()
		cur = conn.cursor()
		# for dic in properties:
		# 	pname = dic["propertyName"]
		# 	pval = dic["propertyValue"]
		# 	cur.execute("IF COL_LENGTH('postgresql-spherical-79867.Compound_Data', '{0}') IS NOT NULL ")
		cur.execute(self.buildAddQuery(compound, properties))
		conn.commit()
		cur.close()
		conn.close()
		return {"status":"success"}

	def buildAddQuery(self, compound, properties):
		addQuery = "INSERT INTO "
		addQuery += active_table+" "
		columnString = "(compound"
		valueString = "('"+compound+"'"	
		for prop in properties:
			pname = prop["propertyName"]
			pval = prop["propertyValue"]
			try:
				pval = str(float(pval))
			except:
				pval = "'"+pval+"'"
			columnString += ", "+pname
			valueString += ", "+pval
		columnString += ")"
		valueString += ")"
		addQuery += columnString + " VALUES " + valueString + ";"
		return addQuery

class SearchHandler(Resource):
	def post(self):
		compound = request.json['compound']
		properties = request.json['properties']
		conn = herokuDBConnect()
		cur = conn.cursor(cursor_factory=RealDictCursor)
		cur.execute(self.buildSearchQuery(compound,properties))
		result = self.buildResultJson(cur.fetchall())
		cur.close()
		conn.close()
		return result

	def buildResultJson(self, result):
		cleanResult = []
		for row in result:
			tempdict = {}
			tempdict['compound'] = row['compound']
			properties = []
			for key in row:
				val = row[key]
				if key == 'compound':
					continue
				if type(val) == Decimal:
					val = float(val)
				properties.append({'propertyName':key,'propertyValue':val})
			tempdict['properties'] = properties
			cleanResult.append(tempdict)
		return json.dumps({'results':cleanResult},indent=2)

	def buildSearchQuery(self, compounddict, properties):
		searchQuery = "SELECT * FROM "+active_table+" WHERE "
		compound = compounddict['value']
		compoundlogic = compounddict['logic']
		compoundString = "compound "
		if compoundlogic.lower() == 'contains':
			compoundString += "LIKE '%{}%' ".format(compound)
		elif compoundlogic.lower() == 'not_contains':
			compoundString += "NOT LIKE '%{}%' ".format(compound)
		elif 'not_eq' in compoundlogic.lower():
			compoundString += "!= '{}' ".format(compound)
		elif 'eq' in compoundlogic.lower():
			compoundString += "= '{}' ".format(compound)
		elif compoundlogic == "":
			compoundString = "TRUE "
		searchQuery += compoundString
		for prop in properties:
			searchQuery += "AND "
			p = prop['propertyName']
			pval = prop['propertyValue']
			plog = prop['propertyLogic'].lower()
			propertyString = "{} ".format(p)
			if plog == 'contains':
				propertyString += "LIKE '%{}%' ".format(pval)
			elif plog == 'not_contains':
				propertyString += "NOT LIKE '%{}%' ".format(pval)
			elif 'not_eq' in plog:
				try:
					gate = float(pval)
					propertyString += "!= {} ".format(pval)
				except:
					propertyString += "!= '{}' ".format(pval)
			elif 'eq' in plog:
				try:
					gate = float(pval)
					propertyString += "= {} ".format(pval)
				except:
					propertyString += "= '{}' ".format(pval)
			elif plog == 'gt' or plog == 'not_lte':
				propertyString += "> {} ".format(pval)
			elif plog == 'lt' or plog == 'not_gte':
				propertyString += "< {} ".format(pval)
			elif plog == 'gte' or plog == 'not_lt':
				propertyString += ">= {} ".format(pval)
			elif plog == 'lte' or plog == 'not_gt':
				propertyString += "<= {} ".format(pval)
			searchQuery += propertyString
		return searchQuery[:-1]+";"





		# Possible logic: contains, eq, gt, lt, negation

### Extra command handlers go here
class CreateHandler(Resource):
	def post(self):
		tablename = request.json['tableName']
		columns = request.json['columns']
		columnString = "( "
		for column in columns:
			columnString += column['columnName']+" "+column['columnType']+","
		columnString = columnString[:-1] + ")"
		conn = herokuDBConnect()
		cur = conn.cursor()
		cur.execute("CREATE TABLE "+tablename+columnString)
		conn.commit()
		cur.close()
		conn.close()
		return {'status':'success'}
###

api.add_resource(AddHandler, '/data/add')
api.add_resource(SearchHandler, '/data/search')
api.add_resource(CreateHandler, '/data/create')

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)