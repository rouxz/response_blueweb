# -*- coding: utf-8 -*-
##############################################################
#
#	  * Blueweb response time
#     * Fetch report of blueweb booking flow from json
#	  * export the report in csv
#
############################################################

#general libraries
import logging
import sys
from datetime import datetime
import getopt
import config as CONFIG
import json
import parse_reports
import export_model

def usage():
	print("Recognised options")
	print("-d, --debug set debug mode to ON")
	print("-h, --help show this help")
	print("-o FILE, --output FILE specify the file to be exported")
	print("-p PATH, --parse_path PATH parse the JSON included in the PATH folder")
	print("-s FILE, --scenario FILE provide a JSON file explaining the different steps of the scenario to be parsed")



def main(argv):
	
	global _debug 
	_debug = False
	
	
	# set all parameters according to command line
	# --------------------------------------------
	try:
		opts, args = getopt.getopt(argv, "hp:do:s:n:", ["help", "parse_path=", "debug", "output=", "scenario="])
	except getopt.GetoptError as err:
		print(err)
		usage()
		sys.exit(2)
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage()
			sys.exit()
		elif opt in ('-d', 'debug'):
			_debug = True
			print("Debug mode ON")
		elif opt in ("-p", "--parse_path"):
			imported_path = arg
		elif opt in ("-o, --output"):
			exported_file = arg
		elif opt in ("-s","--scenario"):
			scenario_json_path = arg
	

	
	#Logging setup
	#-------------
	if _debug :
		level = logging.DEBUG
	else:
		level = logging.INFO
	logging.basicConfig(filename='./log/blueweb-' + datetime.now().strftime("%y-%m-%d-%H-%M") +'.log', level=level)
	
	logging.info('Blueweb response time screening')
	print('Blueweb AF response time screening')
	print("##################################")
	logging.info("##################################")
	logging.info("")
	print("")
	
	
	# importing all necessary data
	# ----------------------------
	try:
		imported_path in locals()
	except:	
		imported_path = CONFIG.DEFAULT_IMPORT_FOLDER
	try:
		scenario_json_path in locals()
	except:
		scenario_json_path = CONFIG.DEFAULT_SCENARIO_PATH + CONFIG.DEFAULT_SCENARIO_NAME
		
		
	# retrieve scenario data from json
	try :
		scenario_json = json.load(open(scenario_json_path))
	except:
	#close program if we cannot load the scenario
		logging.info("Scenario file couldn't be loaded at :", scenario_json_path)
		print("Scenario file couldn't be loaded at :", scenario_json_path)
		return 2
	
	# info regarding our scenario
	scenario = {'name': scenario_json['name'], 'imported_path': imported_path, 'number_of_steps': scenario_json['number_of_steps'], 'matching_cases_dict': scenario_json['grouping'], 'export_name' : str.lower(scenario_json['export_name']) + "-" + datetime.now().strftime("%y-%m-%d") }
	
	
	#parse data from json
	#-------------------
	logging.info("parsing started")
	data = parse_reports.parse(scenario)
	logging.info("parsing done")
	
	#export to CSV
	#-------------
	try: 
	 exported_file in locals()
	except:
		exported_file = CONFIG.DEFAULT_EXPORT_PATH + scenario['export_name'] + "-" + datetime.now().strftime("%y-%m-%d") +'.csv'
		
	try:
		export_model.export(exported_file , data)
		logging.info("CSV exported as " + exported_file)
	except:
		logging.info("Scenario couldn't be stored at :", exported_file)
		print("Scenario couldn't be stored at :", exported_file)
		return 3
		
	return 0


if __name__ == "__main__":
	main(sys.argv[1:])