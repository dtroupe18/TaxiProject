max_lat = 22.858081
min_lat = 22.444014

min_long = 113.749946
max_long = 114.628818

diff_in_latitude =  max_lat - min_lat
diff_in_longitude = max_long - min_long

# 15 rows so
cell_size = diff_in_latitude / 15.0

row_number = (22.746250 - min_lat)//cell_size
col_number = (114.026871 - min_long)//cell_size


def map_ending_to_box(latitude, longitude):
    row_number = int((latitude - min_lat) // cell_size)
    col_number = int((longitude - min_long) // cell_size)

    cell_number_str = str(row_number) + str(col_number)
    return int(cell_number_str)


def map_endings_to_cell(ends_df):
    # map all endings to a cell
    cells = []
    for index, row in ends_df.iterrows():
        lat = row['latitude']
        long = row['longitude']
        cell_number = map_ending_to_box(lat, long)
        cells.append(cell_number)
    ends_df['cell'] = cells

    return ends_df

def get_lat_for_row(row_number):
    return min_lat + (cell_size * row_number)
    # row_number = (x - min_lat) // cell_size