import os
import threading
import tkinter
import tkinter as tk
from tkinter import ttk, filedialog
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

        # initial_processで定義される変数
        self.coordinate_drawer = None
        self.coordinate_anim = None
        self.graph_drawer_list = None
        self.graph_ax_list = None
        self.coordinate_ax = None
        self.fig = None
        self.graph_data_list = None
        self.coordinate_data = None

        self.file_name: str = "data/MCPM_20230410_150228.BVH"

        self.master = master
        master.title("BVH Motion Viewer")
        master.geometry("1080x720")

        # 初期化処理
        self._initial_process(file_name=self.file_name)

        # operation frame
        self.operation_frame = tk.Frame(master=master)
        self.operation_frame.pack(side=tk.BOTTOM)

        # file名の表示
        self.file_name_label = tk.Label(self.operation_frame, text=f"{os.path.basename(self.file_name)}")
        self.file_name_label.pack(side=tk.LEFT, padx=20, pady=5)

        # スライダーの初期化
        self.slider = ttk.Scale(self.operation_frame,
                                from_=0,
                                to=len(self.coordinate_data.local_pos_list) - 1,
                                orient="horizontal",
                                command=self.update_animation_and_graphs)
        self.slider.pack(side=tk.LEFT, padx=2, pady=5)

        # 再生ボタンの初期化
        self.play_button = tk.Button(self.operation_frame, text="再生", command=self.play)
        self.play_button.pack(side=tk.LEFT, padx=2, pady=5)

        # 停止ボタンの初期化
        self.stop_button = tk.Button(self.operation_frame, text="停止", command=self.stop)
        self.stop_button.pack(side=tk.LEFT, padx=2, pady=5)

        # 更新ボタンの初期化
        self.reload_bvh_button = tk.Button(self.operation_frame, text="他のファイルを開く", command=self._read_other_file)
        self.reload_bvh_button.pack(side=tk.LEFT, padx=2, pady=5)

        # グラフを描画するキャンバスの初期化
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side="left", fill="both", expand=True)

    def _read_other_file(self):
        file_path = filedialog.askopenfilename()
        file_ext = os.path.splitext(file_path)[-1]
        if file_ext not in [".BVH", ".bvh"]:
            tk.messagebox.showerror("エラー", "BVHファイルを選択してください")
            return
        if not os.path.exists(file_path):
            tk.messagebox.showerror("エラー", "ファイルが見つかりませんでした。")
            return

        # 正常なファイルの場合は読み込み、描画する
        self.reload_bvh(file_name=file_path)

    def _initial_process(self, file_name: str):
        """tkinterの画面関連以外の初期化処理"""

        # bvhファイルのローディング
        self.coordinate_data: CoordinateData = self.loading_bvh(file_name=file_name)

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

    def _clear_figure_canvas(self):
        for item in self.canvas.get_tk_widget().find_all():
            self.canvas.get_tk_widget().delete(item)
        self.canvas.get_tk_widget().destroy()

    def reload_bvh(self, file_name: str = "data/MCPM_20230410_150425.BVH"):
        print(f"reload bvh start")

        # ファイル名表示を更新
        self.file_name_label.config(text=f"{os.path.basename(file_name)}")

        # 描画を一度すべてクリアする
        self._clear_figure_canvas()

        # 再度グラフデータの読み込みや描画処理
        self._initial_process(file_name=file_name)

        # グラフを描画するキャンバスの初期化
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side="left", fill="both", expand=True)

        # スライダーのtoの値を更新
        self.slider.config(to=len(self.coordinate_data.local_pos_list) - 1)

    @staticmethod
    def loading_bvh(file_name: str):

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
