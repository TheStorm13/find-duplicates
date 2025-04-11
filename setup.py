from setuptools import setup, find_packages

setup(
    name="image-cli-tool",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "click",
        "Pillow",
        "imagehash",
    ],
    entry_points={
        "console_scripts": [
            "find-duplicate=cli.main_cli:ImageCLI.cli",  # Привязка команды `image-cli` к классу.
        ],
    },
)
