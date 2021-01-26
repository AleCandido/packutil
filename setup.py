# -*- coding: utf-8 -*-
import sys
import pathlib
import importlib

from setuptools import setup, find_packages

MAJOR = 0
MINOR = 0
MICRO = 2
repo_path = pathlib.Path(__file__).absolute().parent

# import packutil as pu
sys.path.insert(0, str((repo_path / "src").absolute()))
pu = importlib.import_module("packutil")
sys.path.pop(0)


def setup_package():
    # write version
    pu.versions.write_version_py(
        MAJOR,
        MINOR,
        MICRO,
        pu.versions.is_released(repo_path),
        filename="src/packutil/version.py",
    )
    # paste Readme
    with open("README.md", "r") as fh:
        long_description = fh.read()
    # do it
    setup(
        name="packutil",
        author="Alessandro Candido",
        version=pu.versions.mkversion(MAJOR, MINOR, MICRO),
        long_description=long_description,
        long_description_content_type="text/markdown",
        author_email="",
        url="https://github.com/N3PDF/banana",
        description="mm yummy banana",
        package_dir={"": "src"},
        packages=find_packages("src"),
        package_data={},
        classifiers=[
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
        ],
        install_requires=["pygit2", "semver"],
        python_requires=">=3.7",
    )


if __name__ == "__main__":
    setup_package()
