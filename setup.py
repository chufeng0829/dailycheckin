# -*- coding: utf-8 -*-
import io
import os
import sys
from os import walk
from os.path import isfile, join
from shutil import rmtree

from setuptools import Command, find_packages, setup

NAME = "dailycheckin"
FOLDER = "dailycheckin"
DESCRIPTION = "dailycheckin"
EMAIL = "133397418@qq.com"
AUTHOR = "Sitoi"
REQUIRES_PYTHON = ">=3.6.0"
VERSION = None


def read_file(filename):
    with open(filename) as fp:
        return fp.read().strip()


def read_requirements(filename):
    return [
        line.strip()
        for line in read_file(filename).splitlines()
        if not line.startswith("#")
    ]


REQUIRED = read_requirements("requirements.txt")

here = os.path.abspath(os.path.dirname(__file__))

try:
    with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

about = {}
if not VERSION:
    with open(os.path.join(here, FOLDER, "__version__.py")) as f:
        exec(f.read(), about)
else:
    about["__version__"] = VERSION


def package_files(directories):
    paths = []
    for item in directories:
        if isfile(item):
            paths.append(join("..", item))
            continue
        for path, directories, filenames in walk(item):
            for filename in filenames:
                paths.append(join("..", path, filename))
    return paths


class UploadCommand(Command):
    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds…")
            rmtree(os.path.join(here, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution…")
        os.system("{0} setup.py sdist bdist_wheel --universal".format(sys.executable))

        self.status("Uploading the package to PyPI via Twine…")
        os.system("twine upload dist/*")

        sys.exit()


setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url="https://sitoi.cn",
    project_urls={"Documentation": "https://sitoi.github.io/dailycheckin/"},
    packages=find_packages(exclude=("config",)),
    install_requires=REQUIRED,
    include_package_data=True,
    license="MIT",
    zip_safe=False,
    entry_points={"console_scripts": ["dailycheckin = dailycheckin.main:checkin"]},
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    cmdclass={"upload": UploadCommand},
)
