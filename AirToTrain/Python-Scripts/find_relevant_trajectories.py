import os
import pandas as pd
import numpy as np

######################################################################################
# Find Trajectories from Airport to Train Station (both directions) in Shenzhen China#
######################################################################################


def load_csv_as_df(file_name, sub_directories, column_numbers=None, column_names=None):
    '''
    Load any csv as a pandas dataframe. Provide the filename, the subdirectories, and columns to read(if desired).
    '''
    base_path = os.getcwd()
    full_path = base_path + sub_directories + file_name

    if column_numbers is not None:
        df = pd.read_csv(full_path, usecols=column_numbers)
    else:
        df = pd.read_csv(full_path)

    if column_names is not None:
        df.columns = column_names

    return df


def lookup(s):
    """
    This is an extremely fast approach to datetime parsing.
    For large data, the same dates are often repeated. Rather than
    re-parse these, we store all unique dates, parse them, and
    use a lookup to convert all dates.
    """
    dates = {date: pd.to_datetime(date) for date in s.unique()}
    return s.map(dates)


def label_trajectories(df):
    updated_dfs = []
    taxi_ids = df['taxi_id'].unique()
    print('There are ', len(taxi_ids), ' unique taxi ids in this data')
    empty_route = -1
    trajectory_number = 1

    completed_count = 0

    for taxi_id in taxi_ids:
        # get the df for that taxis
        taxi_df = df.loc[df['taxi_id'] == taxi_id]
        taxi_df['time'] = lookup(taxi_df['time'])
        taxi_df.sort_values(by=['time'], inplace=True)

        passenger_got_in = False
        route_numbers = []
        route_starts = []
        route_ends = []

        for index, row in taxi_df.iterrows():
            passenger_in_taxi = row['occupancy_status']

            # Do we already have a passenger?
            if passenger_got_in:
                if passenger_in_taxi:
                    # trajectory still going
                    route_starts.append(False)
                    route_ends.append(False)
                    route_numbers.append(trajectory_number)
                    continue
                elif not passenger_in_taxi:
                    # trajectory ended
                    passenger_got_in = False
                    route_starts.append(False)
                    route_ends.append(True)
                    route_numbers.append(trajectory_number)
                    trajectory_number += 1

            elif passenger_in_taxi:
                passenger_got_in = True
                route_starts.append(True)
                route_ends.append(False)
                route_numbers.append(trajectory_number)

            else:
                route_starts.append(False)
                route_ends.append(False)
                route_numbers.append(empty_route)

        taxi_df['route_number'] = route_numbers
        taxi_df['route_start'] = route_starts
        taxi_df['route_end'] = route_ends
        updated_dfs.append(taxi_df)
        completed_count += 1

        if completed_count % 1000 == 0:
            print('Completed ', completed_count, ' taxi_ids out of ', len(taxi_ids))

    return pd.concat(updated_dfs)


def find_trajectories_at_airport_or_train(df):
    relevant_route_numbers = []
    relevant_cols = ['latitude', 'longitude', 'route_number', 'route_start']
    route_numbers = df.route_number.unique()

    number_of_trajectories = len(route_numbers) - 1

    for route_number in route_numbers:
        if route_number != -1:

            if route_number % 10000 == 0:
                print('On route number ', route_number, ' out of ', number_of_trajectories)
                print('Currently found ', len(relevant_route_numbers), ' relevant routes')

            start_row = df[relevant_cols][(df['route_start'] == True) & (df['route_number'] == route_number)]
            end_row = df[relevant_cols][(df['route_end'] == True) & (df['route_number'] == route_number)]

            # print(start_row)
            # print(end_row)

            start_lat = start_row['latitude'].iloc[0]
            start_long = start_row['longitude'].iloc[0]

            end_lat = end_row['latitude'].iloc[0]
            end_long = end_row['longitude'].iloc[0]

            if near_airport(start_lat, start_long) and near_train_station(end_lat, end_long):
                relevant_route_numbers.append(route_number)
            elif near_bus_station(start_lat, start_long) and near_train_station(end_lat, end_long):
                relevant_route_numbers.append(route_number)

    return relevant_route_numbers


def near_airport(lat, long):
    if 22.605770 <= lat <= 22.667089 and 113.784647 <= long <= 113.837340:
        return True
    else:
        return False


def near_bus_station(lat, long):
    if 22.567210 <= lat <= 22.568807 and 114.089676 <= long <= 114.091320:
        return True
    else:
        return False


def near_train_station(lat, long):
    if 22.604998 <= lat <= 22.614221 and 114.021111 <= long <= 114.034778:
        return True
    else:
        return False


