import csv
import datetime

def export(export_file, data):

	csv_file = open(export_file, 'w', newline='')
	writer = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	
	for step, (n, duration) in data.responseTime.items():
		writer.writerow([data.name, datetime.datetime.now(), step, n, duration])
		
	csv_file.close()