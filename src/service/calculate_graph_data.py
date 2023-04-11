from typing import Dict, List

import numpy as np
import pandas as pd

from src.model.skeleton_data import CoordinateData, GraphData, MultiPlotGraphData


def angle_between_vectors(pos_list: List[Dict[str, np.array]],
                          origin_joint_name: str,
                          a_joint_name: str,
                          b_joint_name: str):
    """２つのベクトルのなす角度 (3次元)
    """
    # arccosを利用しているので180度を越える場合に利用不可能
    origin_pos = np.array([x[origin_joint_name] for x in pos_list])
    a_pos = np.array([x[a_joint_name] for x in pos_list])
    b_pos = np.array([x[b_joint_name] for x in pos_list])

    vec_from_a_to_origin = a_pos - origin_pos
    vec_from_b_to_origin = b_pos - origin_pos

    # ベクトルa,bの内積を計算
    inner = np.array([np.dot(vec_a_i, vec_b_i) for vec_a_i, vec_b_i in zip(vec_from_a_to_origin, vec_from_b_to_origin)])

    # ベクトルa,bの大きさを計算
    norm_from_a_to_origin = np.linalg.norm(vec_from_a_to_origin, axis=1)
    norm_from_b_to_origin = np.linalg.norm(vec_from_b_to_origin, axis=1)

    norm_dot = norm_from_a_to_origin * norm_from_b_to_origin
    norm_dot = [data if data != 0 else 1 for data in norm_dot]

    # ベクトルa,bのなす角度を計算
    return np.rad2deg(np.arccos(inner / norm_dot))


def angle_between_vectors_2d(pos_list: List[Dict[str, np.array]],
                             origin_joint_name: str,
                             a_joint_name: str,
                             b_joint_name: str,
                             ax=None):
    # arccosを利用しているので180度を越える場合に利用不可能

    origin_pos = np.array([x[origin_joint_name] for x in pos_list])
    a_pos = np.array([x[a_joint_name] for x in pos_list])
    b_pos = np.array([x[b_joint_name] for x in pos_list])

    ax = [0, -1] if not ax else ax
    vec_from_a_to_origin = a_pos[:, ax] - origin_pos[:, ax]
    vec_from_b_to_origin = b_pos[:, ax] - origin_pos[:, ax]
    inner = np.array([np.dot(vec_a_i, vec_b_i) for vec_a_i, vec_b_i in zip(vec_from_a_to_origin, vec_from_b_to_origin)])
    norm_from_a_to_origin = np.linalg.norm(vec_from_a_to_origin, axis=1)
    norm_from_b_to_origin = np.linalg.norm(vec_from_b_to_origin, axis=1)
    norm_dot = norm_from_a_to_origin * norm_from_b_to_origin
    norm_dot = [data if data != 0 else 1 for data in norm_dot]
    return np.rad2deg(np.arccos(inner / norm_dot))


class CalculateGraphData:

    def __init__(self):
        pass

    @staticmethod
    def calculate_head_y_position(coordinate_data: CoordinateData) -> GraphData:
        """頭の位置"""
        head_z = [x["head"][1] for x in coordinate_data.local_pos_list]
        return GraphData(data=head_z, display_name="Head position (z-axis) [cm]", graph_key="head_pos_z")

    @staticmethod
    def calculate_body_speed(coordinate_data: CoordinateData) -> GraphData:
        """身体(torso_1)のスピード"""
        torso_1_pos = np.array([x["torso_1"] for x in coordinate_data.world_pos_list])
        torso_1_pos_m = torso_1_pos * 0.01  # cm to meter
        df_pos = pd.DataFrame(torso_1_pos_m, columns=["x", 'y', "z"])
        window = 10
        df_pos = df_pos.rolling(window=window, center=True).mean()
        df_vel = (df_pos - df_pos.shift(1)) * coordinate_data.fps
        df_vel.fillna(method='bfill', inplace=True)
        speed = (df_vel['x'] ** 2 + df_vel["y"] ** 2 + df_vel["z"] ** 2) ** 0.5

        return GraphData(data=speed, display_name="Body speed [m/s]", graph_key="body_speed")

    @staticmethod
    def calculate_knee_angles(coordinate_data: CoordinateData) -> MultiPlotGraphData:
        """膝関節角度"""
        l_knee_angle = angle_between_vectors(pos_list=coordinate_data.local_pos_list,
                                             origin_joint_name="l_low_leg",
                                             a_joint_name="l_foot",
                                             b_joint_name="l_up_leg")

        r_knee_angle = angle_between_vectors(pos_list=coordinate_data.local_pos_list,
                                             origin_joint_name="r_low_leg",
                                             a_joint_name="r_foot",
                                             b_joint_name="r_up_leg")

        return MultiPlotGraphData(
            data=[l_knee_angle, r_knee_angle],
            display_name="Knee angle [degree]",
            graph_key="knee_angle",
            legends=["left", "right"]
        )
