# ==============================================================================
# Binaries and/or source for the following packages or projects 
# are presented under one or more of the following open source licenses:
# pv.py    The OpenLane-V2 Dataset Authors    Apache License, Version 2.0
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

import cv2
import numpy as np

from .bev import BEV_SCALE, BEV_RANGE
from .utils import THICKNESS, COLOR_DICT
from ...utils import SD_MAP_RANGE

assert BEV_RANGE[0] == SD_MAP_RANGE[0] and BEV_RANGE[1] == SD_MAP_RANGE[2] \
    and BEV_RANGE[2] == SD_MAP_RANGE[1] and BEV_RANGE[3] == SD_MAP_RANGE[3]


def draw_sd_map(sd_map):
    image = np.ones((
        BEV_SCALE * (BEV_RANGE[1] - BEV_RANGE[0]),
        BEV_SCALE * (BEV_RANGE[3] - BEV_RANGE[2]),
        3,
    ), dtype=np.int32) * 191
    if sd_map is not None:
        for i, category in enumerate(sd_map):
            for road in sd_map[category]:
                road = (BEV_SCALE * (-road[:, :2] + np.array([BEV_RANGE[1] , BEV_RANGE[3]]))).astype(int)
                cv2.polylines(image, [road[:, [1,0]]], False, COLOR_DICT[i], THICKNESS * 10)
    return image
