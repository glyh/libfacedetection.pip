#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools.command.build_ext import build_ext
from setuptools.command.install import install
from pybind11.setup_helpers import Pybind11Extension

from glob import glob
import subprocess
import os
import platform
import sys
import shutil
import io

# with open(".version", "r") as f:
#     version = f.read().strip()
#     print(version)
#     version_tag = [int(x) for x in version.split('.')]
#     version_tag[-1] += 1
#     version = '.'.join([str(x) for x in version_tag])

# with open(".version", "w") as f:
#     f.write(version)
# __version__ = version

# 2023-5 first release
__version__ = '2024.9.27'

root_dir = os.path.dirname(os.path.abspath(__file__))

cmake_args = [
    '-DBUILD_SHARED_LIBS=ON',
    '-DDEMO=OFF',
    '-DUSE_OPENMP=ON'
]

ext_args = dict(        
    extra_link_args = [],
    define_macros = [('VERSION_INFO', __version__)],
    language='c++',
    cxx_std=11,
)

# linux
if sys.platform == "linux" or sys.platform == "linux2":
    if platform.uname()[4] == 'AMD64' or platform.uname()[4] == 'x86_64' or platform.uname()[4] == 'aarch64':
        cmake_args.append('-DENABLE_AVX2=ON')
        cmake_args.append('-DENABLE_AVX512=OFF')
        cmake_args.append('-DENABLE_NEON=OFF')
    else:
        cmake_args.append('-DENABLE_AVX2=OFF')
        cmake_args.append('-DENABLE_AVX512=OFF')
        cmake_args.append('-DENABLE_NEON=ON')
    ext_args['extra_link_args'].append('-Wl,-rpath=$ORIGIN')
    cmake_args.append('-DCMAKE_BUILD_TYPE=Release')

    
# windows
elif sys.platform == "win32":
    cmake_args.append('-DENABLE_AVX2=ON')
    cmake_args.append('-DENABLE_AVX512=OFF')
    cmake_args.append('-DENABLE_NEON=OFF')
    cmake_args.append('-DCMAKE_WINDOWS_EXPORT_ALL_SYMBOLS=TRUE')
slimeface_modules = [
    Pybind11Extension(
        "slimeface",
        ["src/main.cpp"],
        **ext_args
        ),
]

def copylibs(src, dst):
    if os.path.isdir(src):
        filelist = os.listdir(src)
        for file in filelist:
            libpath = os.path.join(src, file)
            shutil.copy2(libpath, dst)
    else:
        shutil.copy2(src, dst)

def build_submodule(ext:build_ext):
    src_dir = os.path.join(root_dir, 'libfacedetection')
    build_dir_submodule = os.path.join(os.path.abspath(ext.build_temp), 'libfacedetection')
    if not os.path.exists(build_dir_submodule):
        os.makedirs(build_dir_submodule)

    include_dir = os.path.join(build_dir_submodule, 'include')
    lib_dir = os.path.join(build_dir_submodule, 'lib')
    if not os.path.exists(include_dir):
        os.makedirs(include_dir)
    if not os.path.exists(lib_dir):
        os.makedirs(lib_dir)

    cmake_args.append('-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + lib_dir)
    subprocess.check_call(['cmake', '-S', src_dir] + cmake_args, cwd=build_dir_submodule)
    subprocess.check_call(['cmake', '--build', build_dir_submodule, '--config', 'Release'], cwd=build_dir_submodule)

    # copy header file
    if not os.path.exists(include_dir):
        os.makedirs(include_dir)
    export_header_file = glob(os.path.join(build_dir_submodule, '*.h'))[0]
    header_file = glob(os.path.join(src_dir, 'src', '*.h'))[0]
    shutil.copy2(export_header_file, os.path.join(include_dir, os.path.basename(export_header_file)))
    shutil.copy2(header_file, os.path.join(include_dir, os.path.basename(header_file)))
    if sys.platform == 'win32':
        copylibs(os.path.join(build_dir_submodule, 'Release'), lib_dir)

    ext.include_dirs.append(include_dir)
    ext.library_dirs.append(lib_dir)
    ext.libraries.append('facedetection')

class CustomBuildExt(build_ext):
    def run(self):
        build_submodule(self)
        build_ext.run(self)
        
        dst = os.path.join(self.build_lib, "slimeface")
        
        # copy dynamic libs
        copylibs(self.library_dirs[-1], dst)

        # move generated extension libs
        filelist = os.listdir(self.build_lib)
        for file in filelist:
            filePath = os.path.join(self.build_lib, file)
            if not os.path.isdir(filePath):
                copylibs(filePath, dst)
                os.remove(filePath)
        os.path.dirname
class CustomBuildExtDev(build_ext):
    def run(self):
        build_submodule(self)
        build_ext.run(self)

        dev_folder = os.path.join(os.path.dirname(__file__), "slimeface")

        # copy dynamic libs
        copylibs(self.library_dirs[-1], dev_folder)

        # move generated extension libs
        filelist = os.listdir(self.build_lib)
        for file in filelist:
            filePath = os.path.join(self.build_lib, file)
            if not os.path.isdir(filePath):
                copylibs(filePath, dev_folder)

class CustomInstall(install):
    def run(self):
        install.run(self)


long_description = io.open("README.md", encoding="utf-8").read()

setup(
    name="slimeface",
    keywords = ["face detection"],
    version = __version__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Wwupup",
    author_email="12032501@mail.sustech.edu.cn",
    url="https://github.com/ShiqiYu/libfacedetection.pip",
    description="A face detection library based on libfacedetection",
    license="./LISENCE",
    packages=["slimeface"],
    package_dir={"slimeface": "src/slimeface"},
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: C++",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Development Status :: 4 - Beta",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development",
        "Intended Audience :: Developers",
    ],
    ext_modules=slimeface_modules, 
    cmdclass={'build_ext': CustomBuildExt,
              'develop': CustomBuildExtDev,
              'install': CustomInstall}
)
