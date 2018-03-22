from data_model import *
import logging
import json
import os

def parse(path):
	
	
	logging.info("Parsing folder is " + str(path))
	
	#create a new data model
	data = ReportResponseTime()
	
	#scenario to feed data model
	scenarios = []
	
	#iterate through the different elements of the path folder
	jsons = []
	for file in os.scandir(path):
		if file.name.endswith(".json") and file.is_file():
			jsons.append(file.path)
	
	logging.info(str(len(jsons)) + " files found ")
	
	for f in jsons:
		logging.info("Starting to parse " + str(f))
		parse_file(f)
	
	
	# for test 
	#scenario = {"T1" : 10, "T2": 5, "T3": 7}
	#scenarios = [scenario, scenario, scenario]
	
	#for s in scenarios:
	#	for i, v in s.items():
	#		data.add_measurement(i, v)
	#		
	#		
	#print final result
	#data.print()
	
	
	return data
	
	
def parse_file(file):
	""" read data from within JSON file"""
	data = json.load(open(file))
	
	scenario = {"T1" : -1, "T2": -1, "T3": -1, "T4": -1, "T5": -1, "T6":-1 , "T7": -1, "T8": -1}
	
	for el in data[0]['elements']:
		print(el['name'])
		for step in el['steps']:
			print(step['result']['duration'])
		