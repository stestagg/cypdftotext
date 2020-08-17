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


include_dirs = None
library_dirs = None


# On some BSDs, poppler is in /usr/local, which is not searched by default
if platform.system() in ["Darwin", "FreeBSD", "OpenBSD"]:
    include_dirs = ["/usr/local/include"]
    library_dirs = ["/usr/local/lib"]


# On Windows, only building with conda is tested so far
if platform.system() == "Windows":
    conda_prefix = os.getenv("CONDA_PREFIX")
    if conda_prefix is not None:
        include_dirs = [os.path.join(conda_prefix, r"Library\include")]
        library_dirs = [os.path.join(conda_prefix, r"Library\lib")]


extra_compile_args = ["-Wall"]
extra_link_args = []

if HAVE_CYTHON:
    cythonize('cypdftotext.pyx', language_level=3)


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
