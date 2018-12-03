import matplotlib.pyplot as plt
from itertools import cycle
from matplotlib.font_manager import FontProperties


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


def graph_google_map_routes(dfs, title, one_color=False, return_plot=False, label=None):
    """
    Graphs all routes in list of data frames where each df is one route
    :param dfs: list of dataframes
    :param title: String title for plot
    :param one_color: bool use the same color for all lines
    :return: plot
    """
    color_count = 1
    colour_codes = map('C{}'.format, cycle(range(50)))

    added_label = False

    for df in dfs:
        long = df['longitude'].tolist()
        lat = df['latitude'].tolist()
        colour_code = next(colour_codes)

        if one_color:
            if label is not None and not added_label:
                plt.plot(long, lat, color='g', label=label)
                added_label = True
            else:
                plt.plot(long, lat, color='g')
        else:
            plt.plot(long, lat, color=colour_code)
            color_count += 1

    plt.title(title)
    plt.xlabel('')
    plt.ylabel('')
    frame1 = plt.gca()
    frame1.axes.xaxis.set_ticklabels([])
    frame1.axes.yaxis.set_ticklabels([])

    if return_plot:
        return plt
    else:
        plt.savefig(title + '.png')
        plt.show()


def add_routes_to_plot(plot, df):
    route_numbers = df['route_number'].unique()

    for route_number in route_numbers:
        route_data = df[df['route_number'] == route_number]

        long = route_data['longitude'].tolist()
        lat = route_data['latitude'].tolist()

        plot.plot(long, lat, color='r')

    return plot


def add_route_to_plot(plot, route_df, color='r', label=None, verbose=False):
    long = route_df['longitude'].tolist()
    lat = route_df['latitude'].tolist()

    route_number = route_df['route_number'].unique()

    if verbose:
        print('Added route ', route_number[0], ' with color ', '\'', color, '\'')

    if label is not None:
        plot.plot(long, lat, color=color, label=label)
    else:
        plot.plot(long, lat, color=color)

    return plot


def plot_actual_routes_with_google_maps_routes(google_map_dfs, title, route_df):
    plot = graph_google_map_routes(google_map_dfs, title, one_color=True, return_plot=True)

    plot = add_routes_to_plot(plot, route_df)

    plot.savefig(title + '.png')
    plot.show()


def plot_suspected_fraud_vs_google_maps(google_map_dfs, route_number, df, title, show=True):
    plot = graph_google_map_routes(google_map_dfs, title, one_color=True, return_plot=True)

    route_df = df[df['route_number'] == route_number]
    print('Route ', route_number, ' has ', len(route_df), ' readings!')

    plot = add_route_to_plot(plot, route_df)
    plot.savefig(title + '.png')

    if show:
        plot.show()
    else:
        plot.clf()


def graph_all_routes_against_google_maps(df, google_maps_dfs, air_to_train=True):
    route_numbers = df['route_number'].unique()

    for route_number in route_numbers:
        if air_to_train:
            plot_title = 'Airport to Train Route ' + str(route_number)
        else:
            plot_title = 'Train to Airport Route ' + str(route_number)

        plot_suspected_fraud_vs_google_maps(google_maps_dfs, route_number, df, plot_title, show=False)

    print('Done creating route graphs!')
    return


def graph_everything_with_labels(df, google_maps_dfs, fraud_numbers, title, error_numbers=None, show_errors=False):
    # Graph Google Maps Routes (In Green)
    plot = graph_google_map_routes(google_maps_dfs, title, one_color=True, return_plot=True, label='Google Maps')

    # Add the rest of the routes
    route_numbers = df['route_number'].unique()

    # Add booleans for label
    added_fraud_label = False
    added_error_label = False
    added_normal_label = False

    for route_number in route_numbers:
        route_df = df[df['route_number'] == route_number]

        if route_number in fraud_numbers:
            # print()
            # print('Fraud added ', route_number)
            if not added_fraud_label:
                plot = add_route_to_plot(plot, route_df, color='r', label='Fraud')
                added_fraud_label = True
            else:
                plot = add_route_to_plot(plot, route_df, color='r')

        elif error_numbers is not None and route_number in error_numbers:
            if show_errors:
                if not added_error_label:
                    plot = add_route_to_plot(plot, route_df, color='y', label='Error')
                    added_error_label = True
                else:
                    plot = add_route_to_plot(plot, route_df, color='y')

        else:
            if not added_normal_label:
                # print()
                # print('Normal added ', route_number)
                plot = add_route_to_plot(plot, route_df, color='b', label='Normal')
                added_normal_label = True
            else:
                plot = add_route_to_plot(plot, route_df, color='b')

    plot.savefig(title + '.png')
    font_prop = FontProperties()
    font_prop.set_size('small')
    plot.legend(prop=font_prop)
    plot.show()
    return









