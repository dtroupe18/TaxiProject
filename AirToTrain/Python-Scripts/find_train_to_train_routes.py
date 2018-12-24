import pandas as pd
import os
import mpu

"""
I used this file in combination with the Jupyter Notebook Find Train to Train Routes to locate routes between the north
and west train stations in Shenzhen China.
"""


def filter_data_by_gps(df, min_lat, max_lat, min_long, max_long, with_pass=False):
    """
    :param df: data-frame with latitude and longitude columns
    :param min_lat: minimum latitude value
    :param max_lat: max latitude value
    :param min_long: min longitude
    :param max_long: max longitude
    :param with_pass: required to have a passenger (occupancy_status column)
    :return: data-frame
    """

    all_taxi_ids = df['taxi_id'].unique()
    print('There are ', len(all_taxi_ids), ' taxi ids in this dataset!')

    near_lat = df[(df['latitude'] >= min_lat) & (df['latitude'] <= max_lat)] # 0.0203
    print('There are ', len(near_lat), ' GPS readings in your latitude range!')

    near_lat_and_long = near_lat[(near_lat['longitude'] >= min_long) & (near_lat['longitude'] <= max_long)] #0.022334

    print('There are ', len(near_lat_and_long), ' GPS readings in your latitude and longitude range!')
    taxi_ids = near_lat_and_long['taxi_id'].unique()
    print('There are ', len(taxi_ids), ' taxi ids in your latitude and longitude range!')

    if with_pass:
        with_pass = near_lat_and_long[near_lat_and_long['occupancy_status'] == 1]
        print('There are ', len(with_pass), ' GPS readings in your latitude and longitude range with a passenger!')
        with_pass_ids = with_pass['taxi_id'].unique()
        print('There are ', len(with_pass_ids), ' taxi ids in your latitude and longitude range with a passenger!')
        return with_pass
    else:
        return near_lat_and_long


# Shenzhen Train station west GPS 22.5316,113.903
df = pd.DataFrame()
train_station_west_gps = (22.5316, 113.903)
lat_diff = 0.025
long_diff = 0.025

near_west_train_df = filter_data_by_gps(df,
                                        train_station_west_gps[0] - lat_diff,
                                        train_station_west_gps[0] + lat_diff,
                                        train_station_west_gps[1] - long_diff,
                                        train_station_west_gps[1] + long_diff,
                                        with_pass=True)


train_station_north_gps_min = (22.605502, 114.023724)
train_station_north_gps_max = (22.613580, 114.034568)

near_north_train_df = filter_data_by_gps(df,
                                         train_station_north_gps_min[0],
                                         train_station_north_gps_max[0],
                                         train_station_north_gps_min[1],
                                         train_station_north_gps_max[1],
                                         with_pass=True)


def get_gps_records_with_taxi_id_in(taxi_id_list, df):
    return df[df['taxi_id'].isin(taxi_id_list)]


def find_column_intersection(df1, df2, col_name):
    """
    :param df1: data-frame
    :param df2: data-frame
    :param col_name: name of column
    :return: list of values in both columns
    """

    col_one_unique = df1[col_name].unique()
    col_two_unique = df2[col_name].unique()
    intersection = list(set(col_one_unique) & set(col_two_unique))

    return intersection


def get_rows_with_col_value_in(df, val_list, col_name):
    return df[df[col_name].isin(val_list)]


def load_google_map_dfs():
    base_path = os.getcwd()
    dfs = []
    column_names = ['latitude', 'longitude']

    file_names = ['North-Train-To-West-Left-Google-Maps-Route.csv',
                  'North-Train-To-West-Middle-Google-Maps-Route.csv',
                  'West-Train-To-North-Bottom-Google-Maps-Route.csv',
                  'West-Train-To-North-Middle-Google-Maps-Route.csv',
                  'West-Train-To-North-Top-Google-Maps-Route.csv'
                  ]

    for file_name in file_names:
        df = pd.read_csv(base_path + '/' + file_name)
        df.columns = column_names
        dfs.append(df)

    return dfs


def concat(row, col):
    return str(row) + '-' + str(col)


