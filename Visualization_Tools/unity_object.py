import numpy as np
import pandas as pd
import re

class unity_object:
    def __init__(self, label, data_file, start=(0,0,0), origin=(0,0,0)):
        self.x_origin = origin[0]
        self.y_origin = origin[1]
        self.z_origin = origin[2]

        self.historical_locations = list()
        self.current_location = start
        self.label = label

        self.fn = data_file
        self.load_state()

    def draw_no_update(self, ax, color="b", marker="o", scalex=False, scaley=False, size=1., plot_type="line"):
        print(ax.axis())
        x_val = [loc[0] for loc in self.historical_locations]
        z_val = [loc[2] for loc in self.historical_locations]
        df = pd.DataFrame(x_val, dtype=np.float32)
        df1 = pd.DataFrame(z_val, dtype=np.float32)
        x_arr = np.asarray(x_val, dtype=np.float32)
        z_arr = np.asarray(z_val, dtype=np.float32)

        if plot_type == "scatter":
            ax.scatter(x_arr, z_arr,
                       color=color,
                       marker=marker,
                       s=size,
                       #markersize=1.,
                       label=self.label)
        elif plot_type == "line":
            ax.plot(x_arr, z_arr,
                    color=color,
                    #marker=marker,
                    scalex=scalex,
                    scaley=scaley,
                    linewidth=size,
                    label=self.label)
            ax.plot(x_arr[-1], z_arr[-1],
                    color="g",
                    #marker=marker,
                    scalex=scalex,
                    scaley=scaley,
                    linewidth=size,
                    label=self.label)

        """elif plot_type == "dot":
            for val in zip(x_val, z_val):
                ax.plot(float(val[0]), float(val[1]), color=color, marker=marker, scalex=scalex, scaley=scaley)
                ax.figure.show()"""

        """if plot_type == "scatter":
            ax.scatter(x_val, z_val, color=color, marker=marker)
        elif plot_type == "line":
            ax.plot(x_val, z_val, color=color, marker=marker, scalex=scalex, scaley=scaley)
            ax.plot(x_val[-1], z_val[-1], color="g", marker=marker, scalex=scalex, scaley=scaley)
        elif plot_type == "dot":
            for val in zip(x_val, z_val):
                ax.plot(float(val[0]), float(val[1]), color=color, marker=marker, scalex=scalex, scaley=scaley)
                ax.figure.show()
        #ax.plot(x_val[-1], z_val[-1], color="r", marker="o", scalex=scalex, scaley=scaley)
        #self.plt.show()"""

    def update_state(self, new_position):
        self.current_location = new_position
        self.historical_locations.append(self.current_location)

    def load_state(self):
        loc = list()
        try:
            with open(self.fn, 'r') as f:
                for line in f.readlines():
                    x_val, y_val, z_val = self.extract_coordinates_from_string(line)
                    if x_val is not None and y_val is not None and z_val is not None:
                        loc.append((x_val, y_val, z_val))
            if len(loc) == 0:
                loc.append(self.current_location)

            self.historical_locations = loc
        except FileNotFoundError:
            ...

    def extract_coordinates_from_string(self, string):
        pattern1 = re.compile("\(.*\)")
        pattern2 = re.compile("\d+.\d+")

        search1 = re.search(pattern1, string)
        if search1 is not None:
            tmp = search1.group()
            #search2 = re.findall(pattern2, tmp)
            tmp = tmp.strip("(")
            tmp = tmp.strip(")")
            tmp = tmp.split(",")
        return tmp[0], tmp[1], tmp[2]
