import numpy as np

from src.interface.parser import Bvh
from src.model.skeleton_data import SkeletonData


class BvhReader:

    def __init__(self, file_name: str):
        with open(file_name) as f:
            self.bvh_data: Bvh = Bvh(f.read())

    @staticmethod
    def _separate_angles(frames, joints, joints_saved_channels):

        frame_i = 0
        joints_saved_angles = {}
        get_channels = []
        for joint in joints:
            _saved_channels = joints_saved_channels[joint]

            saved_rotations = []
            for chan in _saved_channels:
                if chan.lower().find('rotation') != -1:
                    saved_rotations.append(chan)
                    get_channels.append(frame_i)

                frame_i += 1
            joints_saved_angles[joint] = saved_rotations

        joints_rotations = frames[:, get_channels]

        return joints_rotations, joints_saved_angles

    @staticmethod
    def _separate_positions(frames, joints, joints_saved_channels):

        frame_i = 0
        joints_saved_positions = {}
        get_channels = []
        for joint in joints:
            _saved_channels = joints_saved_channels[joint]

            saved_positions = []
            for chan in _saved_channels:
                if chan.lower().find('position') != -1:
                    saved_positions.append(chan)
                    get_channels.append(frame_i)

                frame_i += 1
            joints_saved_positions[joint] = saved_positions

        if len(get_channels) == 3 * len(joints):
            # print('all joints have saved positions')
            return frames[:, get_channels], joints_saved_positions

        # no positions saved for the joints or only some are saved.
        else:
            return np.array([]), joints_saved_positions

        pass

    def create_skeleton_data(self) -> SkeletonData:
        # get the names of the joints
        joints = self.bvh_data.get_joints_names()

        # this contains all frames data.
        frames = np.array(self.bvh_data.frames).astype('float32')

        # determine the structure of the skeleton and how the data was saved
        joints_offsets = {}
        joints_hierarchy = {}
        joints_saved_channels = {}
        for joint in joints:
            # get offsets. This is the length of skeleton body parts
            joints_offsets[joint] = np.array(self.bvh_data.joint_offset(joint))

            # Some bvh files save only rotation channels while others also save positions.
            # the order of rotation is important
            joints_saved_channels[joint] = self.bvh_data.joint_channels(joint)

            # determine the hierarcy of each joint.
            joint_hierarchy = []
            parent_joint = joint
            while True:
                parent_name = self.bvh_data.joint_parent(parent_joint)
                if parent_name is None: break

                joint_hierarchy.append(parent_name.name)
                parent_joint = parent_name.name

            joints_hierarchy[joint] = joint_hierarchy

        # seprate the rotation angles and the positions of joints
        joints_rotations, joints_saved_angles = self._separate_angles(frames, joints, joints_saved_channels)
        joints_positions, joints_saved_positions = self._separate_positions(frames, joints, joints_saved_channels)

        # root positions are always saved
        root_positions = frames[:, 0:3]

        return SkeletonData(joints_names=joints,
                            joints_offsets=joints_offsets,
                            joints_hierarchy=joints_hierarchy,
                            root_positions=root_positions,
                            joints_rotations=joints_rotations,
                            joints_saved_angles=joints_saved_angles,
                            joints_positions=joints_positions,
                            joints_saved_positions=joints_saved_positions,
                            fps=int(1/self.bvh_data.frame_time))
