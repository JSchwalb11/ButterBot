import os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import re

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

    hostage_df = hostage_df.drop(labels=[19,38], axis=0)
    drone_df = drone_df.drop(labels=[19,38], axis=0)


    ids = get_all_ids(hostage_df)

    client_times = dict()

    for id in ids:
        client_times[id] = dict()
        client_times[id]['condition'] = get_participant_condition(hostage_df, participant_id=id)
        client_times[id]['Hostage_times'] = get_participant_data(hostage_df, participant_id=id, use_id=True)
        client_times[id]['Drone_times'] = get_participant_data(drone_df, participant_id=id, use_id=True)

    print(str(len(client_times)) + " Participants")
    participant_id = 42

    types = ['Hostage_times', 'Drone_times']
    titles = ['Objective - Hostage Rescue', 'Objective - Hostage Spotting']
    for i, type in enumerate(types):
        tmp = type.split("_")[0]
        """plt.figure()
        plt.plot(client_times[participant_id][type].cumsum())
        plt.ylabel("Time in Simulation (s)")
        plt.xlabel(tmp + " Rescued")
        plt.title("Time Spent vs Hostage Rescued\nParticipant {0}".format(participant_id))
        plt.show()"""


        fig, axs = plt.subplots(2,2, sharex=True, sharey=True)

        p_mode = client_times[participant_id]['condition']
        axs[0, 0].plot(client_times[participant_id][type][:16].cumsum())
        axs[0, 0].set_title("Participant {0}".format(participant_id))

        p_mode1 = client_times[participant_id]['condition']
        axs[0, 1].plot(client_times[participant_id + 1][type][:16].cumsum())
        axs[0, 1].set_title("Participant {0}".format(participant_id + 1))

        p_mode2 = client_times[participant_id]['condition']
        axs[1, 0].plot(client_times[participant_id + 2][type][:16].cumsum())
        axs[1, 0].set_title("Participant {0}".format(participant_id + 2))

        p_mode3 = client_times[participant_id]['condition']
        axs[1, 1].plot(client_times[participant_id + 3][type][:16].cumsum())
        axs[1, 1].set_title("Participant {0}".format(participant_id + 3))

        fig.supxlabel("Running Objective Count")
        fig.supylabel("TT Scenario (s)")
        fig.suptitle(titles[i])
        plt.savefig(titles[i])
        breakpoint()

    #participant_ids = [participant_id, participant_id + 1, participant_id + 2, participant_id + 3]

    missing_participants = []
    conditions = list()
    drone_times = list()
    human_times = list()
    for i in range(1, len(client_times) + 1):
        try:
            conditions.append(client_times[i]['condition'])
            drone_times.append(client_times[i]['Drone_times'])
            human_times.append(client_times[i]['Hostage_times'])
        except KeyError:
            missing_participants.append(i)


    plt.clf()
    df = pd.DataFrame(conditions)
    df1 = df.value_counts()
    #df1.astype(np.int8)

    pattern = re.compile("([a-zA-Z]*)")
    tmp = []
    for i, val in enumerate(df1.index.values):
        search = re.search(pattern, val[0])
        df1.index.values[i] = search.group()

    plt.bar(range(len(df1)), df1.values, align='center')
    plt.xticks(range(len(df1)), df1.index.values)
    plt.title("Distribution of Incentive Mechanisms")
    plt.savefig("Distribution of Incentive Mechanisms")

    df = pd.DataFrame(drone_times)
    num_mode_switches = list()
    total_time = list()
    for row in df.iterrows():
        count = 0
        for val in row[1]:
            if val > 0:
                count += 1
        num_mode_switches.append(count)
        total_time.append(np.sum(row[1]))
    df_drone_time_stats = pd.DataFrame(total_time, columns=["TT Manual Mode"])
    df_num_mode_switches = pd.DataFrame(num_mode_switches, columns=["Distribution of Mode Switching n={0}".format(len(num_mode_switches))])

    df = pd.DataFrame(human_times)
    total_time = list()
    for row in df.iterrows():
        total_time.append(np.sum(row[1]))
    df_human_time_stats = pd.DataFrame(total_time, columns=["TT Automatic Mode"])

    df_tt = pd.DataFrame(df_drone_time_stats.values + df_human_time_stats.values, columns=["TT"])

    df2 = pd.concat([df_drone_time_stats, df_human_time_stats, df_tt], axis=1)
    summary_table = df2.describe()
    plt.clf()
    df2.boxplot(['TT Manual Mode', 'TT Automatic Mode'])

    plt.title("Modal Usage")
    plt.ylabel("Time (s)")
    plt.savefig("Time in Different Modes Boxplot")
    plt.clf()
    plt.scatter(df2['TT Manual Mode'], df2['TT'], marker="*", color='r', label="Manual Mode")
    plt.scatter(df2['TT Automatic Mode'], df2['TT'], marker="o", color='b', label="Automatic Mode")
    #plt.title("Modal Usage")
    plt.ylabel("TT Scenario (s)")
    plt.xlabel("Modal Usage (s)")
    plt.legend()

    plt.savefig("Time in Different Modes Scatter")
    plt.clf()

    print(summary_table)
    df_num_mode_switches.hist(grid=False)
    plt.xlabel("Frequency")
    plt.ylabel("Participant Count")
    plt.savefig("Distribution of Mode Switching")

    df = pd.DataFrame(human_times)
    hostages_rescued = list()
    for row in df.iterrows():
        count = 0
        for val in row[1]:
            if val > 0:
                count += 1
        hostages_rescued.append(count)







