# ==============================================================================
# Binaries and/or source for the following packages or projects 
# are presented under one or more of the following open source licenses:
# evaluate.py    The OpenLane-V2 Dataset Authors    Apache License, Version 2.0
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
from tqdm import tqdm

from .distance import pairwise, area_distance, lane_segment_distance, lane_segment_distance_c, traffic_element_distance
from ..io import io
# from ..preprocessing import check_results
from ...utils import TRAFFIC_ELEMENT_ATTRIBUTE, AREA_CATEGOTY

THRESHOLDS_AREA = [0.5, 1.0, 1.5]
THRESHOLDS_LANESEG = [1.0, 2.0, 3.0]
THRESHOLDS_TE = [0.75]
THRESHOLD_RELATIONSHIP_CONFIDENCE = 0.5


def _pr_curve(recalls, precisions):
    r"""
    Calculate average precision based on given recalls and precisions.

    Parameters
    ----------
    recalls : array_like
        List in shape (N, ).
    precisions : array_like
        List in shape (N, ).

    Returns
    -------
    float
        average precision
    
    Notes
    -----
    Adapted from https://github.com/Mrmoore98/VectorMapNet_code/blob/mian/plugin/datasets/evaluation/precision_recall/average_precision_gen.py#L12

    """
    recalls = np.asarray(recalls)[np.newaxis, :]
    precisions = np.asarray(precisions)[np.newaxis, :]

    num_scales = recalls.shape[0]
    ap = np.zeros(num_scales, dtype=np.float32)

    for i in range(num_scales):
        for thr in np.arange(0, 1 + 1e-3, 0.1):
            precs = precisions[i, recalls[i, :] >= thr]
            prec = precs.max() if precs.size > 0 else 0
            ap[i] += prec
    ap /= 11

    return ap[0]

def _tpfp(gts, preds, confidences, distance_matrix, distance_threshold):
    r"""
    Generate lists of tp and fp on given distance threshold.

    Parameters
    ----------
    gts : List
        List of groud truth in shape (G, ).
    preds : List
        List of predictions in shape (P, ).
    confidences : array_like
        List of float in shape (P, ).
    distance_matrix : array_like
        Distance between every pair of instances.
    distance_threshold : float
        Predictions are considered as valid within the distance threshold.

    Returns
    -------
    (array_like, array_like, array_like)
        (tp, fp, match) both in shape (P, ).

    Notes
    -----
    Adapted from https://github.com/Mrmoore98/VectorMapNet_code/blob/mian/plugin/datasets/evaluation/precision_recall/tgfg.py#L10.

    """
    assert len(preds) == len(confidences)

    num_gts = len(gts)
    num_preds = len(preds)

    tp = np.zeros((num_preds), dtype=np.float32)
    fp = np.zeros((num_preds), dtype=np.float32)
    idx_match_gt = np.ones((num_preds), dtype=int) * np.nan

    if num_gts == 0:
        fp[...] = 1
        return tp, fp, idx_match_gt
    if num_preds == 0:
        return tp, fp, idx_match_gt

    dist_min = distance_matrix.min(0)
    dist_idx = distance_matrix.argmin(0)

    confidences_idx = np.argsort(-np.asarray(confidences))
    gt_covered = np.zeros(num_gts, dtype=bool)
    for i in confidences_idx:
        if dist_min[i] < distance_threshold:
            matched_gt = dist_idx[i]
            if not gt_covered[matched_gt]:
                gt_covered[matched_gt] = True
                tp[i] = 1
                idx_match_gt[i] = matched_gt
            else:
                fp[i] = 1
        else:
            fp[i] = 1
    
    return tp, fp, idx_match_gt

