import csv

from collections import defaultdict
from bs4 import BeautifulSoup
from functions import *
from graph import create_chart

# Starting url
url = 'https://www.otomoto.pl/osobowe/volkswagen/passat/od-2008/?search%5B\
filter_float_year%3Ato%5D=2008&search%5Bfilter_float_mileage%3Afrom%5D=150000\
&search%5Bfilter_float_mileage%3Ato%5D=200000&search%5Bbrand_program_id%5D%5B0\
%5D=&search%5Bcountry%5D='

filename = 'car_listings.csv'
headers = ['title', 'price', 'year', 'mileage', 'fuel']
fuel_types = ['Benzyna', 'Diesel', 'Benzyna+LPG']

# Add headers to the file
with open(filename, 'w') as f:
    writer = csv.writer(f)
    writer.writerow(headers)
f.close()

get_listings(url, filename)
mileages = get_mileage_ranges()

# Work with the created csv file
with open(filename) as f:
    reader = csv.reader(f)
    header_row = next(reader)

    data_lists = []
    for row in reader:
        data_lists.append([(int(row[1])), row[4], row[3]])

petrol_prices = []
diesel_prices = []
combo_prices = []
for data_list in data_lists:
    if data_list[1] == 'Benzyna':
        petrol_prices.append(data_list[0])
    elif data_list[1] == 'Diesel':
        diesel_prices.append(data_list[0])
    elif data_list[1] == 'Benzyna+LPG':
        combo_prices.append(data_list[0])
    else:
        pass

# Create a list of dictionaries for the graph to take in
keys = ['value', 'label']
averages = list(safe_div(petrol_prices, diesel_prices, combo_prices))
petrol_list = [averages[0], fuel_types[0]]
diesel_list = [averages[1], fuel_types[1]]
combo_list = [averages[2], fuel_types[2]]

dictList = []
dictList.append(dict(zip(keys, petrol_list)))
dictList.append(dict(zip(keys, diesel_list)))
dictList.append(dict(zip(keys, combo_list)))
print(dictList)

# Create chart
create_chart(dictList)

"""
Zmodyfikować wyciąganie średniej ceny, żeby poza rodzajem paliwa były też
kryteria takie jak np. średni przebieg w przedziałach co 10000km. Potem dodać
rozróżnienie modeli jeśli wyszukiwanie dotyczy więcej niż jednej marki auta.
"""
