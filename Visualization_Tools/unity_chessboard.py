import os

import numpy as np
import matplotlib.pyplot as plt
import re
import argparse
import pandas as pd

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

        """ax.plot(x_arr, z_arr,
                color=color,
                #marker=marker,
                scalex=scalex,
                scaley=scaley,
                label=self.label,
                linewidth=1.)
        #ax.scatter(x_arr, z_arr, color=color, marker=marker)
        print(ax.axis())"""

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


class chessboard:
    def __init__(self, max_dim, x_start, y_start, x_origin=0, y_origin=0, add_labels=True):
        self.x_origin = x_origin
        self.y_origin = y_origin
        self.max_dim = max_dim

        #self.internal_x_ticks = np.arange(x_origin, x_origin + max_dim, (x_origin + max_dim) // 10)
        #self.internal_y_ticks = np.arange(y_origin, y_origin + max_dim, (y_origin + max_dim) // 10)
        self.internal_x_ticks = np.arange(-max_dim, max_dim, max_dim//5)
        self.internal_y_ticks = np.arange(-max_dim, max_dim, max_dim//5)

        self.xlabel = "Relative Location (Lateral)"
        self.ylabel = "Relative Location (Vertical)"
        self.title="Player Movements"

        self.historical_locations = list()
        self.objects = list()
        self.current_location = (x_start, y_start)

        self.plt = plt

        self.add_labels = add_labels
        #self.draw(self.current_location)

    def add_object(self, unity_object):
        self.objects.append(unity_object)

    def draw_objects(self):
        self.init_plot()
        #self.ax.autoscale(enable=False)
        markers = ['o', '*', '.']
        colors = ['r', 'b', 'y']
        plot_type = "line"
        size=1.

        for i, object in enumerate(self.objects):
            #breakpoint()
            if object.label.find("hostage") > -1:
                plot_type = "scatter"
                size=4

            object.draw_no_update(self.plt,
                                  color=colors[i],
                                  #marker=markers[i],
                                  scalex=False,
                                  scaley=False,
                                  size=size,
                                  plot_type=plot_type)
            #self.configure_plot()
            #self.ax.figure.show()

        #self.configure_plot()
        #self.plt.show()
        """self.init_plot()
        for i, object in enumerate(self.objects):
            print(object.label)
            object.draw_no_update(self.plt)
        """

        self.plt.legend()

    def np_arr_to_ascii_arr(self, np_arr):
        l = list()
        for val in np_arr:
            l.append(chr(val))
        return l

    def init_plot(self):
        self.fig, self.ax = plt.subplots()
        self.configure_plot()

    def configure_plot(self):
        self.plt.xlim([-self.max_dim, self.max_dim])
        self.plt.ylim([-self.max_dim, self.max_dim])
        self.plt.yticks(self.internal_y_ticks)
        # self.ax.set_yticklabels(labels=self.np_arr_to_ascii_arr(self.internal_y_ticks + 65))
        self.plt.xticks(self.internal_x_ticks)
        self.plt.xlabel(self.xlabel)
        self.plt.ylabel(self.ylabel)
        self.plt.title(self.title)
        self.plt.grid(visible=True)
        if self.add_labels == False:
            self.plt.xticks([])
            self.plt.yticks([])

    def update_state(self, new_position):
        self.current_location = new_position
        self.historical_locations.append(self.current_location)

    def save_state(self, fn):
        with open(fn, 'w') as f:
            for loc in self.historical_locations:
                f.write(str(loc) + '\n')


    def clear_save_file(self, fn):
        with open(fn, 'w') as fp:
            ...


if __name__ == '__main__':
    # python3 unity_chessboard.py --max_dim=10 --x_start=1 --y_start=1 --load_file=chessboard_state.txt --save_file=chessboard_state.txt --x_pos=2.33 --y_pos=3.2"
    parser = argparse.ArgumentParser(description="Draws a chessboard representation of the Player's historical position" \
                                                 + " within the game.")
    parser.add_argument("--max_dim", type=int,
                        help="Higher dimension yields a more granular position.\n" \
                             + "ex. max_dim=5: 5^2 possible locations, " \
                             + "max_dim=10: 10^2 possible locations.")

    parser.add_argument("--x_start", type=float,
                        help="Starting position on X Axis.")
    parser.add_argument("--y_start", type=float,
                        help="Starting position on Y Axis.")

    parser.add_argument("--save_file", type=str,
                        help="File to save state data to.")

    parser.add_argument("--load_file", type=str,
                        help="File to load state data from.")

    parser.add_argument("--x_pos", type=float,
                        help="Current position on X Axis.")

    parser.add_argument("--y_pos", type=float,
                        help="Current position on Y Axis.")

    parser.add_argument("--data_dir", type=str,
                        help="Directory that contains all data files.")

    args = parser.parse_args()

    num_steps = 5
    scale = 5

    random_steps = False
    save_state = False
    steps = list()

    if random_steps == True:
        df = pd.DataFrame(np.random.random(num_steps * 2).reshape((num_steps, 2)), columns=['x_pos', 'y_pos'])
        for val in df.values:
            steps.append(val * scale)

    else:
        steps.append((1., 2.))
        steps.append((3., 1.))
        steps.append((2., 3.))

    objects_discovered = dict()
    for root, dirs, files in os.walk(args.data_dir):
        for file in files:
            objects_discovered[file] = os.path.join(root, file)

    board = chessboard(max_dim=args.max_dim, x_start=args.x_start, y_start=args.y_start, add_labels=True)

    for object in objects_discovered:
        #breakpoint()
        board.add_object(unity_object(label=object, data_file=objects_discovered[object]))
    board.draw_objects()
    board.plt.show()

    if save_state == True:
        board.save_state(fn=args.save_file)
    else:
        #board.clear_save_file(fn=args.load_file)
        ...

