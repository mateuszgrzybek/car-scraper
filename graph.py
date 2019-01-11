import pygal
from pygal.style import LightColorizedStyle as LCS, RotateStyle as RS

def mileage_chart(car_name, mileage_keys, flat_petrol, flat_diesel, flat_combo):
    """Create a chart based on the calculated mileage range averages."""
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
    bar_chart.title = """Średnie ceny w zależności od przebiegu i paliwa.
                      Samochód: {}""".format(car_name)
    bar_chart.x_labels = mileage_keys
    bar_chart.add('Benzyna', flat_petrol)
    bar_chart.add('Diesel', flat_diesel)
    bar_chart.add('Benzyna+LPG', flat_combo)
    bar_chart.render_to_file('mileage_prices.svg')

def year_chart(car_name, year_keys, flat_petrol_y, flat_diesel_y, flat_combo_y,
               unique_years):
    """Create a chart based on the calculated yearly averages."""
    # Define the chart's style
    chart_style = RS('#F7B258', base_style=LCS)

    # Adjust the configuration of the chart
    config = pygal.Config()
    config.x_label_rotation = 45
    config.title_font_size = 24
    config.label_font_size = 12
    config.major_label_font_size = 16
    config.y_labels_major_every = 4

    if len(unique_years) >= 3:
        # Create the chart
        line_chart = pygal.Line(config, style=chart_style, show_legend=True)
        line_chart.title = """Średnie ceny w zależności od roku produkcji i paliwa.
                          Samochód: {}""".format(car_name)
        line_chart.x_labels = year_keys
        line_chart.add('Benzyna', flat_petrol_y)
        line_chart.add('Diesel', flat_diesel_y)
        line_chart.add('Benzyna+LPG', flat_combo_y)
        line_chart.render_to_file('year_prices.svg')

    else:
        bar_chart = pygal.Bar(config, style=chart_style, show_legend=True)
        bar_chart.title = """Średnie ceny w zależności od roku produkcji i paliwa.
                          Samochód: {}""".format(car_name)
        bar_chart.x_labels = year_keys
        bar_chart.add('Benzyna', flat_petrol_y)
        bar_chart.add('Diesel', flat_diesel_y)
        bar_chart.add('Benzyna+LPG', flat_combo_y)
        bar_chart.render_to_file('year_prices.svg')
