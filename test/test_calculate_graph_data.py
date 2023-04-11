import json
from dataclasses import asdict
from typing import List

from icecream import ic
from matplotlib import pyplot as plt

from src.interface.bvh_reader import BvhReader
from src.model.skeleton_data import SkeletonData, CoordinateData, GraphData, MultiPlotGraphData
from src.presenter.graph_data_drawer import GraphDataDrawer, MultiPlotGraphDataDrawer
from src.service.calculate_graph_data import CalculateGraphData
from src.service.coordinate_data_converter import CoordinateDataConverter


class TestCalculateGraphData:

    def test_calculate_head_pos(self):

        # given
        json_file_path = "test/data/MCPM_20230410_150228_coordinate.json"
        with open(json_file_path) as f:
            json_data = json.load(f)
        coordinate_data_schema = CoordinateData.schema()
        coordinate_data: CoordinateData = coordinate_data_schema.loads(json_data)

        # when
        graph_data: GraphData \
            = CalculateGraphData.calculate_head_y_position(coordinate_data=coordinate_data)

        # then
        assert graph_data.display_name == "Head position (z-axis) [cm]"
        assert graph_data.graph_key == "head_pos_z"
        assert len(graph_data.data)

    def test_calculate_body_speed(self):

        # given
        json_file_path = "test/data/MCPM_20230410_150228_coordinate.json"
        with open(json_file_path) as f:
            json_data = json.load(f)
        coordinate_data_schema = CoordinateData.schema()
        coordinate_data: CoordinateData = coordinate_data_schema.loads(json_data)

        # when
        graph_data: GraphData \
            = CalculateGraphData.calculate_body_speed(coordinate_data=coordinate_data)

        # then
        assert graph_data.display_name == "Body speed [m/s]"
        assert graph_data.graph_key == "body_speed"
        assert len(graph_data.data)

        output_data = False
        if output_data:
            fig = plt.figure(figsize=(6, 6))
            ax = fig.add_subplot(111)
            drawer: GraphDataDrawer = GraphDataDrawer(ax=ax, graph_data=graph_data)
            drawer.draw_graph_data_at_specific_frame(frame=0)
            plt.show()

    def test_calculate_knee_angle(self):

        # given
        json_file_path = "test/data/MCPM_20230410_150228_coordinate.json"
        with open(json_file_path) as f:
            json_data = json.load(f)
        coordinate_data_schema = CoordinateData.schema()
        coordinate_data: CoordinateData = coordinate_data_schema.loads(json_data)

        # when
        multi_graph_data: MultiPlotGraphData \
            = CalculateGraphData.calculate_knee_angles(coordinate_data=coordinate_data)

        # then
        assert multi_graph_data.display_name == "Knee angle [degree]"
        assert multi_graph_data.graph_key == "knee_angle"
        assert len(multi_graph_data.data[0])
        assert len(multi_graph_data.data[1])

        output_data = False
        if output_data:
            fig = plt.figure(figsize=(6, 6))
            ax = fig.add_subplot(111)
            drawer: MultiPlotGraphDataDrawer = MultiPlotGraphDataDrawer(ax=ax, multi_graph_data=multi_graph_data)
            drawer.draw_graph_data_at_specific_frame(frame=0)
            plt.show()
