import pandas as pd
import mpu
import os

######################################
# Add Distance and Duration to Routes#
######################################


def lookup(s):
    """
    This is an extremely fast approach to datetime parsing.
    For large data, the same dates are often repeated. Rather than
    re-parse these, we store all unique dates, parse them, and
    use a lookup to convert all dates.
    """
    dates = {date: pd.to_datetime(date) for date in s.unique()}
    return s.map(dates)


def calculate_route_durations(df):
    route_durations = {}
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

            if end_time < start_time:
                print('End time earlier than start time for route number ', route_id)
                print()

            route_duration = end_time - start_time
            # print('route_duration ', route_duration)

            duration_in_seconds = route_duration.total_seconds()

            print('Route ', route_id, ' duration in seconds ', duration_in_seconds)

            route_durations[route_id] = duration_in_seconds

    duration_df = pd.DataFrame(list(route_durations.items()), columns=['route_number', 'duration_in_seconds'])
    return duration_df


def distance_between_gps(gps_one, gps_two):
    km_distance = mpu.haversine_distance((gps_one[0], gps_one[1]), (gps_two[0], gps_two[1]))

    if km_distance < 0:
        print('got negative distance that\'s weak')
        km_distance *= -1

    return km_distance


def calculate_route_distances(df):
    route_distances = {}
    df['time'] = lookup(df['time'])
    route_ids = df['route_number'].unique()

    for route_id in route_ids:
        route_df = df[df['route_number'] == route_id]
        route_df.sort_values('time')
        route_df.reset_index(drop=True)

        distance_sum = 0.0
        is_first_row = True

        print('starting on route number', route_id)
        print(route_df.index)

        for index, row in route_df.iterrows():
            print('index', index)
            if not is_first_row:
                last_row = route_df.loc[index - 1]
                last_lat = last_row['latitude']
                last_long = last_row['longitude']
                last_gps = (last_lat, last_long)

                current_lat = row['latitude']
                current_long = row['longitude']
                current_gps = (current_lat, current_long)

                distance_between_rows = distance_between_gps(last_gps, current_gps)
                print('distance between rows', distance_between_rows)

                distance_sum += distance_between_rows
            else:
                is_first_row = False

        route_distances[route_id] = distance_sum

    distance_df = pd.DataFrame(list(route_distances.items()), columns=['route_number', 'distance_in_km'])
    return distance_df


def merge_distance_time_into_route_df(dt_df, df):
    route_dfs = []
    route_ids = df['route_number'].unique()

    for route_id in route_ids:
        route_df = df[df['route_number'] == route_id]
        distance_time_df = dt_df[dt_df['route_number'] == route_id]

        distance = distance_time_df['distance_in_km'].iloc[0]
        time = distance_time_df['duration_in_seconds'].iloc[0]

        route_df['distance_in_km'] = distance
        route_df['duration_in_seconds'] = time

        route_dfs.append(route_df)

    return pd.concat(route_dfs)


def reduce_dataframe_by_col(df, col_name):
    row_dfs = []
    unique_values = df[col_name].unique()

    for val in unique_values:
        val_df = df[df[col_name] == val]

        row_dfs.append(val_df.iloc[[0]])

    return pd.concat(row_dfs)


def load_google_map_dfs():
    column_names = ['latitude', 'longitude']
    file_names = ['BottomRoute.csv', 'MiddleRoute.csv', 'TopRoute.csv', 'TrainToAirMiddle.csv']
    base_path = os.getcwd()

    bottom_df = pd.read_csv(base_path + '/' + file_names[0])
    bottom_df.columns = column_names

    middle_df = pd.read_csv(base_path + '/' + file_names[1])
    middle_df.columns = column_names

    middle_df2 = pd.read_csv(base_path + '/' + file_names[3])
    middle_df2.columns = column_names

    top_df = pd.read_csv(base_path + '/' + file_names[2])
    top_df.columns = column_names

    return bottom_df, middle_df, middle_df2, top_df
