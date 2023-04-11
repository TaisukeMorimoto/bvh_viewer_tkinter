import json

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

        # dump時に「TypeError: Object of type float32 is not JSON serializable」となるためコメントアウト
        # json_file_path = "test/data/MCPM_20230410_150228_skeleton.json"
        # skeleton_data_schema = SkeletonData.schema()
        # with open(json_file_path, mode="wt", encoding="utf-8") as f:
        #     json.dump(skeleton_data_schema.dumps(skeleton_data), f, ensure_ascii=False, indent=4)
