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
		compound = None
		compound_logic = None
		compound_ind = None
		raw_request = raw_input('please enter a request of the form - \ncommand, compound:formula:logic, property1:value1:logic1, property2:value2:logic2, etc.\n')
		request_list = raw_request.split(',')
		if len(request_list) == 0:
			continue
		# Strip extra spaces
		for i in range(len(request_list)):
			request_list[i] = " ".join(request_list[i].split())
			if "compound" in request_list[i].lower():
				compound = request_list[i].split(":")[1].strip()
				compound_logic = request_list[i].split(":")[2].strip()
				compound_ind = i
		command = request_list[0]

		if command == "quit":
			break
		if not compound_ind is None:
			property_list = request_list[1:compound_ind] + request_list[compound_ind+1:]

		if command.lower() == "add":
			if compound is None:
				print("Compound entry missing")
				continue
			elif compound == '':
				print("A non-empty formula must be entered for an add request")
				continue
			response = requests.post(url+"/data/add",json=buildAddDict(compound,property_list))
			print(response.text)
		elif command.lower() == "search":
			response = requests.post(url+"/data/search",json=buildSearchDict(compound,compound_logic,property_list))
			print(response.text)

		### Extra commands go here
		elif command.lower() == "create table":
			tablename = raw_input('please enter a table name\n')
			columns = raw_input('please enter column name:column type pairs separated by commas\n').split(",")
			response = requests.post(url+"/data/create",json={"tableName":tablename, "columns":columns})
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
		innerdict = {}
		innerdict["propertyName"] = breakdown[0]
		innerdict["propertyValue"] = breakdown[1]
		innerdict["propertyLogic"] = breakdown[2]
	output["properties"] = proplist
	return output

if __name__ == "__main__":
	main()