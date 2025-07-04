from setuptools import setup, find_packages

setup(
    name="find-duplicate",
    version="1.0",
    packages=find_packages(where="src"),  # Ищем пакеты только в src
    package_dir={"": "src"},             # Указываем, что корень пакетов - src
    install_requires=[
        "click",
        "Pillow",
        "imagehash",
        "psutil",
    ],
    entry_points={
        "console_scripts": [
            "find-duplicate=cli.cli:cli",
        ],
    },
)
