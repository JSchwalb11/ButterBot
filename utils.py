import shutil
import os
from pathlib import Path

def save_fps_to_dir(fps, dir):
    num_files = 0
    for num_files, fp in enumerate(fps):
        fp = Path(fp)
        src = Path(fp)
        dst = Path(os.path.join(dir, os.path.basename(src)))
        shutil.copyfile(src, dst)

    print(f"Saved {num_files}")

def clean_dirs(dirs):
    num_files = 0
    for num_dirs, dir in enumerate(dirs):
        for root, dirs1, files in os.walk(dir):
            for num_files, file in enumerate(files):
                rm_path = os.path.join(root, file)
                os.remove(rm_path)
        print(f"Removed {num_files} in {dir}")

