import pandas as pd
import os


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


def label_trajectories(df, trajectory_number):
    df['time'] = lookup(df['time'])  # add time for sorting
    updated_dfs = []
    taxi_ids = df['taxi_id'].unique()
    print('There are ', len(taxi_ids), ' unique taxi ids in this data')

    empty_route = -1
    completed_count = 0

    for taxi_id in taxi_ids:
        # get the df for that taxi
        taxi_df = df.loc[df['taxi_id'] == taxi_id]
        taxi_df.sort_values(by=['time'], inplace=True)
        passenger_got_in = False

        route_numbers = []
        route_starts = []
        route_ends = []
        relevant_starts = []
        relevant_ends = []

        airport_starts = []
        airport_ends = []
        train_starts = []
        train_ends = []

        for index, row in taxi_df.iterrows():
            passenger_in_taxi = row['occupancy_status']

            # Do we already have a passenger?
            if passenger_got_in:
                if passenger_in_taxi:
                    # trajectory still going
                    route_starts.append(False)
                    route_ends.append(False)
                    relevant_ends.append(False)
                    relevant_starts.append(False)
                    train_starts.append(False)
                    airport_starts.append(False)
                    train_ends.append(False)
                    airport_ends.append(False)
                    route_numbers.append(trajectory_number)
                    continue
                elif not passenger_in_taxi:
                    # trajectory ended
                    passenger_got_in = False
                    route_starts.append(False)
                    route_ends.append(True)
                    route_numbers.append(trajectory_number)
                    trajectory_number += 1

                    # Is this relevant?
                    end_lat = row['latitude']
                    end_long = row['longitude']

                    if near_airport(end_lat, end_long) or near_train_station(end_lat, end_long):
                        relevant_ends.append(True)

                        if near_airport(end_lat, end_long):
                            airport_ends.append(True)
                            train_ends.append(False)
                        else:
                            airport_ends.append(False)
                            train_ends.append(True)

                    else:
                        relevant_ends.append(False)
                        airport_ends.append(False)
                        train_ends.append(False)

                    relevant_starts.append(False)
                    airport_starts.append(False)
                    train_starts.append(False)

            elif passenger_in_taxi:
                # someone just got in
                passenger_got_in = True
                route_starts.append(True)
                route_ends.append(False)
                route_numbers.append(trajectory_number)
                # is this relevant?

                start_lat = row['latitude']
                start_long = row['longitude']

                if near_airport(start_lat, start_long) or near_train_station(start_lat, start_long):
                    relevant_starts.append(True)

                    if near_airport(start_lat, start_long):
                        airport_starts.append(True)
                        train_starts.append(False)
                    else:
                        train_starts.append(True)
                        airport_starts.append(False)

                else:
                    relevant_starts.append(False)
                    airport_starts.append(False)
                    train_starts.append(False)

                relevant_ends.append(False)
                airport_ends.append(False)
                train_ends.append(False)

            else:
                # driving around without no passenger
                route_starts.append(False)
                route_ends.append(False)
                relevant_ends.append(False)
                relevant_starts.append(False)
                train_starts.append(False)
                airport_starts.append(False)
                train_ends.append(False)
                airport_ends.append(False)
                route_numbers.append(empty_route)

        taxi_df['route_number'] = route_numbers
        taxi_df['route_start'] = route_starts
        taxi_df['route_end'] = route_ends
        taxi_df['relevant_start'] = relevant_starts
        taxi_df['relevant_end'] = relevant_ends
        taxi_df['airport_start'] = airport_starts
        taxi_df['airport_end'] = airport_ends
        taxi_df['train_start'] = train_starts
        taxi_df['train_end'] = train_ends

        taxi_df = taxi_df[taxi_df.route_number != -1]
        updated_dfs.append(taxi_df)
        completed_count += 1

        if completed_count % 500 == 0:
            print('Completed ', completed_count, ' taxi_ids out of ', len(taxi_ids))

    print('Done mapping trajectories!')
    return pd.concat(updated_dfs), trajectory_number


def find_trajectories_at_airport_or_bus(df):
    # Test this method!
    air_to_bus_df = df[(df['airport_start'] == True) & (df['train_end'] == True)]
    bus_to_air_df = df[(df['train_start'] == True) & (df['airport_end'] == True)]

    relevant_air_to_bus_numbers = air_to_bus_df.route_number.unique()
    relevant_bus_to_air_numbers = bus_to_air_df.route_number.unique()

    route_numbers = relevant_air_to_bus_numbers + relevant_bus_to_air_numbers

    print('Found ', len(route_numbers), ' relevant routes!')

    return df[df['route_number'].isin(route_numbers)]


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


def load_data_and_find_relevant_routes(file_name, sub_directories, trajectory_number):
    col_numbers = [3, 4, 5, 6, 7, 8, 12]
    col_names = ['longitude', 'latitude', 'time', 'taxi_id', 'speed', 'direction', 'occupancy_status']

    df = load_csv_as_df(file_name, sub_directories, col_numbers, col_names)
    df, new_trajectory_number = label_trajectories(df, trajectory_number)

    labeled_file_name = file_name + '-With-Trajectories.csv'
    df.to_csv(labeled_file_name, encoding='utf-8')

    relevant_df = find_trajectories_at_airport_or_bus(df)
    csv_file_name = file_name + '.csv'

    relevant_df.to_csv(csv_file_name, encoding='utf-8')

    with open('RouteNumbers.txt', 'w') as f:
        f.write('%d' % new_trajectory_number)

    print('\n\n')
    print("###########################################################")
    print('Found ', len(relevant_df), ' relevant routes in ', file_name)
    print('Current Trajectory Number: ', new_trajectory_number)

    return relevant_df, new_trajectory_number


def load_all_data_from(folder_name, number_of_files):
    trajectory_number = 1
    base_file_name = 'part-m-'
    relevant_dfs = []

    for i in range(0, number_of_files):
    # for i in range(0, number_of_files):

        if i < 10:
            file_number = '0000' + str(i)
        else:
            file_number = '000' + str(i)

        file_name = base_file_name + file_number
        df, new_trajectory_number = load_data_and_find_relevant_routes(file_name, folder_name, trajectory_number)

        relevant_dfs.append(df)
        trajectory_number = new_trajectory_number

        print('new_trajectory_number: ', new_trajectory_number)

    return relevant_dfs


all_relevant_df_list = load_all_data_from('/2014-04-06/', 76)

dfs = pd.concat(all_relevant_df_list)
dfs.to_csv('RelevantTrajectories.csv', encoding='utf-8')
