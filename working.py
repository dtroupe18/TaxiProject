import pandas as pd


def label_trajectories(df):
    updated_dfs = []
    taxi_ids = df['taxi_id'].unique()
    print('There are ', len(taxi_ids), ' in this data')
    empty_route = -1
    trajectory_number = 1

    completed_count = 0

    for taxi_id in taxi_ids[:10]:
        # get the df for that taxis
        taxi_df = df.loc[df['taxi_id'] == taxi_id]
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


def find_trajectories_at_airport_or_bus(df):
    relevant_route_numbers = []
    relevant_cols = ['latitude', 'longitude', 'route_number', 'route_start']
    route_numbers = df.route_number.unique()

    number_of_trajectories = len(route_numbers) - 1

    for route_number in route_numbers:
        if route_number != -1:

            if route_number % 100 == 0:
                print('On route number ', route_number, ' out of ', number_of_trajectories)

            start_row = df[relevant_cols][(df['route_start'] == True) & (df['route_number'] == route_number)]
            end_row = df[relevant_cols][(df['route_end'] == True) & (df['route_number'] == route_number)]

            # print(start_row)
            # print(end_row)

            start_lat = start_row['latitude'].iloc[0]
            start_long = start_row['longitude'].iloc[0]

            end_lat = end_row['latitude'].iloc[0]
            end_long = end_row['longitude'].iloc[0]

            if near_airport(start_lat, start_long) and near_bus_station(end_lat, end_long):
                relevant_route_numbers.append(route_number)
            elif near_bus_station(start_lat, start_long) and near_airport(end_lat, end_long):
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


