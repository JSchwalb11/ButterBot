import numpy as np
import matplotlib.pyplot as plt
import re
import argparse
import pandas as pd

class chessboard:
    def __init__(self, max_dim, x_start, y_start, x_origin=0, y_origin=0):
        self.x_origin = x_origin
        self.y_origin = y_origin

        self.internal_x_ticks = np.arange(x_origin, x_origin + max_dim)
        self.internal_y_ticks = np.arange(y_origin, y_origin + max_dim)

        self.historical_locations = list()
        self.current_location = (x_start, y_start)

        self.plt = plt
        self.draw(self.current_location)

    def draw(self, new_position):
        self.init_plot()
        self.update_state(new_position=new_position)
        x_val = [loc[0] for loc in self.historical_locations]
        y_val = [loc[1] for loc in self.historical_locations]

        self.ax.plot(x_val, y_val, color="b", marker="o", scalex=False, scaley=False)
        self.ax.plot(x_val[-1], y_val[-1], color="r", marker="o", scalex=False, scaley=False)
        self.plt.show()

    def draw_no_update(self):
        self.init_plot()
        x_val = [loc[0] for loc in self.historical_locations]
        y_val = [loc[1] for loc in self.historical_locations]

        self.ax.plot(x_val, y_val, color="b", marker="o", scalex=False, scaley=False)
        self.ax.plot(x_val[-1], y_val[-1], color="r", marker="o", scalex=False, scaley=False)
        self.plt.show()

    def np_arr_to_ascii_arr(self, np_arr):
        l = list()
        for val in np_arr:
            l.append(chr(val))
        return l

    def init_plot(self, xlabel="Relative Location (Lateral)", ylabel="Relative Location (Vertical)",
                  title="Player Movements"):
        self.fig, self.ax = plt.subplots()
        self.configure_plot(xlabel=xlabel, ylabel=ylabel, title=title)

    def configure_plot(self, xlabel, ylabel, title):
        self.ax.set_yticks(self.internal_y_ticks)
        self.ax.set_yticklabels(labels=self.np_arr_to_ascii_arr(self.internal_y_ticks + 65))
        self.ax.set_xticks(self.internal_x_ticks)
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)
        self.ax.set_title(title)
        self.ax.grid(visible=True)

    def update_state(self, new_position):
        self.current_location = new_position
        self.historical_locations.append(self.current_location)

    def save_state(self, fn):
        with open(fn, 'w') as f:
            for loc in self.historical_locations:
                f.write(str(loc) + '\n')

    def load_state(self, fn):
        loc = list()
        try:
            with open(fn, 'r') as f:
                for line in f.readlines():
                    x_val, y_val = self.extract_coordinates_from_string(line)
                    if x_val is not None and y_val is not None:
                        loc.append((x_val, y_val))
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
            search2 = re.findall(pattern2, tmp)
            return float(search2[0]), float(search2[1])

    def create_new_save_file(self, fn):
        with open(fn, 'w') as fp:
            ...


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

    args = parser.parse_args()

    num_steps = 5
    scale = 10

    random_steps = True
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

    board = chessboard(max_dim=args.max_dim, x_start=args.x_start, y_start=args.y_start)
    board.load_state(fn=args.load_file)
    for step in steps:
        board.draw((step[0], step[1]))

    if save_state == True:
        board.save_state(fn=args.save_file)
    else:
        board.clear_save_file(fn=args.load_file)

