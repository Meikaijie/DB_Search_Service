# Compounds DB Search Service  
### Code Dependencies  
requests (2.18.4), psycopg2 (2.7.3.2), Flask (0.12.2), flask-restful (0.3.6)  
  
### Introduction/Overview  
This web API stores and gives users access to a database containing compounds and some of their recorded properties. The main functions offered to users are adding new rows to the database, and searching for specific records in the database. Currently, there is only one table in the database holding meaningful information, 'comp_data'. The table has three columns - compound, band_gap, and color - and can be visualized as below:  
  
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
  
#### Raw Requests  
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
  
#### Importing Clientside functions  
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
  
#### REPL  
To start the REPL, call python Clientside.py https://citrine-search-api.herokuapp.com, or just python Clientside.py. If an API URL is not provided the REPL will prompt the user for one, and https://citrine-search-api.herokuapp.com should be entered then.  
  
To add new data, enter the command 'add', the desired compound formula, and the desired property values when prompted. Below is an example of what proper execution should look like.  
```
please enter a command - add, search, or quit
add
please enter a compound in the format - compound:compoundLogic - or nothing if a compound is not applicable to the request
Ga2Se3
please enter an optional list of properties of the form - propertyName1:value1:logic1, propertyName2:value2:logic2, etc.
band gap:1, color:Brown
{"status" : "success"}
```  
  
To search for records, enter the command 'search', the desired compound formula and logic, and the desired property values and logic when prompted. Below is an example of what a proper execution should look like.  
```
please enter a command - add, search, or quit
search
please enter a compound in the format - compound:compoundLogic - or nothing if a compound is not applicable to the request
Ga:contains
please enter an optional list of properties of the form - propertyName1:value1:logic1, propertyName2:value2:logic2, etc.
band gap:2:gt, color:White:eq
{
	"results": [
	{
		"compound": "Ga2O3".
		"properties": [
			{
				"propertyName": "band_gap",
				"propertyValue": 4.4
			},
			{
				"propertyName": "color",
				"propertyValue": "White"
			}
		]
	}

	]
}
```
  
### Command/Database Reference  
##### Available REPL commands:  
add  
search  
quit  
##### Existing table columns:  
compound  
band_gap  
color  
##### Available Logical operators:  
contains (string/text only)  
eq  
gt (greater than, numeric only)  
lt (less than, numeric only)  
gte (greater than or equal, numeric only)  
lte(less than or equal, numeric only)  
not (goes in front of any other logical operator)  












