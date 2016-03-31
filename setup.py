# setup.py
# configures package for installation

from setuptools import setup

setup(name="docxchanges",
      version=0.1,
      description="an unpacker for docx files that extracts tracked changes",
      url="https://github.com/electroducer/docxchanges",
      author="Jonas Robertson",
      author_email="jonas.robertson@gmail.com",
      license="MIT",
      packages=["docxchanges"],
      zip_safe=False)