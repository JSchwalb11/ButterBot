from PIL import Image
import os
import numpy as np
import pickle
from sklearn.model_selection import train_test_split




import data_augmentation
import feature_extraction
import PIL
import image_ops
import yolo_utils
from yolo_utils import yolo_to_rect


def get_train_data(dir_path, ratio=0.25):
    """

    :param file_path: path to data
    :return: numpy array of images
    """
    images = []

    for root, dirs, files in os.walk(dir_path, topdown=False):
        for d in dirs:
            dir1_path = root + '/' + d
            for root1, dirs1, files1 in os.walk(dir1_path, topdown=False):
                for name in files1:
                    fp = root + '/' + d + '/' + name
                    print(fp)
                    image = np.asarray(resize(fp, ratio=ratio), dtype=np.uint8)
                    images.append(image)

    return images

def resize(image_file_path, ratio):
    img = Image.open(image_file_path)
    if (img.size[0] != 512):
        img = img.resize((512, img.size[1]), Image.ANTIALIAS)
    if(img.size[1] != 512):
        img = img.resize((img.size[0], 512), Image.ANTIALIAS)
    img_resized = img.resize((int(img.size[0]*ratio), int(img.size[1]*ratio)), Image.ANTIALIAS)
    return img_resized

def get_edge_data(img_arr):
    edge_images = np.zeros((img_arr.shape[0], img_arr.shape[1], img_arr.shape[2], img_arr.shape[3]),
                           dtype=np.uint8)

    for i, image in enumerate(img_arr):
        edge_images[i] = feature_extraction.get_edge(image)
        print("Got edges for image {0}".format(i))

    return edge_images


def retrieve_contoured_images(train_images, save_dir, input_type, dim, num_classes, debug_save_dir="C:\\Data\\Contours\\Debug\\Reference Contours\\", yolo_save_dir="C:\\Data\\Yolo Data"):
    filtered_contours, data = image_ops.filter_image_array_contours(train_images, input_type)

    #aug_images1, data1 = data_augmentation.flip_rotate(aug_images, rotate=[0], input_type=input_type, aug_yolo=False, yolo_data=data)
    aug_labels = data_augmentation.generate_labels(filtered_contours, num_classes=num_classes)

    #img_ids = list(range(0, len(filtered_contours)))
    img_ids = list()
    new_images = list()
    new_labels = list()
    new_yolo_labels = list()
    for i, image in enumerate(filtered_contours):
        nan_array = np.isnan(image)
        not_nan_array = ~ nan_array
        arr = image[not_nan_array]
        if len(arr) > 0:
            arr = arr.reshape((128, 128))
            new_images.append(arr)
            new_yolo_labels.append(data[i])
            new_labels.append(aug_labels[i])
            img_ids.append(i)

    new_yolo_labels = np.array(new_yolo_labels) / dim

    for i in range(0, len(new_images)):
        rgb_id = img_ids[i]
        cls = new_labels[i]
        yolo_data = new_yolo_labels[i]
        img = new_images[i]

        line = str(cls) + " " + \
               str(yolo_data[0]) + " " + \
               str(yolo_data[1]) + " " + \
               str(yolo_data[2]) + " " + \
               str(yolo_data[3])

        #filename = save_dir + "{0}\\".format(cls) + str(i)
        filename = save_dir + "{0}\\".format(cls) + str(rgb_id)
        PIL.Image.fromarray(img).convert("L").save(filename + ".png")

        debug_filename = debug_save_dir + "{0}\\".format(cls) + str(rgb_id)
        img = train_images[rgb_id]
        PIL.Image.fromarray(img).save(debug_filename + ".png")


        with open(filename + ".txt", 'w') as f:
            f.write(line)
            f.close()

        with open(debug_filename + ".txt", 'w') as f:
            f.write(line)
            f.close()


    return new_images, new_labels, new_yolo_labels




if __name__ == '__main__':
    data_dir = "D:\\UnityData\\v3_0"
    contour_save_dir = "D:\\UnityData\\v3_0\\Contours"
    #pca_save_dir = "C:\\Data\\PCA\\"
    debug_contour_save_dir = "C:\\Data\\Contours\\Debug\\Reference Contours\\"

    input_type = 'b/w'
    #input_type = 'rgb'



    num_classes = len(os.listdir(data_dir))
    paths = [contour_save_dir, debug_contour_save_dir]

    for i in range(0, num_classes):
        for path in paths:
            p = os.path.join(path, str(i))

            try:
                os.mkdir(p)
                print("Created Directory")
            except OSError as error:
                print("Directory Already Exists")


    train_images = np.asarray(get_train_data(dir_path=data_dir, ratio=0.25))
    train_labels = data_augmentation.generate_labels(train_images, num_classes=num_classes)

    dim = train_images.shape[1]

    contour_images, contour_labels, yolo_labels = retrieve_contoured_images(train_images,
                                                                        dim=dim,
                                                                        save_dir=contour_save_dir,
                                                                        input_type='rgb',
                                                                        num_classes=num_classes)

    #yolo_utils.yolo_to_rect(debug_contour_save_dir=debug_contour_save_dir)
    #upscaled_imgs = yolo_utils.upscale_images(train_images, new_w=640, new_h=640)


    tmp = 0
    for i, label in enumerate(train_labels):
        if label != tmp:
            print("New class at idx {0}".format(i))
            tmp = label



