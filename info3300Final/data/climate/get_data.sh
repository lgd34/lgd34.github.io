#!/bin/bash
for number in {1956..2016}
do
curl "https://www.fema.gov/disasters/grid/year/csv/$number?field_disaster_type_term_tid_1=All&attach=page" -o "$number.csv"
done
exit 0
