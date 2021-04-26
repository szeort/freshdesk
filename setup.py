"""
Setuptools package definition
"""
from setuptools import find_packages, setup

VERSION = open("version.txt").read().rstrip()
REQUIRES = list(open("requirements.txt"))
DEV_REQUIRES = list(open("requirements-dev.txt"))


setup(
    name="freshdesk",
    version=VERSION,
    description="Freshdesk client sdk for python",
    author="Samir Zeort",
    url="https://github.com/szeort/flashdesk",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    entry_points={
        "console_scripts": ['copy-user=flashdesk.sync:main']
    },
    license="GPL",
    install_requires=REQUIRES,
    extras_require={"dev": DEV_REQUIRES},
    classifiers=["Programming Language :: Python"],
    test_suite="test",
)
