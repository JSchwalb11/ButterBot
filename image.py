import image_utils as iu
import os



class image:
    def __init__(self, workspace, fp, im_downsize_ratio):
        self.fp = fp
        self.workspace = workspace
        self.data = iu.Image.open(fp)
        self.resized_img = iu.resize(fp, ratio=im_downsize_ratio)
        self.class_id = self.generate_label()
        self.resized_dim = self.resized_img.height
        self.x_anchor = None
        self.y_anchor = None
        self.w_anchor = None
        self.h_anchor = None
        self.yolo_label = ""
        self.has_contours = False
        self.extract_contour()

        if self.has_contours == True:
            self.save_image()

    def generate_label(self):
        label = int(self.fp.split("\\")[3].split(".")[0]) - 1  # 1-indexed to 0-indexed
        if label > 3:
            breakpoint()
        return label


    def generate_yolo_label(self):
        self.yolo_label = str(self.class_id) + " " + \
                          str(self.x_anchor) + " " + \
                          str(self.y_anchor) + " " + \
                          str(self.w_anchor) + " " + \
                          str(self.h_anchor)


    def extract_contour(self):
        self.contour_data, anchors = iu.filter_image_contours(self.resized_img)

        try:
            anchors /= self.resized_dim
            self.x_anchor, self.y_anchor, self.w_anchor, self.h_anchor = anchors[0], anchors[1], anchors[2], anchors[3]
            self.generate_yolo_label()
            self.has_contours = True
        except TypeError:
            #breakpoint()
            ...

    def save_image(self):
        fn = self.fp.split("\\")[-1].split(".")[0]

        path = os.path.join(self.workspace.yolo_data_dir, "images")
        #if os.path.isdir(path) is False: os.mkdir(path)
        self.data.save(os.path.join(path, fn + ".png"), format="png")

        path = os.path.join(self.workspace.yolo_data_dir, "labels")
        with open(os.path.join(path, fn + ".txt"), "w") as f:
            f.write(self.yolo_label)