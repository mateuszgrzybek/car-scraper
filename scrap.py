import csv
import webbrowser
import os
from collections import defaultdict

from functions import *
from graph import mileage_chart, year_chart

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

    mileage_keys = ['0-50k', '50-100k', '100-150k', '150-200k', '200-250k']
    mileage_lists = dict((key, []) for key in mileage_keys)
    years = []

    for row in reader:
        if int(row[3]) in range(0, 50000):
            mileage_lists['0-50k'].append([(float(row[1])), row[4], row[3],
                                         row[2]])
        elif int(row[3]) in range(50000, 100000):
            mileage_lists['50-100k'].append([(float(row[1])), row[4], row[3],
                                           row[2]])
        elif int(row[3]) in range(100000, 150000):
            mileage_lists['100-150k'].append([(float(row[1])), row[4], row[3],
                                            row[2]])
        elif int(row[3]) in range(150000, 200000):
            mileage_lists['150-200k'].append([(float(row[1])), row[4], row[3],
                                            row[2]])
        else:
            mileage_lists['200-250k'].append([(float(row[1])), row[4], row[3],
                                            row[2]])

        car_name_raw = str(row[0]).split(' ')
        car_name = car_name_raw[0] + ' ' + car_name_raw[1]
        years.append(int(row[2]))

year_keys = list(range(min(years, key=int), max(years, key=int)))
petrol_prices = dict((key, []) for key in mileage_keys)
diesel_prices = dict((key, []) for key in mileage_keys)
combo_prices = dict((key, []) for key in mileage_keys)
year_petrol = dict((key, []) for key in year_keys)
year_diesel = dict((key, []) for key in year_keys)
year_combo = dict((key, []) for key in year_keys)

for k,v in mileage_lists.items():
    for mileage_list in v:
        if mileage_list[1] == 'Benzyna':
            petrol_prices[k].append(mileage_list[0])
        elif mileage_list[1] == 'Diesel':
            diesel_prices[k].append(mileage_list[0])
        elif mileage_list[1] == 'Benzyna+LPG':
            combo_prices[k].append(mileage_list[0])
        else:
            pass
    for mileage_list in v:
        for year in year_keys:
            if mileage_list[3] == str(year) and mileage_list[1] == 'Benzyna':
                year_petrol[year].append(mileage_list[0])
            elif mileage_list[3] == str(year) and mileage_list[1] == 'Diesel':
                year_diesel[year].append(mileage_list[0])
            elif mileage_list[3] == str(year) and mileage_list[1] == 'Benzyna+LPG':
                year_combo[year].append(mileage_list[0])
            else:
                pass


mileage_averages = list(mileage_averages(petrol_prices, diesel_prices,
                                         combo_prices))
year_averages = list(year_averages(year_petrol, year_diesel, year_combo))

# Extract separate dictionary values from the averages function and work with
# them to get a format readable by pygal (a list of floats/integers for each
# fuel type)
petrol_avgs = mileage_averages[0].values()
diesel_avgs = mileage_averages[1].values()
combo_avgs = mileage_averages[2].values()
flat_petrol, flat_diesel, flat_combo = [], [], []
petrol_avgs_y = year_averages[0].values()
diesel_avgs_y = year_averages[1].values()
combo_avgs_y = year_averages[2].values()
flat_petrol_y, flat_diesel_y, flat_combo_y = [], [], []

for sub_1, sub_2, sub_3 in zip(petrol_avgs, diesel_avgs, combo_avgs):
    for item_1, item_2, item_3 in zip(sub_1, sub_2, sub_3):
        flat_petrol.append(float(item_1))
        flat_diesel.append(float(item_2))
        flat_combo.append(float(item_3))
for sub_1, sub_2, sub_3 in zip(petrol_avgs_y, diesel_avgs_y, combo_avgs_y):
    for item_1, item_2, item_3 in zip(sub_1, sub_2, sub_3):
        flat_petrol_y.append(float(item_1))
        flat_diesel_y.append(float(item_2))
        flat_combo_y.append(float(item_3))

# Create pygal charts based on the aquired data
mileage_chart(car_name, mileage_keys, flat_petrol, flat_diesel, flat_combo)
year_chart(car_name, year_keys, flat_petrol_y, flat_diesel_y, flat_combo_y)

webbrowser.open('file://' + os.path.realpath('mileage_prices.svg'))
webbrowser.open('file://' + os.path.realpath('year_prices.svg'))
