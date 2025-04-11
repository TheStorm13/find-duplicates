from setuptools import setup, find_packages

setup(
    name="find-duplicate",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "click",
        "Pillow",
        "imagehash",
    ],
    entry_points={
        "console_scripts": [
            "find-duplicate=src.main:cli",
        ],
    },
)
