import os

# https://www.leshenko.net/p/ugit/#write-tree-ignore-ugit
from . import data


def write_tree(directory="."):
    entries = []
    with os.scandir(directory) as it:
        for entry in it:
            fullPath = f"{directory}/{entry.name}"

            oid = 0
            type_ = "blob"
            if is_ignored(fullPath):
                continue

            if entry.is_file(follow_symlinks=False):
                type_ = "blob"
                with open(entry.path, "rb") as f:
                    oid = data.hash_objects(f.read(), type_)

            elif entry.is_dir(follow_symlinks=False):
                type_ = "tree"
                oid = write_tree(fullPath)

            entries.append((entry.name, oid, type_))

    tree = "".join(f"{type_} {oid} {name}\n" for name, oid, type_ in entries)

    return data.hash_objects(tree.encode(), "tree")


def is_ignored(path) -> bool:
    return ".ugit" in path.split("/") or ".git" in path.split("/")


def _iter_tree_entries(oid):
    if not oid:
        return
    tree = data.get_object(oid, "tree")
    for entry in tree.decode().splitlines():
        type_, oid, name = entry.split(" ", 2)
        yield type_, oid, name


def get_tree(oid, base_path=""):
    result = {}
    for type_, oid, name in _iter_tree_entries(oid):
        assert "/" not in name
        assert name not in ("..", ".")
        path = base_path + name
        if type_ == "blob":
            result[path] = oid
        elif type_ == "tree":
            result.update(get_tree(oid, f"{path}/"))
        else:
            assert False, f"Unknown tree entry {type_}"
    return result


def read_tree(tree_oid):
    for path, oid in get_tree(tree_oid, base_path="./").items():
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            f.write(data.get_object(oid))
