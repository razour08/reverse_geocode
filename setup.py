import os
from setuptools import setup


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename), encoding='utf-8').read()


setup(
    name="reverse_geocode",
    version="2.0.0",
    packages=["reverse_geocode"],
    package_dir={"reverse_geocode": "reverse_geocode"},
    package_data={"reverse_geocode": ["countries.csv", "geocode.gz"]},
    author="Ramzi Dekali",
    author_email="",
    description="Reverse geocode coordinates to Arabic city and country names",
    long_description=read("README.md"),
    long_description_content_type='text/markdown',
    url="https://github.com/razour08/reverse_geocode",
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Natural Language :: Arabic",
        "Topic :: Scientific/Engineering :: GIS",
    ],
    license="lgpl",
    install_requires=["numpy", "scipy"],
    python_requires=">=3.7",
)
