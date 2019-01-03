import csv

from collections import defaultdict
from requests import get
from contextlib import closing
from bs4 import NavigableString, BeautifulSoup

def get_url(url):
    """
    Requests the given url and returns it's content if the response is as
    expected.
    """
    with closing(get(url, stream=True)) as response:
        if is_good_response(response):
            return response.text
        else:
            return None

def get_listings(url, filename):
    """
    Keeps getting all the listings starting from the given url
    """
    soup = BeautifulSoup(get_url(url), 'html.parser')
    articles = soup.find_all('article', class_='adListingItem')
    get_params(filename, articles)
    loop_count = 0
    print('Scraping the given url.')

    while True:
        """
        Infinite loop that tries to find the next page's url and extract data
        from it. If the url variable appears to be NoneType (no url) break the
        loop due to an error.
        """
        try:
            next_url = soup.find('li', class_='next abs')
            url = next_url.a.get('href')
        except AttributeError:
            break

        if url:
            soup = BeautifulSoup(get_url(url), 'html.parser')
            articles = soup.find_all('article', class_='adListingItem')
            get_params(filename, articles)
            loop_count += 1
            site_count = loop_count
            print('Scraping subsite: {}'.format(site_count))
        else:
            break
    print('Scraped the given url and {} subsites.'.format(loop_count))

def is_good_response(response):
    """
    Returns True if status_code = 200 and the HTTP response appears
    to be HTML.
    """
    print('Status code:', response.status_code)
    return(response.status_code == 200,
           response.text.find('html'))

def get_params(filename, articles):
    """
    Iterates through all the items within the articles list and finds
    all desired parameters about each listing.
    """
    for article in articles:
        car = []

        title_container = article.find('a', class_='offer-title__link')
        title = title_container['title']
        car.append(title)

        pr_container = article.find('span', class_='offer-price__number')
        pr = [element for element in pr_container if isinstance(element,
                NavigableString)]
        price = pr[0].strip()
        car.append(price.replace(' ', '').replace(',', '.'))

        year_container = article.find('li', {'class' : 'offer-item__params-item',
                                        'data-code' : 'year'})
        year = year_container.span.text.strip()
        car.append(year)

        mileage_container = article.find('li', {'class' : 'offer-item__params-item',
                                            'data-code' : 'mileage'})
        mileage = mileage_container.span.text
        car.append(int(mileage[:-3].replace(' ', '')))

        fuel_container = article.find('li', {'class' : 'offer-item__params-item',
                                        'data-code' : 'fuel_type'})
        fuel = fuel_container.span.text
        car.append(fuel)

        with open(filename, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(car)

def averages(petrol_prices, diesel_prices, combo_prices):
    """Calculates the average prices for each mileage range, additionaly
    depending on the fuel type, then puts them in the dictionaries"""
    avg_petrol = defaultdict(list)
    avg_diesel = defaultdict(list)
    avg_combo = defaultdict(list)
    for k, v in petrol_prices.items():
        if len(v) > 0:
            avg_petrol[k].append(format(sum(v)/len(v), '.2f'))
        else:
            avg_petrol[k].append(0)
    for k,v in diesel_prices.items():
        if len(v) > 0:
            avg_diesel[k].append(format(sum(v)/len(v), '.2f'))
        else:
            avg_diesel[k].append(0)
    for k,v in combo_prices.items():
        if len(v) > 0:
            avg_combo[k].append(format(sum(v)/len(v), '.2f'))
        else:
            avg_combo[k].append(0)
    return avg_petrol, avg_diesel, avg_combo

def safe_div(petrol_prices, diesel_prices, combo_prices):
    """Checks if attempt to divide by 0 will be made. If one is made (eg.
    one of the lists is empty), returns the corresponding value as 0.
    NO LONGER USED."""
    if len(petrol_prices) == 0:
        avg_petrol = 0
        return int(avg_petrol)
    elif len(diesel_prices) == 0:
        avg_diesel = 0
        return int(avg_diesel)
    elif len(combo_prices) == 0:
        avg_combo = 0
        return int(avg_combo)
    else:
        avg_petrol = format(sum(petrol_prices)/len(petrol_prices), '.2f')
        avg_diesel = format(sum(diesel_prices)/len(diesel_prices), '.2f')
        avg_combo = format(sum(combo_prices)/len(combo_prices), '.2f')
        return float(avg_petrol), float(avg_diesel), float(avg_combo)
        
def get_mileage_ranges(top=250000, step=50000):
    """
    Creates a list which contains a bunch of other lists, containing a 50000 km
    range each. Makes sense right? NOT USED.
    """
    mileages = []
    for i in range(0, top, step):
        mileage_range = (i, i+step)
        mileages.append(mileage_range)
    return mileages
