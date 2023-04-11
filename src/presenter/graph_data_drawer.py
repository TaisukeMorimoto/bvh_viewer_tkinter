from typing import Dict, List

import numpy as np
from matplotlib import pyplot as plt
import matplotlib
from src.model.skeleton_data import CoordinateData, GraphData, MultiPlotGraphData


class GraphDataDrawer:

    def __init__(self, ax, graph_data: GraphData, line_color: str = "r"):
        self.is_playing: bool = True
        self.ax = ax
        self.current_frame: int = 0
        self.graph_data: GraphData = graph_data
        self.line_color: str = line_color
        self.v_lines = None
        self.y_min: int
        self.y_max: int
        self._set_y_lim(graph_data)

    def _set_y_lim(self, graph_data: GraphData):
        self.y_min = min(graph_data.data)
        self.y_max = max(graph_data.data)

    def clear(self):
        """描画のクリア
        """
        self.ax.cla()

    def draw_graph_data_at_specific_frame(self, frame: int):
        """特定のフレーム時のグラフデータを描画
        """
        self.current_frame = frame
        self.clear()
        self.ax.set_title(self.graph_data.display_name)
        self.ax.xaxis.set_visible(False)
        self.ax.plot(self.graph_data.data, self.line_color)
        self.v_lines = self.ax.vlines(frame, ymin=self.y_min, ymax=self.y_max, colors="k")

    def update_graph_data_at_specific_frame(self, frame: int):
        """特定のフレーム時のグラフデータを描画
        """
        self.current_frame = frame
        self.v_lines.set_segments([np.array([[frame, self.y_min], [frame, self.y_max]])])


class MultiPlotGraphDataDrawer(GraphDataDrawer):
    def __init__(self, ax, multi_graph_data: MultiPlotGraphData):
        super().__init__(ax, multi_graph_data)
        self.graph_data: MultiPlotGraphData = multi_graph_data
        self.line_colors: List[str] = ["m", "c"]

    def _set_y_lim(self, graph_data: MultiPlotGraphData):
        self.y_min = min([min(graph_data.data[0]), min(graph_data.data[1])])
        self.y_max = max([max(graph_data.data[0]), max(graph_data.data[1])])

    def draw_graph_data_at_specific_frame(self, frame: int):
        """特定のフレーム時のグラフデータを描画
        """
        self.current_frame = frame
        self.clear()
        self.ax.set_title(self.graph_data.display_name)
        self.ax.xaxis.set_visible(False)
        for i, line_data in enumerate(self.graph_data.data):
            self.ax.plot(line_data, self.line_colors[i], label=self.graph_data.legends[i])
        self.v_lines = self.ax.vlines(frame, ymin=self.y_min, ymax=self.y_max, colors="k")
        self.ax.legend()
