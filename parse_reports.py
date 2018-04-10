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
	
	#create the parser according to the scenario needed with a dictionary loaded from json
	
	parser = ParserScenario(scenario['number_of_steps'], scenario['matching_cases_dict'])
	
	#parse each file of the input and add the result (a dict of step and duration ) the list scenarios
	for f in jsons:
		if CONFIG.DEBUG:
			print("Starting to parse " + str(f))
		logging.info("Starting to parse " + str(f))
		scenarios.append(parser.parse_file(f))
		logging.info("Parsing of " + str(f) + " done")
		if CONFIG.DEBUG:
			print("Parsing of " + str(f) + " done")

	
	
	# put the parsed scenarios into the datamodel
	for s in scenarios:
		for i, v in s.items():
			if (v >= -1):
				# No error 
				data.add_measurement(i, v)
			

	#print final result
	data.print()
	
	#return data model
	return data




class ParserScenario():
	""" a parser will parse a JSON Qcumber file and group steps according to matching cases dictionary"""
	def __init__(self, number_of_steps, matching_cases_dict):
		self.durations_of_steps = {}
		for i in range(1, number_of_steps + 1):
			self.durations_of_steps.update({"T" + str(i): -1})
		pass
	
		# self.matching_cases = json.load(open(matching_cases_dict))
		self.matching_cases = matching_cases_dict
		
	
	def parse_file(self, file):
		""" read data from within JSON file"""
		data = json.load(open(file))
	
		#reinitiate scenario dict to -1
		for k in self.durations_of_steps:
			self.durations_of_steps[k] = -1
	

		# We loop on the main data structre
		for el in data[0]['elements']:
			for step in el['steps']:
				#check if elements is identified and corresponding a case we want to track
				try:
					# do we have line info in the json element ?
					if 'line' in step:
						# Does this line correspond to something we want to track ?
						key = str(step['line'])
						if key in self.matching_cases:
							# found the step we are looking at
							actual_step = self.matching_cases[key]
							if actual_step in self.durations_of_steps:
								if step['result']['status'] == "passed":
									if CONFIG.DEBUG:
										print(actual_step + ": " + str(step['result']['duration']))
									if (self.durations_of_steps[actual_step] == -1):
										 # step not already logged
										self.durations_of_steps[actual_step] = step['result']['duration']
									elif self.durations_of_steps[actual_step] == -2:
										# there has been an issue on this step
										pass
									else:
										# add this substep to the actual step
										self.durations_of_steps[actual_step] += step['result']['duration']
								else:
									# One step has failed or skipped cannot do the data processing
									self.durations_of_steps[actual_step] == -2
						else:
							pass
				except Exception as e:
					print("Erreur " + str(e))
		return self.durations_of_steps