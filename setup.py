from setuptools import setup, find_packages

setup(
    name="image-cli-tool",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "click",
        "Pillow",
    ],
    entry_points={
        "console_scripts": [
            "image-cli=cli.main_cli:ImageCLI.cli",  # Привязка команды `image-cli` к классу.
        ],
    },
)
