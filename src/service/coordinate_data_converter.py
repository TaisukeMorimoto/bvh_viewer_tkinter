import numpy as np

from src.model.skeleton_data import SkeletonData, CoordinateData


class CoordinateDataConverter:
    """skeleton_dataをcoordinate_dataに変換する"""

    def __init__(self):
        pass

    @staticmethod
    def Rx(ang, in_radians=False):
        """ rotation matrices
        """
        if not in_radians:
            ang = np.radians(ang)

        Rot_Mat = np.array([
            [1, 0, 0],
            [0, np.cos(ang), -1 * np.sin(ang)],
            [0, np.sin(ang), np.cos(ang)]
        ])
        return Rot_Mat

    @staticmethod
    def Ry(ang, in_radians=False):
        if not in_radians:
            ang = np.radians(ang)

        Rot_Mat = np.array([
            [np.cos(ang), 0, np.sin(ang)],
            [0, 1, 0],
            [-1 * np.sin(ang), 0, np.cos(ang)]
        ])
        return Rot_Mat

    @staticmethod
    def Rz(ang, in_radians=False):
        if not in_radians:
            ang = np.radians(ang)

        Rot_Mat = np.array([
            [np.cos(ang), -1 * np.sin(ang), 0],
            [np.sin(ang), np.cos(ang), 0],
            [0, 0, 1]
        ])
        return Rot_Mat

    def _get_rotation_chain(self, joint_channels, joint_rotations):
        """ the rotation matrices need to be chained according to the order in the file
        """

        # the rotation matrices are constructed in the order given in the file
        Rot_Mat = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])  # identity matrix 3x3
        order = ''
        index = 0
        for chan in joint_channels:  # if file saves xyz ordered rotations, then rotation matrix must be chained as R_x @ R_y @ R_z
            if chan[0].lower() == 'x':
                Rot_Mat = Rot_Mat @ self.Rx(joint_rotations[index])
                order += 'x'

            elif chan[0].lower() == 'y':
                Rot_Mat = Rot_Mat @ self.Ry(joint_rotations[index])
                order += 'y'

            elif chan[0].lower() == 'z':
                Rot_Mat = Rot_Mat @ self.Rz(joint_rotations[index])
                order += 'z'
            index += 1
        # print(order)
        return Rot_Mat

    def _calculate_frame_joint_positions_in_local_space(self, joints, joints_offsets, frame_joints_rotations,
                                                        joints_saved_angles, joints_hierarchy):

        local_positions = {}

        for joint in joints:

            # ignore root joint and set local coordinate to (0,0,0)
            if joint == joints[0]:
                local_positions[joint] = [0, 0, 0]
                continue

            connected_joints = joints_hierarchy[joint]
            connected_joints = connected_joints[::-1]
            connected_joints.append(
                joint)  # this contains the chain of joints that finally end with the current joint that we want the coordinate of.
            Rot = np.eye(3)
            pos = [0, 0, 0]
            for i, con_joint in enumerate(connected_joints):
                if i == 0:
                    pass
                else:
                    parent_joint = connected_joints[i - 1]
                    Rot = Rot @ self._get_rotation_chain(joints_saved_angles[parent_joint],
                                                    frame_joints_rotations[parent_joint])
                joint_pos = joints_offsets[con_joint]
                joint_pos = Rot @ joint_pos
                pos = pos + joint_pos

            local_positions[joint] = pos

        return local_positions

    def _calculate_frame_joint_positions_in_world_space(self, local_positions, root_position, root_rotation, saved_angles):

        world_pos = {}
        for joint in local_positions:
            pos = local_positions[joint]

            Rot = self._get_rotation_chain(saved_angles, root_rotation)
            pos = Rot @ pos

            pos = np.array(root_position) + pos
            world_pos[joint] = pos

        return world_pos

    def convert_to_coordinate_data(self, skeleton_data: SkeletonData) -> CoordinateData:
        """skeleton_dataをcoordinate_dataに変換する"""
        frame_joints_rotations = {en: [] for en in skeleton_data.joints_names}

        local_pos_list = []
        world_pos_list = []
        for i in range(0, len(skeleton_data.joints_rotations)):

            frame_data = skeleton_data.joints_rotations[i]

            # fill in the rotations dict
            joint_index = 0
            for joint_name in skeleton_data.joints_names:
                frame_joints_rotations[joint_name] = frame_data[joint_index:joint_index + 3]
                joint_index += 3

            # this returns a dictionary of joint positions in local space. This can be saved to file to get the joint positions.
            local_pos = self._calculate_frame_joint_positions_in_local_space(skeleton_data.joints_names,
                                                                        skeleton_data.joints_offsets,
                                                                        frame_joints_rotations,
                                                                        skeleton_data.joints_saved_angles,
                                                                        skeleton_data.joints_hierarchy)
            local_pos_list.append(local_pos)

            # calculate world positions
            world_pos = self._calculate_frame_joint_positions_in_world_space(local_pos,
                                                                        skeleton_data.root_positions[i],
                                                                        frame_joints_rotations[skeleton_data.joints_names[0]],
                                                                        skeleton_data.joints_saved_angles[skeleton_data.joints_names[0]])
            world_pos_list.append(world_pos)

        return CoordinateData(world_pos_list=world_pos_list,
                              local_pos_list=local_pos_list,
                              joint_names=skeleton_data.joints_names,
                              joints_hierarchy=skeleton_data.joints_hierarchy,
                              fps=skeleton_data.fps)
