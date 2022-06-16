import PIL.Image
import cv2
import numpy as np
import math
from matplotlib import pyplot as plt
from PIL import Image

def resize(image_file_path, ratio):
    img = Image.open(image_file_path)
    if (img.size[0] != 512):
        img = img.resize((512, img.size[1]), Image.ANTIALIAS)
    if(img.size[1] != 512):
        img = img.resize((img.size[0], 512), Image.ANTIALIAS)
    img_resized = img.resize((int(img.size[0]*ratio), int(img.size[1]*ratio)), Image.ANTIALIAS)
    return img_resized

def coords_top_left_to_center(x_tl, y_tl, w, h):
    x_center = x_tl + (w/2)
    y_center = y_tl + (h/2)
    return x_center, y_center

def get_contours(im):
    bw_img = get_bw_image(im)
    bw_img_arr = PIL_to_Numpy(bw_img)
    contours, hierarchy = cv2.findContours(bw_img_arr, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2:]
    return bw_img, contours

def pil_to_cv(pil_image):
    """
    Returns a copy of an image in a representation suited for OpenCV
    :param pil_image: PIL.Image object
    :return: Numpy array compatible with OpenCV
    """
    return np.array(pil_image)

def get_bw_image(im_rgb):
    if type(im_rgb) is PIL.Image.Image:
        #breakpoint()
        im_tmp = PIL_to_Numpy(im_rgb)
    else:
        im_tmp = im_rgb

    im_bgr = cv2.cvtColor(im_tmp, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(im_bgr, cv2.COLOR_BGR2GRAY)
    ret, bw_img = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    return Numpy_to_PIL(bw_img)


def gr_to_bw(im_gr):
    #cv2.C
    #gray = cv2.cvtColor(im_gr, cv2.COLOR_BGR2GRAY)
    ret, bw_img = cv2.threshold(im_gr, 127, 255, cv2.THRESH_BINARY)
    return bw_img

def get_canny_edge(im_rgb, threshold1=100, threshold2=200):
    # convert im_rgb from PIL.Image to numpy array
    # extract edges from numpy array
    # convert numpy array to PIL.Image
    tmp = np.array(im_rgb)
    canny = cv2.Canny(tmp, threshold1, threshold2)
    tmp_contour = Image.fromarray(canny)
    return tmp_contour

def PIL_to_Numpy(im):
    return np.array(im)


def Numpy_to_PIL(arr):
    return Image.fromarray(arr)

def extract_edges(numpy_img_arr):
    edge_arr = np.zeros((numpy_img_arr.shape[0], numpy_img_arr.shape[1], numpy_img_arr.shape[2]),
                          dtype=np.uint8)
    for i, image in enumerate(numpy_img_arr):
        edge_arr[i] = get_canny_edge(image)

    return edge_arr

def filter_image_contours(im, idx=0, canny_edge=False, contours=False, input_type='rgb', heuristics=True):
    im2, contours = get_contours(im)

    im2 = PIL_to_Numpy(im2)

    max_area = 0
    max_area_arg = 0
    area = lambda cnt: math.prod(cv2.boundingRect(cnt)[2:])


    for i, cnt in enumerate(contours):
        #area_i = cv2.contourArea(cnt)#area(cnt)
        area_i = area(cnt)
        if area_i > max_area:
            max_area = area_i
            max_area_arg = i

    if len(contours) > 0:
        object_of_interest = contours[max_area_arg]
        x, y, w, h = cv2.boundingRect(object_of_interest)
        im3 = np.zeros((im2.shape[0], im2.shape[1]), dtype=np.uint8)
        if heuristics == False:
            return im2, np.asarray([x, y, w, h])

        if max_area > 512 and w < 128:
            object_of_interest = contours[max_area_arg]
            x, y, w, h = cv2.boundingRect(object_of_interest)
            if x == 0:
                x = x + 1
            if y == 0:
                y = y + 1
            # print("x: {0}\ny: {1}\nw: {2}\nh: {3}\n".format(x,y,w,h))
            # cv2.rectangle(im3, (x, y), (x + w, y + h), (200, 0, 0), 2)
            im3[y:y + h, x:x + w] = im2[y:y + h, x:x + w]
            x_center, y_center = coords_top_left_to_center(x, y, w, h)
            #data = (x, y, w, h)
            if x == 0 or y == 0:
                print()
            return im3, np.asarray([x_center, y_center, w, h])
        else:
            """
            fig, axs = plt.subplots(nrows=1, ncols=2)
            cv2.rectangle(im3, (x, y), (x + w, y + h), (200, 0, 0), 2)
            im3[y:y + h, x:x + w] = im2[y:y + h, x:x + w]
            axs[0].imshow(im2)
            axs[1].imshow(im3)
            plt.show()
            """
            #print("Found something weird")
            #print("x: {0}\ny: {1}\nw: {2}\nh: {3}\n".format(x,y,w,h))
            return None, None


    else:
        return None, None

def extract_yolo_coords():
    ...

def filter_image_array_contours(image_array):
    tmp = np.zeros((image_array.shape[0], image_array.shape[1], image_array.shape[2]))
    img_coords = list()
    for i, single_image in enumerate(image_array):
        print("image #{0}".format(i))
        img, data = filter_image_contours(i, single_image)
        tmp[i] = img
        img_coords.append(data)
    return tmp, np.asarray(img_coords)

if __name__ == '__main__':
    import pickle
    import sys
    from matplotlib import pyplot as plt

    x = -2
    y = 4
    w = 10
    h = 6

    x_c, y_c = coords_top_left_to_center(x,y,w,h)
    print()


    aug_images_file = open("aug_data.pkl", 'rb')
    aug_labels_file = open("aug_labels.pkl", 'rb')

    aug_images = pickle.load(aug_images_file)
    aug_labels = pickle.load(aug_labels_file)

    """
    if (len(aug_images) == len(aug_labels)):
        print("Lengths match")
    else:
        print("Lengths do not match, check data loader")
        sys.exit(0)
    """
    """
    num_classes = 4
    slice = len(aug_images) // num_classes
    im = aug_images[slice*1+1000]
    im_bw = get_bw_image(im)
    im_contour = get_contours(im_bw, input_type='b/w')
    edges = cv2.Canny(im, 100, 200)
    bw_edges = cv2.Canny(im_bw, 100, 200)
    plt.figure(1)
    """
    #fig, axes = plt.subplots(nrows=4, ncols=3, sharey=True)

    imgs = np.asarray( [aug_images[1], aug_images[10500], aug_images[13200], aug_images[17573]] , dtype=np.uint8)
    input_type = 'b/w'
    fig, axes = plt.subplots(nrows=len(imgs), ncols=3)
    axes[0][0].set_title("Before Filtering")
    axes[0][1].set_title("After Filtering")
    axes[0][2].set_title("Centroid")
    contoured_imgs, data = filter_image_array_contours(imgs, input_type=input_type)
    for i, im in enumerate(imgs):
        axes[i][0].imshow(im)
        axes[i][1].imshow(contoured_imgs[i])

        x,y,w,h = data[i][0], data[i][1], data[i][2], data[i][3]
        x_center, y_center = coords_top_left_to_center(x,y,w,h)
        axes[i][2].plot(x_center, y_center, marker="o", markeredgecolor="red", markerfacecolor="green")
        cv2.rectangle(contoured_imgs[i], (x, y), (x + w, y + h), (200, 0, 0), 2)
        axes[i][2].imshow(contoured_imgs[i])

    fig.suptitle("Contour Selection")
    plt.show()
    plt.savefig("Contour Selection")
        #axes[i][0].imshow(im)


        #im_canny = get_canny_edge(im)
        #axes[i][1].imshow(im_canny)


        #im_bw = get_bw_image(im)
        #im_contour = get_contours(im_bw, input_type='b/w')
        #axes[i][2].imshow(im_contour[0])

    """
    axes[0][0].set_title("Original")
    axes[0][1].set_title("get_canny_edge")
    axes[0][2].set_title("get_contours")
    fig.suptitle("Preprocessing Images")
    plt.savefig("Preprocessing_Images")
    """

    #plt.subplot(211)
    #plt.imshow(edges, cmap='gray')
    #plt.subplot(212)
    #plt.imshow(bw_edges, cmap='gray')
    #plt.imshow(im_contour, cmap='gray')
    #plt.subplot(221)
    #plt.imshow(edges, cmap='gray')
    #plt.show()