def _inject(num_gt, pred, tp, idx_match_gt, confidence, distance_threshold, object_type):
    r"""
    Inject tp matching into predictions.

    Parameters
    ----------
    num_gt : int
        Number of ground truth.
    pred : dict
        Dict storing predictions for all samples,
        to be injected.
    tp : array_like
    idx_match_gt : array_like
    confidence : array_lick
    distance_threshold : float
        Predictions are considered as valid within the distance threshold.
    object_type : str
        To filter type of object for evaluation.

    """
    if tp.tolist() == []:
        pred[f'{object_type}_{distance_threshold}_idx_match_gt'] = []
        pred[f'{object_type}_{distance_threshold}_confidence'] = []
        pred[f'{object_type}_{distance_threshold}_confidence_thresholds'] = []
        return

    confidence = np.asarray(confidence)
    sorted_idx = np.argsort(-confidence)
    sorted_confidence = confidence[sorted_idx]
    tp = tp[sorted_idx]

    tps = np.cumsum(tp, axis=0)
    eps = np.finfo(np.float32).eps
    recalls = tps / np.maximum(num_gt, eps)

    taken = np.percentile(recalls, np.arange(10, 101, 10), method='closest_observation')
    taken_idx = {r: i for i, r in enumerate(recalls)}
    confidence_thresholds = sorted_confidence[np.asarray([taken_idx[t] for t in taken])]

    pred[f'{object_type}_{distance_threshold}_idx_match_gt'] = idx_match_gt
    pred[f'{object_type}_{distance_threshold}_confidence'] = confidence
    pred[f'{object_type}_{distance_threshold}_confidence_thresholds'] = confidence_thresholds

def _AP(gts, preds, distance_matrices, distance_threshold, object_type, filter, inject):
    r"""
    Calculate AP on given distance threshold.

    Parameters
    ----------
    gts : dict
        Dict storing ground truth for all samples.
    preds : dict
        Dict storing predictions for all samples.
    distance_matrices : dict
        Dict storing distance matrix for all samples.
    distance_threshold : float
        Predictions are considered as valid within the distance threshold.
    object_type : str
        To filter type of object for evaluation.
    filter : callable
        To filter objects for evaluation.
    inject : bool
        Inject or not.

    Returns
    -------
    float
        AP over all samples.

    """
    tps = []
    fps = []
    confidences = []
    num_gts = 0
    for token in gts.keys():
        gt = [gt for gt in gts[token][object_type] if filter(gt)]
        pred = [pred for pred in preds[token][object_type] if filter(pred)]
        confidence = [pred['confidence'] for pred in preds[token][object_type] if filter(pred)]
        filtered_distance_matrix = distance_matrices[token].copy()
        filtered_distance_matrix = filtered_distance_matrix[[filter(gt) for gt in gts[token][object_type]], :]
        filtered_distance_matrix = filtered_distance_matrix[:, [filter(pred) for pred in preds[token][object_type]]]
        tp, fp, idx_match_gt = _tpfp(
            gts=gt, 
            preds=pred, 
            confidences=confidence, 
            distance_matrix=filtered_distance_matrix, 
            distance_threshold=distance_threshold,
        )
        tps.append(tp)
        fps.append(fp)
        confidences.append(confidence)
        num_gts += len(gt)
        if inject:
            _inject(
                num_gt=len(gt),
                pred=preds[token],
                tp=tp,
                idx_match_gt=idx_match_gt,
                confidence=confidence,
                distance_threshold=distance_threshold,
                object_type=object_type,
            )

    confidences = np.hstack(confidences)
    sorted_idx = np.argsort(-confidences)
    tps = np.hstack(tps)[sorted_idx]
    fps = np.hstack(fps)[sorted_idx]

    if len(tps) == num_gts == 0:
        return np.float32(1)

    tps = np.cumsum(tps, axis=0)
    fps = np.cumsum(fps, axis=0)
    eps = np.finfo(np.float32).eps
    recalls = tps / np.maximum(num_gts, eps)
    precisions = tps / np.maximum((tps + fps), eps)
    return _pr_curve(recalls=recalls, precisions=precisions)

def _mAP_over_threshold(gts, preds, distance_matrices, distance_thresholds, object_type, filter, inject):
    r"""
    Calculate mAP over distance thresholds.

    Parameters
    ----------
    gts : dict
        Dict storing ground truth for all samples.
    preds : dict
        Dict storing predictions for all samples.
    distance_matrices : dict
        Dict storing distance matrix for all samples.
    distance_thresholds : list
        Distance thresholds.
    object_type : str
        To filter type of object for evaluation.
    filter : callable
        To filter objects for evaluation.
    inject : bool
        Inject or not.

    Returns
    -------
    list
        APs over all samples.

    """
    return np.asarray([_AP(
        gts=gts, 
        preds=preds, 
        distance_matrices=distance_matrices,
        distance_threshold=distance_threshold, 
        object_type=object_type,
        filter=filter,
        inject=inject,
    ) for distance_threshold in distance_thresholds])

