from flask import Flask, request
import urlparse
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
	print("Received")
	print(request.form)

def main():
	pass

if __name__ == "__main__":
	main()