def filter_data_by_gps(df, with_pass=False):
    # Airport in Shenzhen is 22.627078, 113.804928 and 22.606742, 113.827262.
    # Train Station in Shenzhen is 22.605502, 114.023724 and 22.613580, 114.034568.

    all_taxi_ids = df['taxi_id'].unique()
    print('There are ', len(all_taxi_ids), ' taxi ids in this dataset!')

    near_lat = df[(df['latitude'] >= 22.606742) & (df['latitude'] <= 22.627078)]
    print('There are ', len(near_lat), ' GPS readings near the latitude of the airport')

    near_airport = near_lat[(near_lat['longitude'] >= 113.804928) & (near_lat['longitude'] <= 113.827262)]

    print('There are ', len(near_airport), ' GPS readings near the airport!')
    taxi_ids = near_airport['taxi_id'].unique()
    print('There are ', len(taxi_ids), ' taxi ids near the airport!')

    if with_pass:
        with_pass = near_airport[near_airport['occupancy_status'] == 1]
        print('There are ', len(with_pass), ' GPS readings near the airport with a passenger!')
        with_pass_ids = with_pass['taxi_id'].unique()
        print('There are ', len(with_pass_ids), ' taxi ids near the airport with a passenger!')
        return with_pass
    else:
        return near_airport


def filter_data_by_train_gps(df, with_pass=False):
    # Train Station in Shenzhen is 22.605502, 114.023724 and 22.613580, 114.034568.
    all_taxi_ids = df['taxi_id'].unique()
    print('There are ', len(all_taxi_ids), ' taxi ids in this dataset!')

    near_lat = df[(df['latitude'] >= 22.605502) & (df['latitude'] <= 22.613580)]
    print('There are ', len(near_lat), ' GPS readings near the latitude of the airport')

    near_airport = near_lat[(near_lat['longitude'] >= 114.023724) & (near_lat['longitude'] <= 114.034568)]

    print('There are ', len(near_airport), ' GPS readings near the airport!')
    taxi_ids = near_airport['taxi_id'].unique()
    print('There are ', len(taxi_ids), ' taxi ids near the airport!')

    if with_pass:
        with_pass = near_airport[near_airport['occupancy_status'] == 1]
        print('There are ', len(with_pass), ' GPS readings near the airport with a passenger!')
        with_pass_ids = with_pass['taxi_id'].unique()
        print('There are ', len(with_pass_ids), ' taxi ids near the airport with a passenger!')
        return with_pass
    else:
        return near_airport


def get_taxi_data_near_airport_data(near_airport, full_df):
    taxi_ids = near_airport['taxi_id'].unique()

    relevant_taxis = full_df[full_df['taxi_id'].isin(taxi_ids)]

    return relevant_taxis


def label_trajectories(df):
    df['time'] = lookup(df['time'])
    updated_dfs = []
    taxi_ids = df['taxi_id'].unique()
    print('There are ', len(taxi_ids), ' in this data')
    empty_route = -1
    trajectory_number = 1

    completed_count = 0

    for taxi_id in taxi_ids[:10]:
        # get the df for that taxis
        taxi_df = df.loc[df['taxi_id'] == taxi_id]
        taxi_df.sort_values(by=['time'], inplace=True)
        passenger_got_in = False
        route_numbers = []
        route_starts = []
        route_ends = []

        for index, row in taxi_df.iterrows():
            passenger_in_taxi = row['occupancy_status']

            # Do we already have a passenger?
            if passenger_got_in:
                if passenger_in_taxi:
                    # trajectory still going
                    route_starts.append(False)
                    route_ends.append(False)
                    route_numbers.append(trajectory_number)
                    continue
                elif not passenger_in_taxi:
                    # trajectory ended
                    passenger_got_in = False
                    route_starts.append(False)
                    route_ends.append(True)
                    route_numbers.append(trajectory_number)
                    trajectory_number += 1

            elif passenger_in_taxi:
                passenger_got_in = True
                route_starts.append(True)
                route_ends.append(False)
                route_numbers.append(trajectory_number)

            else:
                route_starts.append(False)
                route_ends.append(False)
                route_numbers.append(empty_route)

        taxi_df['route_number'] = route_numbers
        taxi_df['route_start'] = route_starts
        taxi_df['route_end'] = route_ends
        updated_dfs.append(taxi_df)
        completed_count += 1

        if completed_count % 100 == 0:
            print('Completed ', completed_count, ' taxi_ids out of ', len(taxi_ids))

    return pd.concat(updated_dfs)



