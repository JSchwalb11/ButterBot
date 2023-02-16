import pandas as pd
import os
import re
import matplotlib.pyplot as plt
import numpy as np


def clean(d):
    cleaned_d = dict()
    for key in d:
        cleaned_d[key] = clean_scopus_file(d[key])

    os.chdir("Data_Files")
    fns = ["scopus_{0}.csv".format(key) for key in cleaned_d]
    for i, key in enumerate(cleaned_d):
        fn = fns[i]
        with open(fn, "w") as f:
            f.write(cleaned_d[key])



    return fns


def clean_scopus_file(fn):
    with open(fn, "r") as f:
        tmp = f.readlines()
        a = ""
        for i, line in enumerate(tmp[8:]):
            data = (line.split("\"")[1], line.split("\"")[3])
            a += data[0] + "," + data[1] + "\n"
        return a



if __name__ == '__main__':
    years_back = 50

    d_files = []
    os.chdir("../")
    for root, dirs, files in os.walk(os.path.join(os.getcwd(), "Data_Files")):
        #for dir in dirs:
        for file in files:
            if file.find("Scopus") == 0:
                path = os.path.join(root, file)

                d_files.append(path)


    search_dict = dict()

    for fn in d_files:
        with open(fn, "r") as f:
            tmp = f.readlines()
            tmp = tmp[2]
            src = re.compile("KEY(.*)")
            found = re.search(src, tmp)
            if (found):
                search_term = found.group().split("(")[1].split(")")[0]
                search_dict[search_term] = fn

    #print(search_dict)
    csv_files = clean(search_dict)

    data_dict = dict()
    for file in csv_files:
        search_term = file.split("_")[-1].split(".")[0]
        t = file
        df = pd.read_csv(t)
        df.columns = ['Year', "Paper Count"]
        df1 = df[:years_back]
        data_dict[search_term] = df1


    fig, axs = plt.subplots()

    colors = ["r", "g", "b", "m", "y", "k", "c"]
    #labels = data_dict.keys()
    labels = data_dict[list(data_dict.keys())[0]]['Year']
    x = labels
    keys = list(data_dict.keys())

    x_ = range(-(len(keys)//2).__floor__(), len(keys) - len(keys)//2)

    for i, key in enumerate(data_dict):
        print(i)
        plt.plot(x, data_dict[key]['Paper Count'], "-{0}".format(colors[i]), label=keys[i])


    plt.xlabel("Years")
    plt.ylabel("Paper Count")
    plt.title("Search Interest")


    plt.legend()
    os.chdir("../Visualization_Tools/Plots")
    path = os.getcwd()


    plt.savefig(path + "/" + "Scopus Search Interest.png")
    #plt.show()



    #breakpoint()