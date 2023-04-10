from src.interface.bvh_reader import BvhReader
from src.model.skeleton_data import SkeletonData


class TestBvhReader:

    def test_read(self):
        file_name: str = "test/data/MCPM_20230410_150228.BVH"
        reader: BvhReader = BvhReader(file_name)
        skeleton_data: SkeletonData = reader.create_skeleton_data()

        assert len(skeleton_data.joints_names) == 27
        assert len(skeleton_data.joints_rotations)
        assert len(skeleton_data.joints_hierarchy)