def _average_precision_per_vertex(gts, preds, confidences):
    r"""
    Calculate average precision for a vertex.

    Parameters
    ----------
    gts : array_like
        List of vertices in shape (G, ).
    preds : array_like
        List of vertices in shape (P, ).
    confidences : array_like
        List of confidences in shape (P, ).

    Returns
    -------
    float
        AP for a vertex

    """
    assert len(np.unique(preds)) == len(preds) == len(confidences)

    num_gts = len(gts)
    num_preds = len(preds)

    tp = np.zeros((num_preds), dtype=np.float32)
    fp = np.zeros((num_preds), dtype=np.float32)

    if num_gts == num_preds == 0:
        return np.float32(1)
    if num_gts == 0 or num_preds == 0:
        return np.float32(0)
    else:
        gts = set(gts)
        confidences_idx = np.argsort(-confidences)
        preds = preds[confidences_idx]
        for i, pred in enumerate(preds):
            if pred in gts:
                tp[i] = 1
            else:
                fp[i] = 1

    rel = tp
    tp = np.cumsum(tp)
    fp = np.cumsum(fp)
    eps = np.finfo(np.float32).eps
    precisions = tp / np.maximum((tp + fp), eps)

    return np.dot(precisions, rel) / num_gts
    
def _AP_directerd(gts, preds):
    r"""
    Calculate average precision on the given adjacent matrices,
    where vertices are directedly connected.

    Parameters
    ----------
    gts : array_like
        List of float in shape (N, N).
    preds : array_like
        List of float in shape (N, N).

    Returns
    -------
    float
        mAP for directed graph

    """
    assert gts.shape[0] == gts.shape[1] == preds.shape[0] == preds.shape[1]

    indices = np.arange(gts.shape[0])

    acc = []

    # one direction
    for gt, pred in zip(gts, preds):
        gt = indices[gt.astype(bool)]
        confidence = pred[pred > THRESHOLD_RELATIONSHIP_CONFIDENCE]
        pred = indices[pred > THRESHOLD_RELATIONSHIP_CONFIDENCE]
        acc.append(_average_precision_per_vertex(gt, pred, confidence))

    # the other direction
    for gt, pred in zip(gts.T, preds.T):
        gt = indices[gt.astype(bool)]
        confidence = pred[pred > THRESHOLD_RELATIONSHIP_CONFIDENCE]
        pred = indices[pred > THRESHOLD_RELATIONSHIP_CONFIDENCE]
        acc.append(_average_precision_per_vertex(gt, pred, confidence))

    return acc

def _AP_undirecterd(gts, preds):
    r"""
    Calculate average precision on the given adjacent matrices,
    where vertices are undirectedly connected.

    Parameters
    ----------
    gts : array_like
        List of float in shape (X, Y).
    preds : array_like
        List of float in shape (X, Y).

    Returns
    -------
    float
        mAP for undirected graph

    """
    assert gts.shape[0] == preds.shape[0] and gts.shape[1] == preds.shape[1]

    acc = []

    indices = np.arange(gts.shape[1])
    for gt, pred in zip(gts, preds):
        gt = indices[gt.astype(bool)]
        confidence = pred[pred > THRESHOLD_RELATIONSHIP_CONFIDENCE]
        pred = indices[pred > THRESHOLD_RELATIONSHIP_CONFIDENCE]
        acc.append(_average_precision_per_vertex(gt, pred, confidence))
    
    indices = np.arange(gts.shape[0])
    for gt, pred in zip(gts.T, preds.T):
        gt = indices[gt.astype(bool)]
        confidence = pred[pred > THRESHOLD_RELATIONSHIP_CONFIDENCE]
        pred = indices[pred > THRESHOLD_RELATIONSHIP_CONFIDENCE]
        acc.append(_average_precision_per_vertex(gt, pred, confidence))

    return acc

