# Compounds DB Search Service  
### Code Dependencies  
requests (2.18.4), psycopg2 (2.7.3.2), Flask (0.12.2), flask-restful (0.3.6)  
  
### Introduction/Overview  
This web API stores and gives users access to a database containing compounds and some of their recorded properties. Currently, there is only one table in the database holding meaningful information, 'comp_data'. The table has three columns - compound, band_gap, and color - and can be visualized as below:  
  
| compound | band_gap | color |
| -------- | -------- | ----- |
| Ga2Se3   | 2.05     | Red   |
| Ga2O3    | 4.4      | White |
| ...      | ...      | ...   |
  
The API is hosted on Heroku with the domains https://citrine-search-api.herokuapp.com/data/add, https://citrine-search-api.herokuapp.com/data/search, https://citrine-search-api.herokuapp.com/data/create, but can only be interacted with through POST requests.  
  
### File Descriptions  
Clientside.py - This file contains utility functions that make it easier for users to send properly formatted POST requests to the web API for adding or retrieving data. Additionally, it can be run from the command line/terminal with the command "python Clientside.py" to start a simple REPL that similarly aids users in interacting with the server.  
  
Procfile - This file describes what commands are run by my application's dynos on Heroku's platform.  
  
requirements.txt - Contains information regarding external dependencies so Heroku can install them.  
  
Serverside.py - This file contains server code that parses POST requests, queries the database, and then reformats the query results for the response.  
  
### Usage Guide/Examples  
Users can interact with the server in three ways - building and sending POST requests on their own, sending POST requests through the "make..." functions in Clientside.py, or sending POST requests through the REPL started by calling python Clientside.py.  
  
##### Raw Requests  
To add new data, construct a POST request with the JSON formatting below, and send it to https://citrine-search-api.herokuapp.com/data/add  
```
{
	"compound":formula, 
 	"properties":[
     {
		"propertyName":pName1,
		"propertyValue":pValue1
     },
     {
    	"propertyName":pName2,
    	"propertyValue":pValue2
     },
    ...
    ]
}
```  
For example -  
```
{
	"compound":"GaN, 
 	"properties":[
     {
		"propertyName":"band gap",
		"propertyValue":"3.4"
     }
    ]
}
```  

To search for records, construct a POST request with the JSON formatting below, and send it to https://citrine-search-api.herokuapp.com/data/search  
```
{
	"compound":{
		"logic": log,
		"value": formula
	}
	"properties":[
	 {
	 	"propertyName":pName1
	 	"propertyValue":pValue1
	 	"propertyLogic":pLogic1
	 },
	 {
	 	"propertyName":pName2
	 	"propertyValue":pValue2
	 	"propertyLogic":pLogic2
	 }
	]
}
```  
For example - 
```
{
	"compound":{
		"logic": "contains",
		"value": "Ga"
	}
	"properties":[
	 {
	 	"propertyName":"band gap"
	 	"propertyValue":"3.4"
	 	"propertyLogic":"gt"
	 },
	 {
	 	"propertyName":"color"
	 	"propertyValue":"White"
	 	"propertyLogic":"eq"
	 }
	]
}
```  
  
##### Importing Clientside functions  
To add new data, call the makeAddRequest() function as shown below
```python
import Clientside

response1 = Clientside.makeAddRequest('Ga2Se3',[('band gap','2.65'),('color','Yellow')])
print(response1.text)   # will print {'status':'success'}

response2 = Clientside.makeAddRequest('Ga2Se3',[('nonexistant column','whatever')])
print(response2.text)   # will print {'Error':'Invalid Query'} because there is no column 'nonexistant column'
```  
  
To search for records, call the makeSearchRequest() function as shown below
```python
import Clientside

response1 = Clientside.makeSearchRequest('Ga','contains',[('band gap','2.0','gt')])
print(response.json())  # will print search results in json format

response2 = Clientside.makeSearchRequest('Ga','nonsense',[])
print(response.json())  # will print {'Error':'Invalid Query'} because 'nonsense' is not a valid logical operator
```  
  
##### REPL
  
## Command Reference  













