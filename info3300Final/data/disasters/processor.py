import csv

# List courtesy of http://stackoverflow.com/questions/32937610/python-dictionary-of-states
states = [
	'Alabama','Arizona','Arkansas','California','Colorado',
	'Connecticut','Delaware','Florida','Georgia','Idaho', 
	'Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana',
	'Maine','Maryland','Massachusetts','Michigan','Minnesota',
	'Mississippi', 'Missouri','Montana','Nebraska','Nevada',
	'New Hampshire','New Jersey','New Mexico','New York',
	'North Carolina','North Dakota','Ohio',    
	'Oklahoma','Oregon','Pennsylvania','Rhode Island',
	'South Carolina','South Dakota','Tennessee','Texas','Utah',
	'Vermont','Virginia','Washington','West Virginia',
	'Wisconsin','Wyoming'
]


def process_row(row):
	# Keep only the main 50 states
	if not row['State/Tribal Government'] in states:
		return False

	processed_row = row

	year = int(row['Date'][-2:])
	if year > 50:
		processed_row['Date'] = "19" + str(year)
	else:
		processed_row['Date'] = "20" + str(year).zfill(2)

	incident = processed_row['Incident Description'].lower()
	if "fire" in incident or "fire" in processed_row['Declaration Type'].lower():
		processed_row['Incident Description'] = "Fire"
	elif "winter" in incident or "ice" in incident or "snow" in incident or "blizzard" in incident or "freez" in incident:
		# Note - includes "severe cold temperatures", not necessarily directly associated with storm
		processed_row['Incident Description'] = "Winter Storm"
	elif "water shortage" in incident:
		processed_row['Incident Description'] = "Drought"
	elif "hurricane" in incident or "tropical" in incident or "typhoon" in incident:
		processed_row['Incident Description'] = "Tropical Storm"
	elif "flood" in incident or "tornado" in incident or "severe storm" in incident or "heavy rain" in incident:
		processed_row['Incident Description'] = "Severe Storm/Flooding"
	else:
		processed_row['Incident Description'] = "Other"

	# Rename the rows to be more concise/trim those we don't use
	processed_row['State'] = processed_row.pop('State/Tribal Government')
	del processed_row['Declaration Type']
	del processed_row['Number']

	return processed_row

if __name__ == '__main__':
	rows = []

	# 2017 is exclusive, 2016 inclusive
	for year in range(1956, 2017):
		with open(str(year) + '.csv') as csvfile:
			reader = csv.DictReader(csvfile)
			for row in reader:
				processed_row = process_row(row)
				if processed_row:
					rows.append(processed_row)

	with open('disasters.csv', 'w') as csvfile:
		# Specify field order
		fieldnames = ['Date', 'State', 'Incident Description']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

		writer.writeheader()
		for row in rows:
			writer.writerow(row)