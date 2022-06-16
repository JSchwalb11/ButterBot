from workspace import workspace
from dataloader import dataloader



if __name__ == '__main__':
    debug = False
    workspace = workspace(debug=debug, data_dir="C:\\Data\\Latest v2.0\\", yolo_data_dir="C:\\Users\\JoeyS\\PycharmProjects\\datasets\\test\\")
    dataloader = dataloader(workspace=workspace, debug=debug)
    # instantiate AI Model here
    # training data located in yolo_data_dir

    print("Ratio of images kept: {0}/{1} ({2})".format(dataloader.fps_used, len(dataloader.fps), dataloader.fps_used/len(dataloader.fps)))

