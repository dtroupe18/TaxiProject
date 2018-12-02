import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import numpy as np
from itertools import cycle


def plot_route(df, route_number):
    route_data = df[df['route_number'] == route_number]

    long = route_data['longitude'].tolist()
    lat = route_data['latitude'].tolist()

    plt.plot(long, lat, color='r')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Route ' + str(route_number))
    plt.show()


def plot_all_routes_in(df):
    color_count = 1
    # cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
    colour_codes = map('C{}'.format, cycle(range(50)))
    route_numbers = df['route_number'].unique()

    for route_number in route_numbers:
        colour_code = next(colour_codes)
        route_data = df[df['route_number'] == route_number]

        long = route_data['longitude'].tolist()
        lat = route_data['latitude'].tolist()

        plt.plot(long, lat, color=colour_code)
        color_count += 1

    plt.show()





