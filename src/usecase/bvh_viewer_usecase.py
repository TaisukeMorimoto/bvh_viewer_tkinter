import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.getcwd())
from src.interface.bvh_reader import BvhReader
from src.presenter.coordinate_data_drawer import CoordinateDataDrawer
from src.service.coordinate_data_converter import CoordinateDataConverter
from src.model.skeleton_data import SkeletonData, CoordinateData


class BvhViewerUsecase:
    """bvh形式のデータファイルを読み込み、位置情報に変換した上で時系列で描画する"""

    def __init__(self):
        pass

    @staticmethod
    def run():

        # file name読み込み
        if len(sys.argv) != 2:
            print('Call the function with the BVH file')
            quit()
        file_name = sys.argv[1]

        # bvh形式のデータを読み込み、スケルトンデータに変換する
        bvh_reader: BvhReader = BvhReader(file_name)
        skeleton_data: SkeletonData = bvh_reader.create_skeleton_data()

        # スケルトンデータをコーディネートデータ（位置情報）に変換する
        coordinate_data_converter: CoordinateDataConverter = CoordinateDataConverter()
        coordinate_data: CoordinateData = coordinate_data_converter.convert_to_coordinate_data(skeleton_data=skeleton_data)

        # コーディネートデータを時系列で描画
        CoordinateDataDrawer.draw_local_pos(coordinate_data=coordinate_data)


if __name__ == "__main__":
    BvhViewerUsecase.run()