def _mAP_topology_lsls(gts, preds, distance_thresholds):
    r"""
    Calculate mAP on topology among lane segments.

    Parameters
    ----------
    gts : dict
        Dict storing ground truth for all samples.
    preds : dict
        Dict storing predictions for all samples.
    distance_thresholds : list
        Distance thresholds.

    Returns
    -------
    float
        mAP over all samples abd distance thresholds.

    """
    acc = []
    for distance_threshold in distance_thresholds:
        for token in gts.keys():
            preds_topology_lsls_unmatched = preds[token]['topology_lsls']

            idx_match_gt = preds[token][f'lane_segment_{distance_threshold}_idx_match_gt']
            gt_pred = {m: i for i, m in enumerate(idx_match_gt) if not np.isnan(m)}

            gts_topology_lsls = gts[token]['topology_lsls']
            if 0 in gts_topology_lsls.shape:
                continue

            gt_indices = np.array(list(gt_pred.keys())).astype(int)
            pred_indices = np.array(list(gt_pred.values())).astype(int)
            preds_topology_lsls = np.ones_like(gts_topology_lsls, dtype=gts_topology_lsls.dtype) * np.nan
            xs = gt_indices[:, None].repeat(len(gt_indices), 1)
            ys = gt_indices[None, :].repeat(len(gt_indices), 0)
            preds_topology_lsls[xs, ys] = preds_topology_lsls_unmatched[pred_indices][:, pred_indices]
            preds_topology_lsls[np.isnan(preds_topology_lsls)] = (
                1 - gts_topology_lsls[np.isnan(preds_topology_lsls)]) * (0.5 + np.finfo(np.float32).eps)

            acc.append(_AP_directerd(gts=gts_topology_lsls, preds=preds_topology_lsls))

    if len(acc) == 0:
        return np.float32(0)
    return np.hstack(acc).mean()

def _mAP_topology_lste(gts, preds, distance_thresholds):
    r"""
    Calculate mAP on topology between lane segments and traffic elements.

    Parameters
    ----------
    gts : dict
        Dict storing ground truth for all samples.
    preds : dict
        Dict storing predictions for all samples.
    distance_thresholds : list
        Distance thresholds.

    Returns
    -------
    float
        mAP over all samples abd distance thresholds.

    """
    acc = []
    for distance_threshold_lane_segment in distance_thresholds['lane_segment']:
        for distance_threshold_traffic_element in distance_thresholds['traffic_element']:
            for token in gts.keys():
                preds_topology_lste_unmatched = preds[token]['topology_lste']

                idx_match_gt_lane_segment = preds[token][f'lane_segment_{distance_threshold_lane_segment}_idx_match_gt']
                gt_pred_lane_segment = {m: i for i, m in enumerate(idx_match_gt_lane_segment) if not np.isnan(m)}

                idx_match_gt_traffic_element = preds[token][f'traffic_element_{distance_threshold_traffic_element}_idx_match_gt']
                gt_pred_traffic_element = {m: i for i, m in enumerate(idx_match_gt_traffic_element) if not np.isnan(m)}

                gts_topology_lste = gts[token]['topology_lste']
                if 0 in gts_topology_lste.shape:
                    continue

                gt_indices_ls = np.array(list(gt_pred_lane_segment.keys())).astype(int)
                pred_indices_ls = np.array(list(gt_pred_lane_segment.values())).astype(int)
                gt_indices_te = np.array(list(gt_pred_traffic_element.keys())).astype(int)
                pred_indices_te = np.array(list(gt_pred_traffic_element.values())).astype(int)

                preds_topology_lste = np.ones_like(gts_topology_lste, dtype=gts_topology_lste.dtype) * np.nan
                xs = gt_indices_ls[:, None].repeat(len(gt_indices_te), 1)
                ys = gt_indices_te[None, :].repeat(len(gt_indices_ls), 0)
                preds_topology_lste[xs, ys] = preds_topology_lste_unmatched[pred_indices_ls][:, pred_indices_te]
                preds_topology_lste[np.isnan(preds_topology_lste)] = (
                    1 - gts_topology_lste[np.isnan(preds_topology_lste)]) * (0.5 + np.finfo(np.float32).eps)

                acc.append(_AP_undirecterd(gts=gts_topology_lste, preds=preds_topology_lste))

    if len(acc) == 0:
        return np.float32(0)
    return np.hstack(acc).mean()

