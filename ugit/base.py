import os

# https://www.leshenko.net/p/ugit/#write-tree-ignore-ugit
from . import data


def write_tree(directory="."):
    with os.scandir(directory) as it:
        for entry in it:
            fullPath = f"{directory}/{entry.name}"

            if is_ignored(fullPath):
                continue

            if entry.is_file(follow_symlinks=False):
                # TODO write the file to object store
                # with open(entry.path, "wb") as f:
                #     data.hash_objects(f.read())

                print(fullPath)
            elif entry.is_dir(follow_symlinks=False):
                write_tree(fullPath)

    # TODO actually create the tree object


def is_ignored(path) -> bool:
    return ".ugit" in path.split("/") or ".git" in path.split("/")
