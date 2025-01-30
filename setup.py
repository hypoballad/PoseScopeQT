from setuptools import setup, find_packages

setup(
    name="PoseScopeQT",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "PyQt6",
        "pytest"
    ],
    entry_points={
        "gui_scripts": [
            "PoseScopeQT = src.main:main"
        ]
    }
)
