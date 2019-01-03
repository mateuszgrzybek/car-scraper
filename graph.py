import pygal
from pygal.style import LightColorizedStyle as LCS, RotateStyle as RS

def create_chart(car_name, mileage_keys, flat_petrol, flat_diesel, flat_combo):
    """
    Create a chart based on the data extracted from the csv file
    """
    # Define the chart's style
    chart_style = RS('#97C9F2', base_style=LCS)

    # Adjust the configuration of the chart
    config = pygal.Config()
    config.x_label_rotation = 45
    config.title_font_size = 24
    config.label_font_size = 12
    config.major_label_font_size = 16
    config.y_labels_major_every = 4

    # Create the chart
    bar_chart = pygal.Bar(config, style=chart_style, show_legend=True)
    bar_chart.title = """Średnie ceny w zależności od przebiegu.
                      Samochód: {}""".format(car_name)
    bar_chart.x_labels = mileage_keys
    bar_chart.add('Benzyna', flat_petrol)
    bar_chart.add('Diesel', flat_diesel)
    bar_chart.add('Benzyna+LPG', flat_combo)
    bar_chart.render_to_file('car_prices.svg')
