from flask import Flask, request
from urllib.parse import urlparse
import os
import psycopg2
app = Flask(__name__)

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

@app.route('/', methods=['POST'])
def requestHandler():
	return request.form['compound']

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)