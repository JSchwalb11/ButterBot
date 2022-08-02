import os
import subprocess
import mmap
import argparse
import sys

"""
def hello_world_mmap():
    # write a simple example file
    with open("hello.txt", "wb") as f:
        f.write(b"Hello Python!\n")

    with open("hello.txt", "r+b") as f:
        # memory-map the file, size 0 means whole file
        mm = mmap.mmap(f.fileno(), 0)
        # read content via standard file methods
        print(mm.readline())  # prints b"Hello Python!\n"
        # read content via slice notation
        print(mm[:5])  # prints b"Hello"
        # update content using slice notation;
        # note that new content must have same size
        mm[6:] = b" world!\n"
        # ... and read again using standard file methods
        mm.seek(0)
        print(mm.readline())  # prints b"Hello  world!\n"
        # close the map
        mm.close()
"""

if __name__ == '__main__':
    l = []
    for arg in sys.argv:
        l.append(arg)
    print(l)
    """
    yolov5_dir = "C:\\Users\\JoeyS\\PycharmProjects\\yolov5"
    command = "python detect.py --weights yolov5s.pt --img 640 --conf 0.25 --source data/images"

    parser = argparse.ArgumentParser(description='Run Yolov5 Detector on MemoryMapped File.')
    parser.add_argument("--mmf", type=str, help="Name of MemoryMappedFile to be accessed.")
    parser.add_argument("--mmf_ptr", type=int, help="Pointer of MemoryMappedViewStream to be accessed.")

    args = parser.parse_args()

    path = "C:\\Users\\JoeyS\\PycharmProjects\\ButterBot\\MMF"
    fn = str(args.mmf_ptr)
    fp = os.path.join(path, fn)
    with open(fp, 'w') as f:
        f.write("Test")
        f.close()
    """


