def load_csv_as_df(file_name, sub_directories, column_numbers=None, column_names=None):
    '''
    Load any csv as a pandas dataframe. Provide the filename, the subdirectories, and columns to read(if desired).
    '''
    # sub_directories = '/Data/'
    base_path = os.getcwd()
    full_path = base_path + sub_directories + file_name

    if column_numbers is not None:
        return pd.read_csv(full_path, usecols=column_numbers)

    # print('Full Path: ', full_path)
    # col_names = ['old_index', 'taxi_id', 'time', 'longitude', 'latitude', 'occupancy_status', 'speed', 'route_number', 'route_start', 'route_end']
    df = pd.read_csv(full_path)
    # df.columns = col_names
    # df.drop('old_index', axis=1, inplace=True)
    return df