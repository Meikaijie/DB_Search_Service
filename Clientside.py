import requests

def main():
	url = None
	try:
		url = sys.argv[1]
	except:
		url = raw_input('please enter the API URL\n')
	requestREPL(url)

def requestREPL(url):
	while True:
		command = raw_input('please enter a command - add, search, or quit\n')
		command = " ".join(command.lower().split())
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
		elif command == "create table":
			tablename = raw_input('please enter a table name\n')
			columns = raw_input('please enter column names and column types in the format -\n name1:type1, name2:type2, etc.\n').split(",")
			response = requests.post(url+"/data/create",json=buildCreateDict(tablename,columns))
			print(response.text)
		###

		else:
			print("Invalid or empty command")
			print("Please start your request with add, search, or quit")
			print

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

if __name__ == "__main__":
	main()