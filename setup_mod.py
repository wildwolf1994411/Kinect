import os
import glob
from distutils.core import setup
import py2exe
# Example:

setup(
    name="Sample",
    version="1.0",
    description="A sample app",
    author="Qi",
    console=['kinect_project.py'],
    data_files  = [],

    options={
            'py2exe': { 
            "includes": ["h5py.defs", "h5py.utils", "h5py._proxy", "h5py.h5ac", "sip", "matplotlib.backends",  "matplotlib.backends.backend_qt4agg",
                        "matplotlib.figure","pylab", "numpy","cPickle", "sklearn.utils.lgamma",
                        "matplotlib.backends.backend_tkagg", "PyQt5", "scipy.sparse.csgraph._validation","scipy", "scipy.integrate", "scipy.special.*","scipy.linalg.*"],

            "dll_excludes": ["MSVFW32.dll",
                            "AVIFIL32.dll",
                            "AVICAP32.dll",
                            "ADVAPI32.dll",
                            "CRYPT32.dll",
                            "WLDAP32.dll"]
            }}
)

# Will copy data/README to dist/README, and all files in data/images/ to dist/images/
# (not checking any subdirectories of data/images/)