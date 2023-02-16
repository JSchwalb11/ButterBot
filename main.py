from workspace import workspace
from dataloader import dataloader
from train_test_split import discover_files, permute_files
from utils import save_fps_to_dir, clean_dirs
import os

if __name__ == '__main__':
    debug = True
    data_dir="D:\\UnityData\\v3_0\\"
    yolo_data_dir="D:\\Datasets\\v3_0_yolo_data\\"
    img_dir = os.path.join(yolo_data_dir, "images")
    label_dir = os.path.join(yolo_data_dir, "labels")
    workspace = workspace(debug=debug, data_dir=data_dir, yolo_data_dir=yolo_data_dir)
    dataloader = dataloader(workspace=workspace, debug=debug, workers=24)
    # instantiate AI Model here
    # training data located in yolo_data_dir
    print("Ratio of images kept: {0}/{1} ({2})".format(dataloader.fps_used, len(dataloader.fps), dataloader.fps_used/len(dataloader.fps)))

    X = discover_files(img_dir, debug=False)
    y = discover_files(label_dir, debug=False)
    assert len(X) == len(y)

    X_train, X_val, X_test, y_train, y_val, y_test = permute_files(X, y)

    train_val_test_dict = dict()
    train_val_test_dict['train'] = X_train, y_train
    train_val_test_dict['val'] = X_val, y_val
    train_val_test_dict['test'] = X_test, y_test

    for key in train_val_test_dict.keys():
        root = os.path.join(yolo_data_dir, key)
        image_path = os.path.join(root, "images")
        label_path = os.path.join(root, "labels")

        clean_dirs([image_path, label_path])

        for obj in [root, image_path, label_path]:
            if not os.path.exists(obj):
                os.mkdir(obj)

        save_fps_to_dir(train_val_test_dict[key][0], image_path)
        save_fps_to_dir(train_val_test_dict[key][1], label_path)


