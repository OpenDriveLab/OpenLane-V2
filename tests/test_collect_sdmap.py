import importlib
import json
import pickle
import sys
import types
from pathlib import Path

import numpy as np
import pytest


def _ensure_optional_deps(monkeypatch):
    if "cv2" not in sys.modules:
        try:
            importlib.import_module("cv2")
        except ImportError:
            monkeypatch.setitem(sys.modules, "cv2", types.ModuleType("cv2"))

    if "iso3166" not in sys.modules:
        try:
            importlib.import_module("iso3166")
        except ImportError:
            iso_mod = types.ModuleType("iso3166")
            iso_mod.countries = {}
            monkeypatch.setitem(sys.modules, "iso3166", iso_mod)

    if "shapely.geometry" not in sys.modules:
        try:
            importlib.import_module("shapely.geometry")
        except ImportError:
            shapely_mod = types.ModuleType("shapely")
            geom_mod = types.ModuleType("shapely.geometry")

            class _Box:
                def __init__(self, minx, miny, maxx, maxy):
                    self.bounds = (minx, miny, maxx, maxy)

            class _LineString:
                def __init__(self, coords):
                    self.coords = [tuple(map(float, pt)) for pt in coords]
                    self.geom_type = "LineString"
                    self.is_empty = len(self.coords) == 0
                    self.geoms = []

                @property
                def length(self):
                    if len(self.coords) < 2:
                        return 0.0
                    arr = np.asarray(self.coords, dtype=np.float64)
                    return float(np.linalg.norm(np.diff(arr, axis=0), axis=1).sum())

                def interpolate(self, distance):
                    if len(self.coords) == 1 or self.length == 0.0:
                        return _LineString([self.coords[0]])
                    arr = np.asarray(self.coords, dtype=np.float64)
                    segs = np.linalg.norm(np.diff(arr, axis=0), axis=1)
                    remaining = float(distance)
                    for idx, seg_len in enumerate(segs):
                        if remaining <= seg_len or idx == len(segs) - 1:
                            ratio = 0.0 if seg_len == 0 else min(max(remaining / seg_len, 0.0), 1.0)
                            pt = arr[idx] + ratio * (arr[idx + 1] - arr[idx])
                            return _LineString([tuple(pt.tolist())])
                        remaining -= seg_len
                    return _LineString([self.coords[-1]])

                def intersection(self, clip_box):
                    minx, miny, maxx, maxy = clip_box.bounds
                    inside = [
                        pt for pt in self.coords
                        if minx <= pt[0] <= maxx and miny <= pt[1] <= maxy
                    ]
                    return _LineString(inside)

            geom_mod.LineString = _LineString
            geom_mod.box = _Box
            shapely_mod.geometry = geom_mod
            monkeypatch.setitem(sys.modules, "shapely", shapely_mod)
            monkeypatch.setitem(sys.modules, "shapely.geometry", geom_mod)


def _write_frame_fixture(root_path: Path, split: str, segment_id: str, timestamp: str, suffix: str, with_annotation: bool):
    info_dir = root_path / split / segment_id / "info"
    info_dir.mkdir(parents=True, exist_ok=True)
    frame = {
        "pose": {
            "translation": [1.0, 2.0, 0.0],
            "rotation": [
                [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 1.0],
            ],
        },
        "sensor": {
            "ring_front_center": {
                "intrinsic": {"K": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]], "distortion": [0.0]},
                "extrinsic": {"rotation": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]], "translation": [0.0, 0.0, 0.0]},
            }
        },
    }
    if with_annotation:
        if suffix == "":
            frame["annotation"] = {
                "lane_centerline": [{"points": [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]]}],
                "traffic_element": [{"points": [[0.0, 0.0], [1.0, 1.0]]}],
                "topology_lclc": [[1]],
                "topology_lcte": [[1]],
            }
        else:
            frame["annotation"] = {
                "area": [{"points": [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]]}],
                "lane_segment": [
                    {
                        "centerline": [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]],
                        "left_laneline": [[0.0, 1.0, 0.0], [1.0, 1.0, 0.0]],
                        "right_laneline": [[0.0, -1.0, 0.0], [1.0, -1.0, 0.0]],
                    }
                ],
                "traffic_element": [{"points": [[0.0, 0.0], [1.0, 1.0]]}],
                "topology_lsls": [[1]],
                "topology_lste": [[1]],
            }

    info_path = info_dir / f"{timestamp}{suffix}.json"
    info_path.write_text(json.dumps(frame), encoding="utf-8")

    sdmap = [
        {"category": "road", "points": [[1.0, 2.0], [11.0, 7.0]]},
    ]
    sdmap_path = root_path / split / segment_id / "sdmap.json"
    sdmap_path.write_text(json.dumps(sdmap), encoding="utf-8")


