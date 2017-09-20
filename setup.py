from setuptools import setup, find_packages

setup(
    name="StefParse",
    author="Nathan Klapstein",
    author_email="nklapste@ualberta.ca",
    version="0.0.0",
    description="Terminal filter/parser for AlbertaSat dev needs",
    url="https://github.com/nklapste/StefParse",
    keywords="AlbertaSat parse filter logger terminal",
    packages=find_packages(exclude=["test"]),
    package_data={
        "": ["README.md"],
    },
    install_requires=[],
    entry_points={
        "console_scripts": ["stefparse = stefparse.__main__:main"],
    },
)
