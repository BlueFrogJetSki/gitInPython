from setuptools import setup

setup(
    name="ugit",
    version="1.0",
    packages=["gitInPython"],
    entry_points={"console_scripts": ["ugit = ugit.main:main"]},
)
