import requests

active_url = "https://citrine-search-api.herokuapp.com"

def main():
	url = None
	try:
		url = sys.argv[1]
	except:
		url = raw_input('please enter the API URL\n')
	requestREPL(url)

# Interpreter loop for server testing and repeated commands
def requestREPL(url):
	while True:
		command = raw_input('please enter a command - add, search, or quit\n')
		command = "_".join(command.lower().split())
		if command == "quit":
			break
		raw_compound = raw_input('please enter a compound in the format - compound:compoundLogic - or nothing if a compound is not applicable to the request\n')
		raw_property = raw_input('please enter an optional list of properties of the form - propertyName1:value1:logic1, propertyName2:value2:logic2, etc.\n')
		property_list = raw_property.split(',')

		for i in range(len(property_list)):
			property_list[i] = "_".join(property_list[i].split())
		c = raw_compound.split(":")
		compound = c[0].strip()
		compound_logic = c[-1].strip()
		if len(c) < 2:
			compound_logic = ''

		if command == "add":
			if compound == '':
				print("A non-empty compound formula must be entered for an add request")
				continue
			response = requests.post(url+"/data/add",json=buildAddDict(compound,property_list))
			print(response.text)
		elif command == "search":
			response = requests.post(url+"/data/search",json=buildSearchDict(compound,compound_logic,property_list))
			print(response.json())

		### Extra commands go here
		elif command == "create_table":
			tablename = raw_input('please enter a table name\n')
			columns = raw_input('please enter column names and column types in the format -\n name1:type1, name2:type2, etc.\n').split(",")
			response = requests.post(url+"/data/create",json=buildCreateDict(tablename,columns))
			print(response.text)
		###

		else:
			print("Invalid or empty command")
			print("Please start your request with add, search, or quit")
			print

# Build and format dictionary using REPL input for add POST request in JSON format
# compound is a string representing the chemical formula
# property_list is a list of strings representing propertyName, propertyValue pairs delimited by ':'
def buildAddDict(compound, property_list):
	output = {}
	output["compound"] = compound
	proplist = []
	for prop in property_list:
		breakdown = prop.split(":")
		if len(breakdown)<2:
			print("skipping empty or improperly formatted property")
			continue
		innerdict = {}
		innerdict["propertyName"] = breakdown[0]
		innerdict["propertyValue"] = breakdown[1]
		proplist.append(innerdict)
	output["properties"] = proplist
	return output

# Send an add POST request to the server and return the response object
# compound is a string representing the chemical formula
# property_list is a list of string tuples containing propertyName and propertyValue pairs
def makeAddRequest(compound, property_list=[]):
	request = {}
	request["compound"] = compound
	proplist = []
	for prop in property_list:
		innerdict = {}
		innerdict["propertyName"] = "_".join(prop[0].split())
		innerdict["propertyValue"] = "_".join(prop[1].split())
		proplist.append(innerdict)
	request["properties"] = proplist
	return requests.post(active_url+"/data/add",json=request)


# Build and format dictionary using REPL input for search POST request in JSON format
# compound is a string representing the chemical formula
# property_list is a list of strings representing propertyName, propertyValue, propertyLogic triples delimited by ':'
def buildSearchDict(compound, compound_logic, property_list):
	output = {}
	output["compound"] = {"logic":compound_logic,"value":compound}
	proplist = []
	for prop in property_list:
		breakdown = prop.split(":")
		if len(breakdown)<3:
			print("skipping empty or improperly formatted property")
			continue
		innerdict = {}
		innerdict["propertyName"] = breakdown[0]
		innerdict["propertyValue"] = breakdown[1]
		innerdict["propertyLogic"] = breakdown[2]
		proplist.append(innerdict)
	output["properties"] = proplist
	return output

# Send a search POST request to the server and return the response object
# compound is a string representing the chemical formula
# compound_logic is a string representing the comparison logic
# property_list is a list of string tuples containing propertyName, propertyValue, and propertyLogic triples
def makeSearchRequest(compound, compound_logic, property_list=[]):
	request = {}
	request["compound"] = {"logic":compound_logic, "value":compound}
	proplist = []
	for prop in property_list:
		innerdict = {}
		innerdict["propertyName"] = "_".join(prop[0].split())
		innerdict["propertyValue"] = "_".join(prop[1].split())
		innerdict["propertyLogic"] = "_".join(prop[2].split())
		proplist.append(innerdict)
	request["properties"] = proplist
	return requests.post(active_url+"/data/search",json=request)


# Build and format dictionary using REPL input for create table POST request in JSON format
# tablename is a string
# columns is a list of strings representing columnName, columnType pairs delimited by ':'
def buildCreateDict(tablename, columns):
	output = {}
	output['tableName'] = tablename
	columnlist = []
	for column in columns:
		columnSplit = column.split(":")
		if len(columnSplit)<2:
			print("skipping empty or improperly formatted column")
		innerdict = {}
		innerdict["columnName"] = columnSplit[0]
		innerdict["columnType"] = columnSplit[1]
		columnlist.append(innerdict)
	output["columns"] = columnlist
	return output

# Send a create table POST request to the server and return the response object
# tablename is a string
# columns is a list of string tuples containing columnName, columnType pairs
def makeCreateRequest(tablename, columns):
	request = {}
	request['tableName'] = tablename
	columnlist = []
	for column in columns:
		innerdict = {}
		innerdict["columnName"] = column[0]
		innerdict["columnType"] = column[1]
		columnlist.append(innerdict)
	request["columns"] = columnlist
	return requests.post(active_url+"/data/create",json=request)

if __name__ == "__main__":
	main()