import dataclasses
from typing import List, Dict

from dataclasses_json import dataclass_json
import numpy as np


@dataclass_json
@dataclasses.dataclass
class SkeletonData:
    """bvh形式のデータを加工し、扱いやすくした骨格データ。ここから座標値などを計算する"""
    joints_names: List[str]  # the names of the joints
    joints_offsets: Dict[str, np.array]  # the length of skeleton body parts
    joints_hierarchy: Dict[str, List[str]]  # the hierarchy of each joint
    root_positions: np.array  # frames[:, 0:3]
    joints_rotations: np.array  # the rotation angles
    joints_saved_angles: np.array # this contains channel information. E.g ['Xrotation', 'Yrotation', 'Zrotation']
    joints_positions: np.array
    joints_saved_positions: np.array
    fps: int


@dataclass_json
@dataclasses.dataclass
class CoordinateData:
    """SkeletonDataを座標系の位置情報に変換したもの"""
    world_pos_list: List[Dict[str, np.array]]  # 絶対座標系での位置情報  0=x, 1=z, 2=y
    local_pos_list: List[Dict[str, np.array]]  # ローカル座標系での位置情報
    joints_hierarchy: Dict[str, List[str]]  # the hierarchy of each joint
    joint_names: List[str]  # the names of the joints
    fps: int


@dataclasses.dataclass
class GraphData:
    """計算後のグラフデータ"""
    data: np.array
    display_name: str
    graph_key: str


@dataclasses.dataclass
class MultiPlotGraphData(GraphData):
    """計算後のグラフデータ"""
    data: List[np.array]
    display_name: str
    graph_key: str
    legends: List[str]
