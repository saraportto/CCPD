from setuptools import setup
from Cython.Build import cythonize
import numpy

setup(
    ext_modules = cythonize("ej2_SumaRiemann_Cython.pyx"),
    include_dirs=[numpy.get_include()]
)

# python setup.py build_ext --inplace
