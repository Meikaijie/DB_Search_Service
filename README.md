# Materials DB Search Service  
## Code Dependencies  
requests (2.18.4), psycopg2 (2.7.3.2), Flask (0.12.2), flask-restful (0.3.6)  
  
## Introduction/Overview  
This web API stores and gives users access to a database containing compounds and some of their recorded properties. Currently, there is only one table in the database holding meaningful information, 'comp_data'. The table has three columns - compound, band_gap, and color - and can be visualized as below:  
  
| compound | band_gap | color |
| -------- | -------- | ----- |
| Ga2Se3   | 2.05     | Red   |
| Ga2O3    | 4.4      | White |
| ...      | ...      | ...   |
  
The API is hosted on Heroku with the domains https://citrine-search-api.herokuapp.com/data/add, https://citrine-search-api.herokuapp.com/data/search, https://citrine-search-api.herokuapp.com/data/create, but can only be interacted with through POST requests.  
  
## File Descriptions  
Clientside.py - This file contains utility functions that make it easier for users to send properly formatted POST requests to the web API for adding or retrieving data. Additionally, it can be run from the command line/terminal with the command "python Clientside.py" to start a simple REPL that similarly aids users in interacting with the server.  
  
Procfile - This file describes what commands are run by my application's dynos on Heroku's platform.  
  
requirements.txt - Contains information regarding external dependencies so Heroku can install them.  
  
Serverside.py - This file contains server code that parses POST requests, queries the database, and then reformats the query results for the response.  
  
## Example Usage  

  
## Command Reference