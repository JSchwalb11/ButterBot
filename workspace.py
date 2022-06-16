import os



class workspace():
    def __init__(self, data_dir="C:\\Data\\Latest v2.0\\",
                 contour_dir="C:\\Data\\Contours\\",
                 pca_dir="C:\\Data\\PCA\\",
                 ref_contours_dir="C:\\Data\\Contours\\Debug\\Reference Contours\\",
                 yolo_data_dir="C:\\Users\\JoeyS\\PycharmProjects\\datasets\\",
                 debug=False):

        self.data_dir = data_dir
        self.contour_dir = contour_dir
        self.pca_dir = pca_dir
        self.ref_contours_dir = ref_contours_dir
        self.yolo_data_dir = yolo_data_dir
        self.debug = debug

        self.create_directories()


    def create_directories(self):
        paths = [self.contour_dir, self.ref_contours_dir]
        num_classes = len(os.listdir(self.data_dir))
        for i in range(0, num_classes):
            for path in paths:
                p = os.path.join(path, str(i))

                try:
                    os.mkdir(p)
                    if self.debug: print("Created Directory")
                except OSError:
                    if self.debug: print("Directory Already Exists")

        paths = [self.yolo_data_dir, os.path.join(self.yolo_data_dir, "images"), os.path.join(self.yolo_data_dir, "labels")]

        for path in paths:
            try:
                os.mkdir(path)
                if self.debug: print("Created Directory")
            except OSError:
                if self.debug: print("Directory Already Exists")