import time
import tkinter as tk
from tkinter import ttk
from typing import List

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from src.interface.bvh_reader import BvhReader
from src.model.skeleton_data import SkeletonData, CoordinateData, GraphData, MultiPlotGraphData
from src.presenter.coordinate_data_drawer import CoordinateDataDrawer
from src.presenter.graph_data_drawer import GraphDataDrawer, MultiPlotGraphDataDrawer
from src.presenter.loading_dialog import LoadingDialog
from src.service.calculate_graph_data import CalculateGraphData
from src.service.coordinate_data_converter import CoordinateDataConverter

graph_colors = ["r", "g", "b"]


class BvhMotionViewerApp:

    def __init__(self, master):

        self.master = master
        master.title("BVH Motion Viewer")
        master.geometry("1080x720")

        # bvhファイルのローディング
        self.coordinate_data: CoordinateData = self.loading_bvh()

        # グラフデータの計算
        self.graph_data_list: List[GraphData] = [
            CalculateGraphData.calculate_head_y_position(coordinate_data=self.coordinate_data),
            CalculateGraphData.calculate_knee_angles(coordinate_data=self.coordinate_data),
            CalculateGraphData.calculate_body_speed(coordinate_data=self.coordinate_data)
        ]

        # グラフの初期化(外枠)
        self.fig = plt.figure(figsize=(10, 5))
        self.coordinate_ax = self.fig.add_subplot(121, projection='3d')
        self.graph_ax_list = [self.fig.add_subplot(x) for x in [322, 324, 326]]

        # アニメーションの初期化
        self.coordinate_anim = None

        # スティックピクチャ描画用クラス
        self.coordinate_drawer: CoordinateDataDrawer = CoordinateDataDrawer(ax=self.coordinate_ax,
                                                                            coordinate_data=self.coordinate_data)
        # スティックピクチャ描画
        self.coordinate_drawer.draw_local_pos_at_initial_frame()

        # グラフ描画用クラス
        self.graph_drawer_list = []
        for i, graph_data in enumerate(self.graph_data_list):
            if isinstance(graph_data, MultiPlotGraphData):
                self.graph_drawer_list.append(MultiPlotGraphDataDrawer(ax=self.graph_ax_list[i],
                                                                       multi_graph_data=graph_data))
            elif isinstance(graph_data, GraphData):
                self.graph_drawer_list.append(GraphDataDrawer(ax=self.graph_ax_list[i],
                                                              graph_data=graph_data,
                                                              line_color=graph_colors[i]))
            else:
                print(graph_data)
                raise NotImplementedError(f"Unexpected instance type: {type(graph_data)}")

        # グラフ描画
        for drawer in self.graph_drawer_list:
            drawer.draw_graph_data_at_specific_frame(frame=0)

        # スライダーの初期化
        self.slider = ttk.Scale(master,
                                from_=0,
                                to=len(self.coordinate_data.local_pos_list),
                                orient="horizontal",
                                command=self.update_animation_and_graphs)
        self.slider.pack()

        # グラフを描画するキャンバスの初期化
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side="left", fill="both", expand=True)

        # 再生ボタンの初期化
        self.play_button = tk.Button(master, text="再生", command=self.play)
        self.play_button.pack()

        # 停止ボタンの初期化
        self.stop_button = tk.Button(master, text="停止", command=self.stop)
        self.stop_button.pack()

    @staticmethod
    def loading_bvh(file_name: str = "data/MCPM_20230410_150228.BVH"):

        # ローディング中の表示
        # dialog = LoadingDialog(self.master)

        # bvh形式のデータを読み込み、スケルトンデータに変換する
        print(f"start loading BVH data")
        print(f"file path: {file_name}")
        bvh_reader: BvhReader = BvhReader(file_name)
        skeleton_data: SkeletonData = bvh_reader.create_skeleton_data()

        # スケルトンデータをコーディネートデータ（位置情報）に変換する
        coordinate_data_converter: CoordinateDataConverter = CoordinateDataConverter()
        coordinate_data: CoordinateData \
            = coordinate_data_converter.convert_to_coordinate_data(skeleton_data=skeleton_data)

        # ローディング中の表示終了
        # dialog.close()
        print(f"finished to convert to coordinate data ")
        return coordinate_data

    def play(self):
        frame_skips = 3
        if self.coordinate_anim is None:
            self.coordinate_anim = FuncAnimation(self.fig,
                                                 self.update_animation_and_graphs,
                                                 frames=range(self.coordinate_drawer.current_frame,
                                                              len(self.coordinate_data.local_pos_list),
                                                              frame_skips),
                                                 interval=10,
                                                 repeat=True)
        else:
            self.coordinate_anim.event_source.start()
        self.canvas.draw_idle()

    def stop(self):
        if self.coordinate_anim is not None:
            self.play_button.config(text="再生")
            self.coordinate_anim.event_source.stop()

    def update_animation_and_graphs(self, frame):
        """frameに応じて再描画"""
        frame = int(float(frame))

        # 現在のフレームを更新
        self.coordinate_drawer.current_frame = frame

        # スティックピクチャのアップデート
        self.coordinate_drawer.draw_local_pos_at_specific_frame(frame=frame)

        # グラフのアップデート
        # 描画が重い場合は、下記をコメントアウトしてグラフのアップデートを制限することでやや軽くなる
        for drawer in self.graph_drawer_list:
            drawer.draw_graph_data_at_specific_frame(frame=frame)

        self.canvas.draw_idle()


root = tk.Tk()
app = BvhMotionViewerApp(root)
root.mainloop()
