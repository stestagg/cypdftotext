import os
import platform
import subprocess
import sys
from setuptools import Extension
from setuptools import setup
try:
    from Cython.Build import cythonize
    HAVE_CYTHON = True
except ImportError:
    HAVE_CYTHON = False


include_dirs = ['lib/poppler/']
library_dirs = None


extra_compile_args = ["-Wall", '-fPIC', '-g']
extra_link_args = ['-g']

if platform.system() == "Darwin":
    extra_compile_args += ["-mmacosx-version-min=10.9", "-std=c++11"]
    extra_link_args += ["-mmacosx-version-min=10.9"]


if HAVE_CYTHON:
    cythonize('cypdftotext.pyx', language_level=3,)


module = Extension(
    "cypdftotext",
    sources=["cypdftotext.cpp"],
    libraries=["poppler-cpp"],
    include_dirs=include_dirs,
    library_dirs=library_dirs,
    extra_compile_args=extra_compile_args,
    extra_link_args=extra_link_args,
)

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="cypdftotext",
    version="3.0.0",
    author="Steve Stagg",
    author_email="stestagg@gmail.com",
    description="Cython port of a simple PDF text extraction library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sstagg/pdftotext-cython",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    ext_modules=[module],
    test_suite="tests",
)