def evaluate(ground_truth, predictions, verbose=True):
    r"""
    Evaluate the road structure cognition task.

    Parameters
    ----------
    ground_truth : str / dict
        Dict of ground truth of path to pickle file storing the dict.
    predictions : str / dict
        Dict of predictions of path to pickle file storing the dict.

    Returns
    -------
    dict
        A dict containing all defined metrics.

    Notes
    -----
    One of pred_path and pred_dict must be None,
    these two arguments provide flexibility for formatting the results only.

    """    
    if isinstance(ground_truth, str):
        ground_truth = io.pickle_load(ground_truth)

    if predictions is None:
        preds = {}
        print('\nDummy evaluation on ground truth.\n')
    else:
        if isinstance(predictions, str):
            predictions = io.pickle_load(predictions)
        # check_results(predictions) # check results format
        predictions = predictions['results']

    gts = {}
    preds = {}
    for token in ground_truth.keys():
        gts[token] = ground_truth[token]['annotation']
        if predictions is None:
            preds[token] = gts[token]
            for i, _ in enumerate(preds[token]['lane_segment']):
                preds[token]['lane_segment'][i]['confidence'] = np.float32(1)
            for i, _ in enumerate(preds[token]['area']):
                preds[token]['area'][i]['confidence'] = np.float32(1)
            for i, _ in enumerate(preds[token]['traffic_element']):
                preds[token]['traffic_element'][i]['confidence'] = np.float32(1)
        else:
            preds[token] = predictions[token]['predictions']

    assert set(gts.keys()) == set(preds.keys()), '#frame differs'

    """
        calculate distances between gts and preds    
    """

    distance_matrices = {
        'laneseg': {},
        'area': {},
        'iou': {},
    }

    for token in tqdm(gts.keys(), desc='calculating distances:', ncols=80, disable=not verbose):

        mask = pairwise(
            [gt for gt in gts[token]['lane_segment']],
            [pred for pred in preds[token]['lane_segment']],
            lane_segment_distance_c,
            relax=True,
        ) < THRESHOLDS_LANESEG[-1]

        distance_matrices['laneseg'][token] = pairwise(
            [gt for gt in gts[token]['lane_segment']],
            [pred for pred in preds[token]['lane_segment']],
            lane_segment_distance,
            mask=mask,
            relax=True,
        )

        distance_matrices['area'][token] = pairwise(
            [gt for gt in gts[token]['area']],
            [pred for pred in preds[token]['area']],
            area_distance,
        )

        distance_matrices['iou'][token] = pairwise(
            [gt for gt in gts[token]['traffic_element']],
            [pred for pred in preds[token]['traffic_element']],
            traffic_element_distance,
        )

    """
        evaluate
    """

    metrics = {
        'OpenLane-V2 UniScore': {},
        # 'Error': {},
    }

    """
        OpenLane-V2 UniScore
    """

    metrics['OpenLane-V2 UniScore']['DET_l'] = _mAP_over_threshold(
        gts=gts, 
        preds=preds, 
        distance_matrices=distance_matrices['laneseg'], 
        distance_thresholds=THRESHOLDS_LANESEG,
        object_type='lane_segment',
        filter=lambda _: True,
        inject=True, # save tp for eval on graph
    ).mean()

    metrics['OpenLane-V2 UniScore']['DET_a'] = np.hstack([_mAP_over_threshold(
        gts=gts, 
        preds=preds, 
        distance_matrices=distance_matrices['area'], 
        distance_thresholds=THRESHOLDS_AREA, 
        object_type='area',
        filter=lambda x: x['category'] == idx,
        inject=False,
    ) for idx in AREA_CATEGOTY.values()]).mean()

    metrics['OpenLane-V2 UniScore']['DET_t'] = np.hstack([_mAP_over_threshold(
        gts=gts, 
        preds=preds, 
        distance_matrices=distance_matrices['iou'], 
        distance_thresholds=THRESHOLDS_TE, 
        object_type='traffic_element',
        filter=lambda x: x['attribute'] == idx,
        inject=False,
    ) for idx in TRAFFIC_ELEMENT_ATTRIBUTE.values()]).mean()

    _mAP_over_threshold(
        gts=gts, 
        preds=preds, 
        distance_matrices=distance_matrices['iou'], 
        distance_thresholds=THRESHOLDS_TE, 
        object_type='traffic_element',
        filter=lambda _: True,
        inject=True, # save tp for eval on graph
    )
    metrics['OpenLane-V2 UniScore']['TOP_ll'] = _mAP_topology_lsls(gts, preds, THRESHOLDS_LANESEG)
    metrics['OpenLane-V2 UniScore']['TOP_lt'] = _mAP_topology_lste(
        gts,
        preds,
        {'lane_segment': THRESHOLDS_LANESEG, 'traffic_element': THRESHOLDS_TE},
    )

    metrics['OpenLane-V2 UniScore']['score'] = np.asarray([
        metrics['OpenLane-V2 UniScore']['DET_l'],
        metrics['OpenLane-V2 UniScore']['DET_a'],
        metrics['OpenLane-V2 UniScore']['DET_t'],
        np.sqrt(metrics['OpenLane-V2 UniScore']['TOP_ll']),
        np.sqrt(metrics['OpenLane-V2 UniScore']['TOP_lt']),
    ]).mean()

    return metrics
