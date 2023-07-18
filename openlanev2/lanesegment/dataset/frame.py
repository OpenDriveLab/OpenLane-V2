# ==============================================================================
# Binaries and/or source for the following packages or projects 
# are presented under one or more of the following open source licenses:
# frame.py    The OpenLane-V2 Dataset Authors    Apache License, Version 2.0
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

from ...centerline.io import io


class Frame:
    r"""
    A data structure containing meta data of a frame.

    """
    def __init__(self, root_path : str, meta : dict) -> None:
        r"""
        Parameters
        ----------
        root_path : str
        meta : dict
            Meta data of a frame.

        """
        self.root_path = root_path
        self.meta = meta

    def get_camera_list(self) -> list:
        r"""
        Retuens a list of camera names.

        Returns
        -------
        list
            A list of str.

        """
        return list(self.meta['sensor'].keys())

    def get_pose(self) -> dict:
        r"""
        Retuens the pose of ego vehicle.

        Returns
        -------
        dict
            {'rotation': [3, 3], 'translation': [3, ]}.

        """
        return self.meta['pose']

    def get_image_path(self, camera : str) -> str:
        r"""
        Retuens the image path given a camera.

        Parameters
        ----------
        camera : str

        Returns
        -------
        str
            Image path.

        """
        return f'{self.root_path}/{self.meta["sensor"][camera]["image_path"]}'

    def get_rgb_image(self, camera : str) -> np.ndarray:
        r"""
        Retuens the RGB image given a camera.

        Parameters
        ----------
        camera : str

        Returns
        -------
        np.ndarray
            RGB Image.

        """
        image_path = self.get_image_path(camera)
        return cv2.cvtColor(io.cv2_imread(image_path), cv2.COLOR_BGR2RGB)
    
    def get_sd_map(self) -> np.ndarray:
        r"""
        Retuens the SD Map.

        Returns
        -------
        np.ndarray
            SD Map.

        """
        if 'sd_map' in self.meta['sensor']:
            return self.meta['sensor']['sd_map']
        else:
            raise Exception('The SD Map as Prior Expansion is required.')

    def get_intrinsic(self, camera : str) -> dict:
        r"""
        Retuens the intrinsic given a camera.

        Parameters
        ----------
        camera : str

        Returns
        -------
        dict
            {'K': [3, 3], 'distortion': [3, ]}.

        """
        return self.meta['sensor'][camera]['intrinsic']

    def get_extrinsic(self, camera : str) -> dict:
        r"""
        Retuens the extrinsic given a camera.

        Parameters
        ----------
        camera : str

        Returns
        -------
        dict
            {'rotation': [3, 3], 'translation': [3, ]}.

        """
        return self.meta['sensor'][camera]['extrinsic']

    def get_annotations(self) -> dict:
        r"""
        Retuens annotations of the current frame.

        Returns
        -------
        dict
            {'lane_segment': list, 'traffic_element': list, 'area': list, 'topology_lsls': list, 'topology_lste': list}.

        """
        if 'annotation' not in self.meta:
            return None
        else:
            return self.meta['annotation']

    def get_annotations_lane_segments(self) -> list:
        r"""
        Retuens lane segment annotations of the current frame.

        Returns
        -------
        list of dict

        """
        result = self.get_annotations()
        return result['lane_segment'] if result is not None else result

    def get_annotations_traffic_elements(self) -> list:
        r"""
        Retuens traffic element annotations of the current frame.

        Returns
        -------
        list of dict

        """
        result = self.get_annotations()
        return result['traffic_element'] if result is not None else result
    
    def get_annotations_areas(self) -> list:
        r"""
        Retuens area annotations of the current frame.

        Returns
        -------
        list of dict

        """
        result = self.get_annotations()
        return result['area'] if result is not None else result

    def get_annotations_topology_lsls(self) -> list:
        r"""
        Retuens the adjacent matrix of topology_lsls.

        Returns
        -------
        list
            [#lane_segment, #lane_segment].

        """
        result = self.get_annotations()
        return result['topology_lsls'] if result is not None else result

    def get_annotations_topology_lste(self) -> list:
        r"""
        Retuens the adjacent matrix of topology_lste.

        Returns
        -------
        list
            [#lane_segment, #traffic_element].
        
        """
        result = self.get_annotations()
        return result['topology_lste'] if result is not None else result
