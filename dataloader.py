import os
from image import image
import time


class dataloader:


    def __init__(self, workspace, im_downsize_ratio=0.25, debug=False):
        self.workspace = workspace
        self.im_downsize_ratio = im_downsize_ratio
        self.debug = debug

        self.fps = self.discover_images()
        self.extract_images()
        self.fps_used = self.count_saved_images()


    def discover_images(self):
        fps = list()

        for root, dirs, files in os.walk(self.workspace.data_dir):
            for dir in dirs:
                path = os.path.join(root, dir)
                for root1, dirs1, files1 in os.walk(path):
                    if self.debug: print("Extracting Images from {0}".format(path))
                    for fn in files1:
                        fp = os.path.join(path, fn)
                        if self.debug: print("Found Image ({0})".format(fp))
                        fps.append(fp)

        return fps


    def extract_image(self, fp):
        image(self.workspace, fp, self.im_downsize_ratio)


    def extract_images(self):
        step = len(self.fps) // 100
        start_time = time.time()

        for i, fp in enumerate(self.fps):
            self.extract_image(fp=fp)

            if i % step == 0 and i > 0:
                step_i = i // step
                elapsed = time.time() - start_time
                steps_remaining = 100 - step_i
                avg_time_per_step = elapsed / step_i
                time_remaining = avg_time_per_step * steps_remaining
                out = "{0}% complete.".format(i // step) + \
                      " Time Elapsed: {0}.".format(elapsed) + \
                      " Time Left: {0}".format(time_remaining)
                print(out)


    def count_saved_images(self):
        for root, dirs, files in os.walk(os.path.join(self.workspace.yolo_data_dir, "images")):
            return len(files)