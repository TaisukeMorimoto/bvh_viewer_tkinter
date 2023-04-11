import json
from dataclasses import asdict

from icecream import ic

from src.interface.bvh_reader import BvhReader
from src.model.skeleton_data import SkeletonData, CoordinateData
from src.service.coordinate_data_converter import CoordinateDataConverter


class TestCoordinateDataConverter:

    def test_convert(self):

        # given
        # 本来は下記のようにjsonから読み込みたい。
        # json_file_path = "test/data/MCPM_20230410_150228_skeleton.json"
        # with open(json_file_path) as f:
        #     json_data = json.load(f)
        # skeleton_data_schema = SkeletonData.schema()
        # skeleton_data: SkeletonData = skeleton_data_schema.loads(json_data)

        file_name: str = "test/data/MCPM_20230410_150228.BVH"
        reader: BvhReader = BvhReader(file_name)
        skeleton_data: SkeletonData = reader.create_skeleton_data()

        # when
        coordinate_data: CoordinateData \
            = CoordinateDataConverter().convert_to_coordinate_data(skeleton_data=skeleton_data)

        # then
        assert len(coordinate_data.world_pos_list)
        assert len(coordinate_data.local_pos_list)
        assert len(coordinate_data.joints_hierarchy)
        assert len(coordinate_data.joint_names) == 27

        json_file_path = "test/data/MCPM_20230410_150228_coordinate.json"
        with open(json_file_path, mode="wt", encoding="utf-8") as f:
            json.dump(coordinate_data.to_json(), f, ensure_ascii=False, indent=4)
