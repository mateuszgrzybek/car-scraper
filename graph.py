import pygal

def create_chart(dictList):
    """
    Create a chart based on the data extracted from the csv file
    """
    bar_chart = pygal.Bar()
    bar_chart.title = 'Ceny samochodu w PLN'
    bar_chart.x_labels = ['Benzyna', 'Diesel', 'Benzyna+LPG']
    bar_chart.add('Średnie ceny', dictList)
    bar_chart.render_to_file('car_prices.svg')
