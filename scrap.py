import csv
from collections import defaultdict

from bs4 import BeautifulSoup

from functions import *
from graph import create_chart

"""
As of now it's best to provide the script with a url that points to a certain
car (both make and model) that was being produced within a certain timespan.
This way the received data will be most accurate and will provide the user with
valuable info in the form of a chart.
The script should be provided with a simple url aquired by running any kind of
search query on 'https://www.otomoto.pl'.
"""
# Starting url
url = 'https://www.otomoto.pl/osobowe/mazda/cx-5/?search%5Bnew_used%5D=on'

filename = 'car_listings.csv'
headers = ['title', 'price', 'year', 'mileage', 'fuel']
fuel_types = ['Benzyna', 'Diesel', 'Benzyna+LPG']
mileage_keys = ['0-50k', '50-100k', '100-150k', '150-200k', '200-250k']

# Add headers to the file
with open(filename, 'w') as f:
    writer = csv.writer(f)
    writer.writerow(headers)
f.close()

get_listings(url, filename)

# Work with the created csv file
with open(filename) as f:
    reader = csv.reader(f)
    header_row = next(reader)

    data_lists = dict((key, []) for key in mileage_keys)

    for row in reader:
        if int(row[3]) in range(0, 50000):
            data_lists['0-50k'].append([(float(row[1])), row[4], row[3]])
        elif int(row[3]) in range(50000, 100000):
            data_lists['50-100k'].append([(float(row[1])), row[4], row[3]])
        elif int(row[3]) in range(100000, 150000):
            data_lists['100-150k'].append([(float(row[1])), row[4], row[3]])
        elif int(row[3]) in range(150000, 200000):
            data_lists['150-200k'].append([(float(row[1])), row[4], row[3]])
        else:
            data_lists['200-250k'].append([(float(row[1])), row[4], row[3]])

        car_name_raw = str(row[0]).split(' ')
        car_name = car_name_raw[0] + ' ' + car_name_raw[1]

petrol_prices = dict((key, []) for key in mileage_keys)
diesel_prices = dict((key, []) for key in mileage_keys)
combo_prices = dict((key, []) for key in mileage_keys)

for k,v in data_lists.items():
    for data_list in v:
        if data_list[1] == 'Benzyna':
            petrol_prices[k].append(data_list[0])
        elif data_list[1] == 'Diesel':
            diesel_prices[k].append(data_list[0])
        elif data_list[1] == 'Benzyna+LPG':
            combo_prices[k].append(data_list[0])
        else:
            pass

averages = list(averages(petrol_prices, diesel_prices, combo_prices))

# Extract separate dictionary values from the averages function and work with
# them to get a format readable by pygal (a list of floats/integers for each
# fuel type)
petrol_avgs = averages[0].values()
diesel_avgs = averages[1].values()
combo_avgs = averages[2].values()
flat_petrol = []
flat_diesel = []
flat_combo = []
for sublist in petrol_avgs:
    for item in sublist:
        flat_petrol.append(float(item))
for sublist in diesel_avgs:
    for item in sublist:
        flat_diesel.append(float(item))
for sublist in combo_avgs:
    for item in sublist:
        flat_combo.append(float(item))

# Create a pygal chart based on the aquired data
create_chart(car_name, mileage_keys, flat_petrol, flat_diesel, flat_combo)
