import pandas as pd


max_lat = 23.0
min_lat = 22.0

min_long = 113
max_long = 115

diff_in_latitude = max_lat - min_lat
diff_in_longitude = max_long - min_long

# 20 rows so
cell_size = diff_in_latitude / 20.0


def concat(row, col):
    return str(row) + '-' + str(col)


def map_gps_to_box(latitude, longitude):
    row_number = int((latitude - min_lat) // cell_size)
    col_number = int((longitude - min_long) // cell_size)

    if col_number < 0 or row_number < 0:
        print('lat: ', latitude)
        print('long: ', longitude)
        print(int((latitude - min_lat)))
        print(int((longitude - min_long)))
        return -1, -1, -1

    # print(row_number)
    # print(col_number)

    # cell_number_str = str(row_number) + str(col_number)

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


def find_routes_with_ten_readings(df, route_numbers, min_num_readings=10):
    routes = []

    for number in route_numbers:
        route_df = df[df['route_number'] == number]

        if len(route_df) >= min_num_readings:
            routes.append(route_df)
        else:
            print('Route: ', number, ' only has ', len(route_df), ' readings!')

    print('Found ', len(routes), ' routes that have 10+ readings')

    return pd.concat(routes)

'''
bad_df = air_df[air_df['route_number'] == 157306]
bad_start = bad_df[bad_df['route_start'] == True]
bad_start.head()

bad_end = bad_df[bad_df['route_end'] == True]
bad_end.head()

air_df.drop(475, inplace=True)

'''