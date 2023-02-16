from workspace import workspace
import os
import shutil

if __name__ == '__main__':
    data_dir = "D:\\UnityData\\v3_0\\"

    i = 0
    nc = 2
    dirs = os.listdir(data_dir)

    for i in range(1, nc+1):
        path = os.path.join(data_dir, str(i))
        if not os.path.exists(path):
            os.mkdir(path)
        else:
            for root, dirs1, files in os.walk(path):
                for file in files:
                    fp = os.path.join(root, file)
                    os.remove(fp)

    for dir in dirs:
        if dir.find("Person") >= 0:
            out_dir = "1"
            for root, dirs, files in os.walk(os.path.join(data_dir, dir)):
                for file in files:
                    src = os.path.join(root, file)
                    dst = os.path.join(data_dir, f"{out_dir}\\image_{i}.png")
                    shutil.copyfile(src, dst)
                    i+=1

        elif dir.find("Building") >= 0 or dir.find("House") >= 0 or dir.find("Trailer") >= 0:
            out_dir = "2"
            for root, dirs, files in os.walk(os.path.join(data_dir, dir)):
                for file in files:
                    src = os.path.join(root, file)
                    dst = os.path.join(data_dir, f"{out_dir}\\image_{i}.png")
                    shutil.copyfile(src, dst)
                    i+=1