@pytest.mark.parametrize("with_annotation", [False, True])
def test_centerline_collect_includes_sd_map_without_annotation(tmp_path, monkeypatch, with_annotation):
    _ensure_optional_deps(monkeypatch)
    from openlanev2.centerline.preprocessing.collect import collect

    split = "test" if not with_annotation else "train"
    _write_frame_fixture(tmp_path, split, "00001", "1000", "", with_annotation=with_annotation)
    data_dict = {split: {"00001": ["1000.json"]}}

    collect(str(tmp_path), data_dict, f"{split}_sd", point_interval=1, with_sd_map=True)

    with open(tmp_path / f"{split}_sd.pkl", "rb") as f:
        meta = pickle.load(f)

    sensor = meta[(split, "00001", "1000")]["sensor"]
    assert "sd_map" in sensor
    assert len(sensor["sd_map"]["road"]) == 1
    np.testing.assert_allclose(sensor["sd_map"]["road"][0], np.array([[0.0, 0.0], [10.0, 5.0]], dtype=np.float32))


@pytest.mark.parametrize("with_annotation", [False, True])
def test_lanesegment_collect_includes_sd_map_without_annotation(tmp_path, monkeypatch, with_annotation):
    _ensure_optional_deps(monkeypatch)
    from openlanev2.lanesegment.preprocessing.collect import collect

    split = "test" if not with_annotation else "train"
    _write_frame_fixture(tmp_path, split, "00001", "1000", "-ls", with_annotation=with_annotation)
    data_dict = {split: {"00001": ["1000.json"]}}

    collect(
        str(tmp_path),
        data_dict,
        f"{split}_ls_sd",
        with_sd_map=True,
        n_points={"area": 4, "centerline": 4, "left_laneline": 4, "right_laneline": 4},
    )

    with open(tmp_path / f"{split}_ls_sd.pkl", "rb") as f:
        meta = pickle.load(f)

    sensor = meta[(split, "00001", "1000")]["sensor"]
    assert "sd_map" in sensor
    assert len(sensor["sd_map"]["road"]) == 1
    np.testing.assert_allclose(sensor["sd_map"]["road"][0], np.array([[0.0, 0.0], [10.0, 5.0]], dtype=np.float32))


def test_collect_omits_sd_map_when_disabled(tmp_path, monkeypatch):
    _ensure_optional_deps(monkeypatch)
    from openlanev2.centerline.preprocessing.collect import collect as collect_cl
    from openlanev2.lanesegment.preprocessing.collect import collect as collect_ls

    _write_frame_fixture(tmp_path, "test", "00001", "1000", "", with_annotation=False)
    _write_frame_fixture(tmp_path, "test", "00001", "1000", "-ls", with_annotation=False)
    data_dict = {"test": {"00001": ["1000.json"]}}

    collect_cl(str(tmp_path), data_dict, "test_cl_nosd", with_sd_map=False)
    collect_ls(str(tmp_path), data_dict, "test_ls_nosd", with_sd_map=False)

    with open(tmp_path / "test_cl_nosd.pkl", "rb") as f:
        meta_cl = pickle.load(f)
    with open(tmp_path / "test_ls_nosd.pkl", "rb") as f:
        meta_ls = pickle.load(f)

    assert "sd_map" not in meta_cl[("test", "00001", "1000")]["sensor"]
    assert "sd_map" not in meta_ls[("test", "00001", "1000")]["sensor"]