def map_gps_to_box(latitude, longitude):
    row_number = int((latitude - min_lat) // cell_size)
    col_number = int((longitude - min_long) // cell_size)

    if col_number < 0 or row_number < 0:
        return -1, -1, -1

    cell_number_str = str(row_number) + str(col_number)

    return concat(row_number, col_number), row_number, col_number


def map_gps_to_cell(df):
    cells = []
    rows = []
    cols = []

    for index, row in df.iterrows():
        lat = row['latitude']
        long = row['longitude']

        cell_number, cell_row, cell_col = map_gps_to_box(lat, long)

        cells.append(cell_number)
        cols.append(cell_col)
        rows.append(cell_row)

    df['cell'] = cells
    df['row'] = rows
    df['column'] = cols

    return df


def map_google_maps_routes_to_cells(df_list):
    with_cells = []
    for df in df_list:
        df = map_gps_to_cell(df)
        with_cells.append(df)
    return with_cells


def save_google_maps_routes_with_cells(route_df_list):
    file_names = ['North-Train-To-West-Left-Google-Maps-Route-Cells.csv',
                  'North-Train-To-West-Middle-Google-Maps-Route-Cells.csv',
                  'West-Train-To-North-Bottom-Google-Maps-Route-Cells.csv',
                  'West-Train-To-North-Middle-Google-Maps-Route-Cells.csv',
                  'West-Train-To-North-Top-Google-Maps-Route-Cells.csv'
                  ]

    for index, df in enumerate(route_df_list):
        df.to_csv(file_names[index], encoding='utf-8', index=False)

    return


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


def graph_all_routes_against_google_maps(df, google_maps_dfs, north_to_west=True):
    route_numbers = df['route_number'].unique()

    for route_number in route_numbers:
        if north_to_west:
            if route_number != 59994 and route_number != 572818:
                plot_title = 'North to West Train Route ' + str(route_number)
        else:
            plot_title = 'West to North Train Route ' + str(route_number)

        plot_suspected_fraud_vs_google_maps(google_maps_dfs, route_number, df, plot_title, show=False)

    print('Done creating route graphs!')
    return


# graph_all_routes_against_google_maps(air_df, [bottom_df, middle_air_train_df, top_df], north_to_west=True)


def find_routes_with_ten_readings(df, route_numbers, min_num_readings=10, verbose=False):
    routes = []

    for number in route_numbers:
        route_df = df[df['route_number'] == number]

        if len(route_df) >= min_num_readings:
            routes.append(route_df)
        elif verbose:
            print('Route: ', number, ' only has ', len(route_df), ' readings!')

    print('Found', len(routes), 'routes that have', min_num_readings, 'or more readings')

    return pd.concat(routes)


def lookup(s):
    """
    This is an extremely fast approach to datetime parsing.
    For large data, the same dates are often repeated. Rather than
    re-parse these, we store all unique dates, parse them, and
    use a lookup to convert all dates.
    """
    dates = {date: pd.to_datetime(date) for date in s.unique()}
    return s.map(dates)


def remove_routes_with_corrupt_start_end_times_and_calc_duration(df):
    route_durations = {}
    proper_route_numbers = []

    df['time'] = lookup(df['time'])
    route_ids = df['route_number'].unique()

    for route_id in route_ids:
        route_df = df[df['route_number'] == route_id]

        start_row = route_df[route_df['route_start'] == True]
        end_row = route_df[route_df['route_end'] == True]

        has_start_and_end = True
        if len(start_row) == 0:
            print('No start for route: ', route_id)
            has_start_and_end = False

        if len(end_row) == 0:
            print('No end for route: ', route_id)
            has_start_and_end = False

        if has_start_and_end:
            start_time = start_row['time'].iloc[0]
            end_time = end_row['time'].iloc[0]

            if start_time < end_time:
                route_duration = end_time - start_time
                duration_in_seconds = route_duration.total_seconds()
                route_durations[route_id] = duration_in_seconds
                proper_route_numbers.append(route_id)

    duration_df = pd.DataFrame(list(route_durations.items()), columns=['route_number', 'duration_in_seconds'])
    return duration_df, df[df['route_number'].isin(proper_route_numbers)]


def find_fraud_routes_by_time_distance(df, avg_time, avg_distance):
    return df[(df['distance_in_km'] >= avg_distance) & (df['duration_in_seconds'] >= avg_time)]


def distance_between_gps(gps_one, gps_two):
    # mpu.haversine_distance((lat1, lon1), (lat2, lon2))
    km_distance = mpu.haversine_distance((gps_one[0], gps_one[1]), (gps_two[0], gps_two[1]))

    if km_distance < 0:
        print('got negative distance that\'s weak')
        km_distance *= -1

    return km_distance


def remove_routes_with_excessive_distances(df):
    proper_route_numbers = []
    df['time'] = lookup(df['time'])
    route_ids = df['route_number'].unique()

    for route_id in route_ids:
        route_df = df[df['route_number'] == route_id]
        route_df.sort_values('time')
        route_df.reset_index(drop=True)

        distance_sum = 0.0
        is_first_row = True

        for index, row in route_df.iterrows():
            if not is_first_row:
                last_row = route_df.loc[index - 1]
                last_lat = last_row['latitude']
                last_long = last_row['longitude']
                last_gps = (last_lat, last_long)

                current_lat = row['latitude']
                current_long = row['longitude']
                current_gps = (current_lat, current_long)

                distance_between_rows = distance_between_gps(last_gps, current_gps)
                distance_sum += distance_between_rows
            else:
                is_first_row = False

        if distance_sum < 100:
            proper_route_numbers.append(route_id)
        else:
            print('Route ', route_id, ' has excessive distance: ', distance_sum)

    return df[df['route_number'].isin(proper_route_numbers)]


def get_suspected_fraud_by_time_distance(df, text_file_name):
    f = open(text_file_name, 'r')
    fraud_numbers = [line.rstrip() for line in f]
    print('Fraud numbers: ', fraud_numbers)
    f.close()

    return df[df['route_number'].isin(fraud_numbers)]



