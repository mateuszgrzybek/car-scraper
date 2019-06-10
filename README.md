# car-scraper
Web-scraping script that extracts data from a given url aquired by running a search query on 'https://www.otomoto.pl'.
After providing the script with a link, the script will scrape the given page and then look for the next page in the html code.
The loop runs for each consecutive page until the next url is nowhere to be found (the container returns NoneType).
After that, the script saves all the scraped data to a .csv file which is then used to create data structures necessary to
plot charts using pygal.
The repository contains three main .py files. The main file is 'scrap.py', which imports user-defined functions from
'functions.py' and 'graph.py'.

# Installation
Run:
```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```
Done. You can now run `python3 scrap.py` and let the scraper work.

# Requirements
All the packages required to run the script properly are defined in the requirements.txt file.

# Sample urls
* https://www.otomoto.pl/osobowe/volkswagen/passat/?search%5Bnew_used%5D=on
* https://www.otomoto.pl/osobowe/mazda/6/?search%5Bbrand_program_id%5D%5B0%5D=&search%5Bcountry%5D=
* https://www.otomoto.pl/osobowe/mercedes-benz/c-klasa/od-2008/?search%5Bbrand_program_id%5D%5B0%5D=&search%5Bcountry%5D=
