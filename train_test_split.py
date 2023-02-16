import os
from sklearn.model_selection import train_test_split

def discover_files(data_dir, debug=False):
    fps = list()
    numFiles = 0
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            numFiles += 1
            fp = os.path.join(root, file)
            if debug: print("Found file ({0})".format(fp))
            fps.append(fp)

    print(f"Found {numFiles} files.")
    return fps

def permute_files(X, y, train_size=0.7, val_size=0.25, test_size=0.05):
    X_train, X_val, y_train, y_val = train_test_split(X, y, train_size=train_size)
    X_val, X_test, y_val, y_test = train_test_split(X_val, y_val, test_size=test_size/val_size)

    return X_train, X_val, X_test, y_train, y_val, y_test