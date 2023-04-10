from typing import Dict

import numpy as np
from matplotlib import pyplot as plt

from src.model.skeleton_data import CoordinateData


class CoordinateDataDrawer:

    def __init__(self):
        pass

    @staticmethod
    def draw_local_pos(coordinate_data: CoordinateData, frame_skips: int = 5):

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        local_pos_min_list = []
        local_pos_max_list = []
        for local_pos in coordinate_data.local_pos_list:
            local_pos_min_list.append(np.amin([x for x in local_pos.values()], axis=0))
            local_pos_max_list.append(np.amax([x for x in local_pos.values()], axis=0))
        local_pos_max = np.amax(local_pos_max_list, axis=0)
        local_pos_min = np.amin(local_pos_min_list, axis=0)

        for i in range(0, len(coordinate_data.local_pos_list), frame_skips):

            local_pos: Dict[np.array] = coordinate_data.local_pos_list[i]
            for joint_name in coordinate_data.joint_names:
                if joint_name == coordinate_data.joint_names[0]: continue  # skip root joint
                parent_joint = coordinate_data.joints_hierarchy[joint_name][0]
                if parent_joint == "root": continue  # skip connect to root

                plt.plot(xs=[local_pos[parent_joint][0], local_pos[joint_name][0]],
                         zs=[local_pos[parent_joint][1], local_pos[joint_name][1]],
                         ys=[local_pos[parent_joint][2], local_pos[joint_name][2]], c='red', lw=2.5)

            # plot origin
            # plt.scatter(xs=[0, 0], zs=[0, 0], ys=[0, 0], c='green', lw=5)
            # ax.set_axis_off()
            ax.set_xlim(local_pos_min[0], local_pos_max[0])
            ax.set_ylim(local_pos_min[2], local_pos_max[2])
            ax.set_zlim(local_pos_min[1], local_pos_max[1])
            plt.title('frame: ' + str(i))
            plt.xlabel("x")
            plt.ylabel("y")
            # plt.zlabel("z")
            plt.pause(0.001)
            ax.cla()

        pass


    @staticmethod
    def draw_world_pos(coordinate_data: CoordinateData, frame_skips: int = 5):

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        world_pos_min_list = []
        world_pos_max_list = []
        for world_pos in coordinate_data.world_pos_list:
            world_pos_min_list.append(np.amin([x for x in world_pos.values()], axis=0))
            world_pos_max_list.append(np.amax([x for x in world_pos.values()], axis=0))
        world_pos_max = np.amax(world_pos_max_list, axis=0)
        world_pos_min = np.amin(world_pos_min_list, axis=0)

        for i in range(0, len(coordinate_data.world_pos_list), frame_skips):

            world_pos: Dict[np.array] = coordinate_data.world_pos_list[i]
            for joint_name in coordinate_data.joint_names:
                if joint_name == coordinate_data.joint_names[0]: continue  # skip root joint
                parent_joint = coordinate_data.joints_hierarchy[joint_name][0]
                if parent_joint == "root": continue  # skip connect to root

                plt.plot(xs = [world_pos[parent_joint][0], world_pos[joint_name][0]],
                         zs = [world_pos[parent_joint][1], world_pos[joint_name][1]],
                         ys = [world_pos[parent_joint][2], world_pos[joint_name][2]], c = 'blue', lw = 2.5)

            # plot origin
            # plt.scatter(xs=[0, 0], zs=[0, 0], ys=[0, 0], c='green', lw=5)

            # ax.set_axis_off()
            ax.set_xlim(world_pos_min[0], world_pos_max[0])
            ax.set_ylim(world_pos_min[2], world_pos_max[2])
            ax.set_zlim(world_pos_min[1], world_pos_max[1])
            plt.title('frame: ' + str(i))
            plt.xlabel("x")
            plt.ylabel("y")
            # plt.zlabel("z")
            plt.pause(0.001)
            ax.cla()

        pass
