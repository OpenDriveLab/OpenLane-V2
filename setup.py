# ==============================================================================
# Binaries and/or source for the following packages or projects 
# are presented under one or more of the following open source licenses:
# setup.py    The OpenLane-V2 Dataset Authors    Apache License, Version 2.0
#
# Contact wanghuijie@pjlab.org.cn if you have any issue.
#
# Copyright (c) 2023 The OpenLane-V2 Dataset Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

from setuptools import setup, find_packages


install_requires = [
    "tqdm",
    "ninja",
    "jupyter",
    "openmim",
    "matplotlib",
    "numpy >=1.22.0, <1.24.0",
    "scikit-learn",
    "similaritymeasures",
    "opencv-python",
    "scipy==1.8.0",
    "ortools==9.2.9972",
    "iso3166",
    "chardet",
    "shapely==2.0.0",
]

setup(
    name='openlanev2',
    version='2.1.0',
    author='The OpenLane-V2 Dataset Authors',
    author_email='wanghuijie@pjlab.org.cn',
    description='The official devkit of the OpenLane-V2 dataset.',
    url='https://github.com/OpenDriveLab/OpenLane-V2',
    install_requires=install_requires,
    packages=find_packages(),
    license='Apache License 2.0',
)
