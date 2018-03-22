from data_model import *
import logging
import json
import os
import config as CONFIG

def parse(scenario):
	
	
	logging.info("Parsing folder is " + str(scenario['imported_path']))
	
	#create a new data model
	data = ReportResponseTime(scenario['name'])
	
	#scenario to feed data model
	scenarios = []
	
	#iterate through the different elements of the path folder
	jsons = []
	for file in os.scandir(scenario['imported_path']):
		if file.name.endswith(".json") and file.is_file():
			jsons.append(file.path)
	
	logging.info(str(len(jsons)) + " files found ")
	
	#create the parser according to the scenario needed
	parser = ParserScenario(8, scenario['scenario_path'])
	
	for f in jsons:
		logging.info("Starting to parse " + str(f))
		scenarios.append(parser.parse_file(f))
		logging.info("Parsing of " + str(f) + " done")

	
	
	# put the parsed scenarios into the datamodel
	for s in scenarios:
		for i, v in s.items():
			data.add_measurement(i, v)
			

	#print final result
	data.print()
	
	#return data model
	return data




class ParserScenario():
	""" a parser will parse a JSON Qcumber file and group steps according to matching cases dictionary"""
	def __init__(self, number_of_steps, matching_cases_file):
		self.scenario = {}
		for i in range(1, number_of_steps + 1):
			self.scenario.update({"T" + str(i): -1})
		pass
	
		self.matching_cases = json.load(open(matching_cases_file))
	
	def parse_file(self, file):
		""" read data from within JSON file"""
		data = json.load(open(file))
	
		#reinitiate scenario dict to -1
		for k in self.scenario:
			self.scenario[k] = -1
	

		# We loop on the main data structre
		for el in data[0]['elements']:
			for step in el['steps']:
				#check if elements is identified and corresponding a case we want to track
				if 'name' in step and (step['name']+str(step['line'])) in self.matching_cases:
					actual_step = self.matching_cases[step['name']+str(step['line'])]
					if actual_step in self.scenario:
						if (self.scenario[actual_step] == -1):
							self.scenario[actual_step] = step['result']['duration']
						else:
							self.scenario[actual_step] += step['result']['duration']
				
		return self.scenario