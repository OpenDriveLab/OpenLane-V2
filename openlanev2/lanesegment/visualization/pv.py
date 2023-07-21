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

from .utils import THICKNESS, COLOR_DEFAULT, COLOR_DICT, interp_arc
from ...centerline.visualization.pv import _draw_traffic_element, _project, _draw_topology

    
def _draw_line(image, line, intrinsic, extrinsic, with_attribute, with_linetype):

    assert not (with_attribute and with_linetype)

    points = _project(interp_arc(line['points']), intrinsic, extrinsic)
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

            try:
                cv2.line(image, pt1=(x1, y1), pt2=(x2, y2), color=color, thickness=THICKNESS, lineType=cv2.LINE_AA)
            except Exception:
                return

def _draw_lane_segment(image, lane_segment, intrinsic, extrinsic, with_attribute, with_linetype, with_centerline, with_laneline):
    if with_centerline:
        _draw_line(image, {'points': lane_segment['centerline'], 'attributes': lane_segment['attributes']}, intrinsic, extrinsic, with_attribute, False)
    if with_laneline:
        _draw_line(image, {'points': lane_segment['left_laneline'], 'linetype': lane_segment['left_laneline_type']}, intrinsic, extrinsic, False, with_linetype)
        _draw_line(image, {'points': lane_segment['right_laneline'], 'linetype': lane_segment['right_laneline_type']}, intrinsic, extrinsic, False, with_linetype)
        _draw_line(image, {'points': np.array([lane_segment['left_laneline'][0], lane_segment['right_laneline'][0]])}, intrinsic, extrinsic, False, False)
        _draw_line(image, {'points': np.array([lane_segment['left_laneline'][-1], lane_segment['right_laneline'][-1]])}, intrinsic, extrinsic, False, False)

def _draw_area(image, area, intrinsic, extrinsic, with_linetype):
    for start, end in zip(area['points'][:-1], area['points'][1:]):
        _draw_line(image, {'points': np.array([start, end]), 'linetype': area['category']}, intrinsic, extrinsic, False, with_linetype)

    points = _project(interp_arc(area['points']), intrinsic, extrinsic)
    if points is None:
        return
    for point in points:
        cv2.circle(image, (int(point[0]), int(point[1])), int(THICKNESS * 1.5), COLOR_DICT[area['category']], -1)

def draw_annotation_pv(camera, image, annotation, intrinsic, extrinsic, with_attribute, with_linetype, with_topology, with_centerline, with_laneline, with_area):
    for lane_segment in annotation['lane_segment']:
        _draw_lane_segment(image, lane_segment, intrinsic, extrinsic, with_attribute, with_linetype, with_centerline, with_laneline)
    if with_area:
        for area in annotation['area']:
            _draw_area(image, area, intrinsic, extrinsic, with_linetype)
    if camera in ['ring_front_center', 'CAM_FRONT']:
        for traffic_element in annotation['traffic_element']:
            _draw_traffic_element(image, traffic_element)
        if with_topology:
            for topology in annotation['topology']:
                _draw_topology(image, topology, intrinsic, extrinsic)
    return image
