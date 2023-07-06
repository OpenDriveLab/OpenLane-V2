# ==============================================================================
# Binaries and/or source for the following packages or projects 
# are presented under one or more of the following open source licenses:
# bev.py    The OpenLane-V2 Dataset Authors    Apache License, Version 2.0
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

from .utils import THICKNESS, COLOR_DEFAULT, COLOR_DICT, interp_arc
from ...centerline.visualization.bev import _draw_vertex

BEV_SCALE = 10
BEV_RANGE = [-50, 50, -25, 25]


def _draw_line(image, line, with_attribute, with_linetype):

    assert not (with_attribute and with_linetype)

    points = np.array(line['points'])
    points = BEV_SCALE * (-points[:, :2] + np.array([BEV_RANGE[1] , BEV_RANGE[3]]))
    points = interp_arc(points)
    if points is None:
        return
    
    if with_attribute and len(set(line['attributes']) - set([0])):
        colors = [COLOR_DICT[a] for a in set(line['attributes']) - set([0])]
    elif with_linetype and line['linetype']:
        colors = [COLOR_DICT[line['linetype']]]
    else:
        colors = [COLOR_DEFAULT]
    
    for idx, color in enumerate(colors):
        for i in range(len(points) - 1):
            x1 = int(points[i][0] + idx * THICKNESS * 1.5)
            y1 = int(points[i][1] + idx * THICKNESS * 1.5)
            x2 = int(points[i+1][0] + idx * THICKNESS * 1.5)
            y2 = int(points[i+1][1] + idx * THICKNESS * 1.5)

            cv2.line(image, pt1=(y1, x1), pt2=(y2, x2), color=color, thickness=THICKNESS, lineType=cv2.LINE_AA)

def _draw_lane_segment(image, lane_segment, with_attribute, with_linetype, with_centerline, with_laneline):
    if with_centerline:
        _draw_line(image, {'points': lane_segment['centerline'], 'attributes': lane_segment['attributes']}, with_attribute, False)
        _draw_vertex(image, {'points': lane_segment['centerline']})
    if with_laneline:
        _draw_line(image, {'points': lane_segment['left_laneline'], 'linetype': lane_segment['left_laneline_type']}, False, with_linetype)
        _draw_line(image, {'points': lane_segment['right_laneline'], 'linetype': lane_segment['right_laneline_type']}, False, with_linetype)
        _draw_line(image, {'points': [lane_segment['left_laneline'][0], lane_segment['right_laneline'][0]]}, False, False)
        _draw_line(image, {'points': [lane_segment['left_laneline'][-1], lane_segment['right_laneline'][-1]]}, False, False)
    
        
def _draw_area(image, area, with_linetype):
    for start, end in zip(area['points'][:-1], area['points'][1:]):
        _draw_line(image, {'points': [start, end], 'linetype': area['category']}, False, with_linetype)

    for point in area['points']:
        point = BEV_SCALE * (-np.array([point])[:, :2] + np.array([BEV_RANGE[1] , BEV_RANGE[3]]))
        cv2.circle(image, (int(point[0, 1]), int(point[0, 0])), int(THICKNESS * 1.5), COLOR_DICT[area['category']], -1)

def draw_annotation_bev(annotation, with_attribute, with_linetype, with_centerline, with_laneline, with_area):
    image = np.ones((
        BEV_SCALE * (BEV_RANGE[1] - BEV_RANGE[0]),
        BEV_SCALE * (BEV_RANGE[3] - BEV_RANGE[2]),
        3,
    ), dtype=np.int32) * 191
    for lane_segment in annotation['lane_segment']:
        _draw_lane_segment(image, lane_segment, with_attribute, with_linetype, with_centerline, with_laneline)
    if with_area:
        for area in annotation['area']:
            _draw_area(image, area, with_linetype)
    return image
