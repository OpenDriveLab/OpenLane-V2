# ==============================================================================
# Binaries and/or source for the following packages or projects 
# are presented under one or more of the following open source licenses:
# distance.py    The OpenLane-V2 Dataset Authors    Apache License, Version 2.0
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
from scipy.spatial.distance import cdist, euclidean
from ...centerline.evaluation.distance import chamfer_distance, frechet_distance, iou_distance


def pairwise(xs: list, ys: list, distance_function: callable, mask: np.ndarray = None, relax: bool = False) -> np.ndarray:
    r"""
    Calculate pairwise distance.

    Parameters
    ----------
    xs : list
        List of data in shape (X, ).
    ys : list
        List of data in shape (Y, ).
    distance_function : callable
        Function that computes distance between two instance.
    mask : np.ndarray
        Boolean mask in shape (X, Y).
    relax : bool
        Relax the result based on distance to ego vehicle,
        for lane segment only.

    Returns
    -------
    np.ndarray
        Float in shape (X, Y),
        where array[i][j] denotes distance between instance xs[i] and ys[j].

    """
    result = np.ones((len(xs), len(ys)), dtype=np.float64) * 1024
    for i, x in enumerate(xs):
        if relax:
            ego_distance = min([euclidean(p, np.zeros_like(p)) for p in x['centerline']])
            relaxation_factor = max(0.5, 1 - 5e-3 * ego_distance)
        else:
            relaxation_factor = 1.0
        for j, y in enumerate(ys):
            if mask is None or mask[i][j]:
                result[i][j] = distance_function(x, y) * relaxation_factor
    return result


def area_distance(gt: dict, pred: dict) -> float:
    r"""
    Calculate Chamfer distance between areas.

    Parameters
    ----------
    gt : dict
    pred : dict

    Returns
    -------
    float
        Chamfer distance

    """
    return chamfer_distance(gt['points'], pred['points'])


def lane_segment_distance_c(gt: dict, pred: dict) -> float:
    r"""
    Calculate distance between lane segments using Chamfer distance,
    for filtering and accelaration.

    Parameters
    ----------
    gt : dict
    pred : dict

    Returns
    -------
    float
    
    """
    return chamfer_distance(gt['centerline'], pred['centerline'])


def lane_segment_distance(gt: dict, pred: dict) -> float:
    r"""
    Calculate distance between lane segments.

    Parameters
    ----------
    gt : dict
    pred : dict

    Returns
    -------
    float
    
    """
    gt_centerline, gt_left_laneline, gt_right_laneline = gt['centerline'], gt['left_laneline'], gt['right_laneline']
    pred_centerline, pred_left_laneline, pred_right_laneline = pred['centerline'], pred['left_laneline'], pred['right_laneline']
    return 0.5 * ( \
        frechet_distance(gt_centerline, pred_centerline) + \
        chamfer_distance(gt_left_laneline, pred_left_laneline) + \
        chamfer_distance(gt_right_laneline, pred_right_laneline))


def traffic_element_distance(gt: dict, pred: dict) -> float:
    r"""
    Calculate IoU distance between traffic elements.

    Parameters
    ----------
    gt : dict
    pred : dict

    Returns
    -------
    float
        IoU distance

    """
    return iou_distance(gt['points'], pred['points'])
