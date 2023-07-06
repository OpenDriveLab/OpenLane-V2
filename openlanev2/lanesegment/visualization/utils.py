# ==============================================================================
# Binaries and/or source for the following packages or projects 
# are presented under one or more of the following open source licenses:
# utils.py    The OpenLane-V2 Dataset Authors    Apache License, Version 2.0
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

import numpy as np

from ...centerline.visualization.utils import interp_arc as interp_arc
from ...centerline.visualization.utils import THICKNESS as THICKNESS
from ...centerline.visualization.utils import COLOR_DEFAULT as COLOR_DEFAULT
from ...centerline.visualization.utils import COLOR_DICT as COLOR_DICT


def assign_attribute(annotation):
    topology_lste = np.array(annotation['topology_lste'], dtype=bool)
    for i in range(len(annotation['lane_segment'])):
        annotation['lane_segment'][i]['attributes'] = \
            set([ts['attribute'] for j, ts in enumerate(annotation['traffic_element']) if topology_lste[i][j]])
    return annotation

def assign_topology(annotation):
    topology_lste = np.array(annotation['topology_lste'], dtype=bool)
    annotation['topology'] = []
    for i in range(topology_lste.shape[0]):
        for j in range(topology_lste.shape[1]):
            if topology_lste[i][j]:
                annotation['topology'].append({
                    'lane_centerline': annotation['lane_segment'][i]['centerline'],
                    'traffic_element': annotation['traffic_element'][j]['points'],
                    'attribute': annotation['traffic_element'][j]['attribute'],
                })
    return annotation
