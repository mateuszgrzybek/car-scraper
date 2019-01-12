import csv
from contextlib import closing

from requests import get
from bs4 import NavigableString, BeautifulSoup


class CreateCsv():
    """Class that contains every necessary step to create a proper .csv file
    for the script to work on."""

    def __init__(self, headers, filename='car_listings.csv'):
        self.filename = filename
        self.headers = headers
        self.response = HTTPResponse()

    def create_csv_headers(self):
        """Creates .csv file headers as specified."""
        with open(self.filename, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(self.headers)
        f.close()

    def get_params(self, articles):
        """Iterates through all the items within the articles list and finds
        all desired parameters about each listing.
        """

        for article in articles:
            car = []
            try:
                title_container = article.find('a', class_='offer-title__link')
                title = title_container['title']
                car.append(title)

                pr_container = article.find('span',
                                            class_='offer-price__number')
                pr = [element for element in pr_container if
                      isinstance(element, NavigableString)]
                price = pr[0].strip()
                car.append(price.replace(' ', '').replace(',', '.'))

                year_container = article.find('li', {
                    'class': 'offer-item__params-item',
                    'data-code': 'year'})
                year = year_container.span.text.strip()
                car.append(year)

                mil_container = article.find('li', {
                    'class': 'offer-item__params-item',
                    'data-code': 'mileage'})
                mileage = mil_container.span.text
                car.append(int(mileage[:-3].replace(' ', '')))

                fuel_container = article.find('li', {
                    'class': 'offer-item__params-item',
                    'data-code': 'fuel_type'})
                fuel = fuel_container.span.text
                car.append(fuel)

                with open(self.filename, 'a') as f:
                    writer = csv.writer(f)
                    writer.writerow(car)
            except AttributeError:
                """In case one of the containers returns NoneType"""
                pass

    def get_listings(self):
        """Keeps getting all the listings starting from the given url."""

        soup = BeautifulSoup(self.response.get_url(), 'html.parser')
        articles = soup.find_all('article', class_='adListingItem')
        self.get_params(articles)
        print('Scraping the given url.')
        loop_count = 0

        while True:
            """Infinite loop that tries to find the next page's url and extract
            data from it. If the url variable appears to be NoneType (no url)
            break the loop due to an error.
            """
            try:
                next_url = soup.find('li', class_='next abs')
                url = next_url.a.get('href')
            except AttributeError:
                break

            if url:
                soup = BeautifulSoup(self.response.get_url(url), 'html.parser')
                articles = soup.find_all('article', class_='adListingItem')
                self.get_params(articles)
                loop_count += 1
                site_count = loop_count
                print('Scraping subsite: {}'.format(site_count))
            else:
                break
        print('Scraped the given url and {} subsites.'.format(loop_count))
        print('Total sites: {}'.format(loop_count + 1))

    def get_previous_listings(self):
        """Gets listings from previous pages if the provided url isn't the
        first page of search results.
        """

        loop_count = 0
        soup = BeautifulSoup(self.response.get_url(), 'html.parser')
        active_page = soup.find('li', class_='active')
        while True:
            """Infinite loop that tries to extract the previous page's url. If
            there's no url to be found (AttributeError due to NoneType) break
            the loop.
            """
            try:
                if active_page.text.strip() != 1:
                    previous_url = soup.find('li', class_='prev abs')
                    url = previous_url.a.get('href')
            except AttributeError:
                break

            if url:
                soup = BeautifulSoup(self.response.get_url(url), 'html.parser')
                articles = soup.find_all('article', class_='adListingItem')
                self.get_params(articles)
                loop_count += 1
                site_count = loop_count
                print('Scraping previous subsite: {}'.format(site_count))
            else:
                break

        if loop_count != 0:
            print('Scraped {} previous subsites.'.format(loop_count))


class HTTPResponse():
    """Class that checks whether the http response is fine and extracts the
    site's source code.
    """

    def get_url(self, url=input('Paste the url:\n>> ').strip()):
        """Requests the given url and returns it's content if the response is
        as expected. The method's default url is the one given by the user
        unless specified otherwise.
        """
        with closing(get(url, stream=True)) as response:
            if self.is_good_response(response):
                return response.text
            else:
                return None

    def is_good_response(self, response):
        """Returns True if status_code = 200 and the HTTP response appears to
        be HTML.
        """
        print('Status code:', response.status_code)
        return (response.status_code == 200,
                response.text.find('html'))
