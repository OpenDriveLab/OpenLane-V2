# ==============================================================================
# Binaries and/or source for the following packages or projects 
# are presented under one or more of the following open source licenses:
# collect.py    The OpenLane-V2 Dataset Authors    Apache License, Version 2.0
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
from shapely.geometry import LineString, box

from ..io import io
from ...utils import SD_MAP_RANGE, SD_MAP_CATEGORY


def _fix_pts_interpolate(curve, n_points):
    ls = LineString(curve)
    distances = np.linspace(0, ls.length, n_points)
    curve = np.array([ls.interpolate(distance).coords[0] for distance in distances], dtype=np.float32)
    return curve


def collect(root_path : str, data_dict : dict, collection : str, with_sd_map : bool = False, n_points : dict = {}) -> None:
    r"""
    Load meta data of data in data_dict,
    and store in a .pkl with split as file name.

    Parameters
    ----------
    root_path : str
    data_dict : dict
        A dict contains ids of data to be preprocessed.
    collection : str
        Name of the collection.
    with_sd_map : bool
        Whether include SD Map for the SD Map as Prior Expansion.
    n_points : int
        Number of points that represent a curve.

    """
    data_list = [(split, segment_id, timestamp.split('.')[0]) \
        for split, segment_ids in data_dict.items() \
            for segment_id, timestamps in segment_ids.items() \
                for timestamp in timestamps
    ]
    meta = {
        (split, segment_id, timestamp): io.json_load(f'{root_path}/{split}/{segment_id}/info/{timestamp}-ls.json') \
            for split, segment_id, timestamp in data_list
    }

    for identifier, frame in tqdm(meta.items(), desc=f'collecting {collection}', ncols=80):
        for k, v in meta[identifier]['pose'].items():
            meta[identifier]['pose'][k] = np.array(v, dtype=np.float64)
        for camera in meta[identifier]['sensor'].keys():
            for para in ['intrinsic', 'extrinsic']:
                for k, v in meta[identifier]['sensor'][camera][para].items():
                    meta[identifier]['sensor'][camera][para][k] = np.array(v, dtype=np.float64)

        if 'annotation' not in frame:
            continue
        for i, area in enumerate(frame['annotation']['area']):
            meta[identifier]['annotation']['area'][i]['points'] = _fix_pts_interpolate(np.array(area['points']), n_points['area'])
        for i, lane_segment in enumerate(frame['annotation']['lane_segment']):
            meta[identifier]['annotation']['lane_segment'][i]['centerline'] = _fix_pts_interpolate(np.array(lane_segment['centerline']), n_points['centerline'])
            meta[identifier]['annotation']['lane_segment'][i]['left_laneline'] = _fix_pts_interpolate(np.array(lane_segment['left_laneline']), n_points['left_laneline'])
            meta[identifier]['annotation']['lane_segment'][i]['right_laneline'] = _fix_pts_interpolate(np.array(lane_segment['right_laneline']), n_points['right_laneline'])
        for i, traffic_element in enumerate(frame['annotation']['traffic_element']):
            meta[identifier]['annotation']['traffic_element'][i]['points'] = np.array(traffic_element['points'], dtype=np.float32)
        meta[identifier]['annotation']['topology_lsls'] = np.array(meta[identifier]['annotation']['topology_lsls'], dtype=np.int8)
        meta[identifier]['annotation']['topology_lste'] = np.array(meta[identifier]['annotation']['topology_lste'], dtype=np.int8)

        if with_sd_map:
            split, segment_id, timestamp = identifier
            sd_map = io.json_load(f'{root_path}/{split}/{segment_id}/sdmap.json')

            translation = meta[identifier]['pose']['translation'][:2]
            rotation = meta[identifier]['pose']['rotation'][:2, :2]

            meta[identifier]['sensor']['sd_map'] = {}
            for category in SD_MAP_CATEGORY:
                meta[identifier]['sensor']['sd_map'][category] = []
            for element in sd_map:
                road = element['points']
                road = (road - translation) @ rotation
                road = LineString(road).intersection(box(*SD_MAP_RANGE))
                if road.geom_type == 'MultiLineString':
                    for new_pts_single in road.geoms:
                        if new_pts_single.is_empty:
                            continue
                        line = np.array(new_pts_single.coords, dtype=np.float32)
                        meta[identifier]['sensor']['sd_map'][element['category']].append(line)
                elif not road.is_empty:
                    line = np.array(road.coords, dtype=np.float32)
                    meta[identifier]['sensor']['sd_map'][element['category']].append(line)

    io.pickle_dump(f'{root_path}/{collection}.pkl', meta)
