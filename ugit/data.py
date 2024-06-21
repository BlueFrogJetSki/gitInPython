import os
import hashlib

GIT_DIR = ".ugit"


def init():

    os.makedirs(GIT_DIR)
    os.makedirs(f"{GIT_DIR}/objects")


def hash_objects(data, type_="blob") -> str:

    # prepend the type to the start of the file, followed by a null byte
    obj = type_.encode() + b"\x00" + data
    oid = hashlib.sha1(data).hexdigest()

    with open(f"{GIT_DIR}/objects/{oid}", "wb") as out:
        out.write(obj)

    return oid


def get_object(oid, expected="blob") -> bytes:

    with open(f"{GIT_DIR}/objects/{oid}", "rb") as f:
        obj = f.read()

    type_, _, content = obj.partition(b"\x00")
    type_ = type_.decode()

    if expected != None:
        assert type_ == expected, f"expected{expected}, got {type_}"

    return content
