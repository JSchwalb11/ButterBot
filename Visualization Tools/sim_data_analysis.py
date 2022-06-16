import os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

def remove_empty_columns(df):
    for key in df.keys():
        if df[key].isnull().all() == True:
            df.drop(key, inplace=True, axis=1)

    for row in df.iterrows():
        if row[1].isnull().all() == True:
            df.drop(row[0], inplace=True, axis=0)

def separate_drone_times(df):
    drone_dict = dict() # new df

    for key in df.keys():
        if key.find("Drone") > -1:
            drone_dict[key] = df[key]
            df.drop(key, inplace=True, axis=1)

        elif key.find("Hostage") > -1:
            #df2[key] = df[key]
            #df.drop(key, inplace=True, axis=1)
            pass

        else:
            drone_dict[key] = df[key]

    drone_df = pd.DataFrame(drone_dict)

    return df, drone_df

def replace_nan_with_zero(df):
    keys = df.keys()
    np_arr = df.values
    new_arr = np.zeros_like(df.values)

    for i in range(0, np_arr.shape[0]):
        for j in range(0, np_arr.shape[1]):
            if j >= 2:
                try:
                    if type(np_arr[i, j]) is float:
                        new_arr[i, j] = 0
                    else:
                        new_arr[i, j] = get_sec(np_arr[i, j])
                except TypeError:
                    breakpoint()
            else:
                new_arr[i, j] = np_arr[i, j]

    return pd.DataFrame(new_arr, columns=keys)

def get_sec(time_str):
    """Get seconds from time."""
    m, s = time_str.split(':')
    return int(m) * 60 + int(s)


def get_row_idx_of_participant_id(df, id):
    key = df.keys()[0]
    for row in df.iterrows():
        if row[1][key] == float(id):
            return row[0]

    return -1

def get_participant_data(df, participant_id, use_id = False):
    keys = df.keys()[2:]
    times = []

    if use_id is True:
        row_id = get_row_idx_of_participant_id(df, participant_id)
        row = df.loc[row_id]

        for key in keys:
            times.append(row[key])

    else:
        for row in df.iterrows():
            for key in keys:
                times.append(row[1][key])

    return np.asarray(times)

def get_participant_condition(df, participant_id):
    row_id = get_row_idx_of_participant_id(df, participant_id)
    row = df.loc[row_id]

    return row[1]

def get_all_ids(df):
    ids = []
    for val in df[df.keys()[0]].values:
        ids.append(val)
    return ids




if __name__ == '__main__':
    df = pd.read_csv(os.path.join(os.getcwd(), "simulation_data.csv"))
    remove_empty_columns(df)
    hostage_df, drone_df = separate_drone_times(df)
    del(df)

    hostage_df = replace_nan_with_zero(hostage_df)
    drone_df = replace_nan_with_zero(drone_df)

    ids = get_all_ids(hostage_df)

    client_times = dict()

    for id in ids:
        client_times[id] = dict()
        client_times[id]['condition'] = get_participant_condition(hostage_df, participant_id=id)
        client_times[id]['hostage_times'] = get_participant_data(hostage_df, participant_id=id, use_id=True)
        client_times[id]['drone_times'] = get_participant_data(drone_df, participant_id=id, use_id=True)

    participant_id = 55

    plt.figure()
    plt.plot(client_times[participant_id]['hostage_times'].cumsum())
    plt.ylabel("Time in Simulation (s)")
    plt.xlabel("Hostages Rescued")
    plt.title("Time Spent vs Hostage Rescued\nParticipant {0}".format(participant_id))
    plt.show()

    breakpoint()

