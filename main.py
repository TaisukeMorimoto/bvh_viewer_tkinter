import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ウィンドウを作成
root = tk.Tk()

# フレームを作成してウィンドウに配置
frame = tk.Frame(root)
frame.pack(side=tk.BOTTOM)

# グラフの初期状態を作成
x = [1, 2, 3, 4, 5]
y = [1, 4, 9, 16, 25]

# フィギュアとサブプロットを作成
fig, ax = plt.subplots()

# ラインプロットを作成
line, = ax.plot(x, y)

# キャンバスを作成してウィンドウに配置
canvas = FigureCanvasTkAgg(fig, master=frame)
canvas.draw()
canvas.get_tk_widget().pack()


# スライダーのコールバック関数
def update(val):
    val = int(val)
    new_y = [i ** (val/10) for i in x]
    line.set_ydata(new_y)
    fig.canvas.draw_idle()


# スライダーを作成してウィンドウに配置
slider = tk.Scale(root, from_=1, to=50, orient=tk.HORIZONTAL, command=update)
slider.pack(side=tk.BOTTOM)

# ウィンドウを表示
tk.mainloop()
