from typing import Dict, List

import numpy as np
from matplotlib import pyplot as plt

from src.model.skeleton_data import CoordinateData


class CoordinateDataDrawer:

    def __init__(self, ax, coordinate_data: CoordinateData):
        self.is_playing: bool = True
        self.ax = ax
        self.current_frame: int = 0
        self.coordinate_data: CoordinateData = coordinate_data
        self.local_pos_min, self.local_pos_max = self._calc_lim(pos_list=self.coordinate_data.local_pos_list)
        self.lines_dict: dict = {}

    @staticmethod
    def _calc_lim(pos_list: List[Dict[str, np.array]]):
        """軸の表示域の計算
        """
        local_pos_min_list = []
        local_pos_max_list = []
        for local_pos in pos_list:
            local_pos_min_list.append(np.amin([x for x in local_pos.values()], axis=0))
            local_pos_max_list.append(np.amax([x for x in local_pos.values()], axis=0))
        pos_max = np.amax(local_pos_max_list, axis=0)
        pos_min = np.amin(local_pos_min_list, axis=0)
        return pos_min, pos_max

    def clear(self):
        """描画のクリア
        """
        self.ax.cla()

    def draw_local_pos_at_initial_frame(self):
        """初回 0フレーム時のスティックピクチャーを描画
        """
        frame = 0
        self.current_frame = frame

        local_pos: Dict[np.array] = self.coordinate_data.local_pos_list[frame]
        for joint_name in self.coordinate_data.joint_names:
            if joint_name == self.coordinate_data.joint_names[0]: continue  # skip root joint
            parent_joint = self.coordinate_data.joints_hierarchy[joint_name][0]
            if parent_joint == "root": continue  # skip connect to root
            lines = self.ax.plot(xs=[local_pos[parent_joint][0], local_pos[joint_name][0]],
                                 zs=[local_pos[parent_joint][1], local_pos[joint_name][1]],
                                 ys=[local_pos[parent_joint][2], local_pos[joint_name][2]], c='red', lw=2.5)
            self.lines_dict[joint_name] = lines

        self.ax.set_title('frame: ' + str(frame))
        self.ax.set_xlim(self.local_pos_min[0], self.local_pos_max[0])
        self.ax.set_ylim(self.local_pos_min[2], self.local_pos_max[2])
        self.ax.set_zlim(self.local_pos_min[1], self.local_pos_max[1])
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.set_zlabel("z")
        self.ax.set_title('frame: ' + str(0))

    def draw_local_pos_at_specific_frame(self, frame: int):
        """特定のフレーム時のスティックピクチャーを描画
        """
        self.current_frame = frame
        local_pos: Dict[np.array] = self.coordinate_data.local_pos_list[frame]
        for joint_name in self.coordinate_data.joint_names:
            if joint_name == self.coordinate_data.joint_names[0]: continue  # skip root joint
            parent_joint = self.coordinate_data.joints_hierarchy[joint_name][0]
            if parent_joint == "root": continue  # skip connect to root

            lines = self.lines_dict[joint_name]
            lines[0].set_data_3d([local_pos[parent_joint][0], local_pos[joint_name][0]],
                                 [local_pos[parent_joint][2], local_pos[joint_name][2]],
                                 [local_pos[parent_joint][1], local_pos[joint_name][1]])

        self.ax.set_title('frame: ' + str(frame))
