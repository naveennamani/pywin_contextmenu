# coding=utf-8
import os
import sys


def clean_empty_folders(root):
    count = 0
    f = os.listdir(root)
    for x in f:
        f2 = os.path.join(root, x)
        if os.path.isdir(f2):
            count += clean_empty_folders(f2)
    f = os.listdir(root)
    if len(f) == 0:
        print("Removing {}".format(root))
        os.rmdir(root)
        return count + 1
    return count


if __name__ == '__main__':
    print(f"Removed {clean_empty_folders(sys.argv[1])} empty folders")
    input("Press ENTER to continue")
