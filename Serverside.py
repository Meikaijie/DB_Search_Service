import requests
import urlparse
import psycopg2

def dbConnect():
	urlparse.uses_netloc.append("postgres")
	url = urlparse.urlparse(os.environ["DATABASE_URL"])
	conn = psycopg2.connect(
    	database=url.path[1:],
    	user=url.username,
    	password=url.password,
    	host=url.hostname,
    	port=url.port)
	return conn

def main():
	pass

if __name__ == "__main__":
	main()