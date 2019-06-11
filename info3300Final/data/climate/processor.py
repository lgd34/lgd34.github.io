import csv, os

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
	'Wisconsin','Wyoming',
]


def process_year(rows):
	new_row = dict()
	new_row['State'] = states[ int(rows[0]['StateCode']) - 1 ]
	new_row['Year'] = int(rows[0]['YearMonth'][3:7])

	total = 0
	for row in rows:
		total += float(row['   TAVG'])

	avg = total/12

	new_row['Avg Temperature Index'] = avg

	return new_row

if __name__ == '__main__':
	rows = []

	for filename in os.listdir("."):
	    if filename.endswith(".txt"): 
	        with open(filename) as csvfile:
	        	reader = csv.DictReader(csvfile)

	        	month_cntr = 0
	        	year_rows = []
	        	for row in reader:
	        		month_cntr += 1
	        		year_rows.append(row)

	        		if month_cntr == 12:
	        			rows.append(process_year(year_rows))
	        			month_cntr = 0
	    				year_rows = []

	with open('climate.csv', 'w') as csvfile:
		# Specify field order
		fieldnames = ['Year', 'State', 'Avg Temperature Index']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

		writer.writeheader()
		for row in rows:
			writer.writerow(row)