import sys
import numpy as np
import matplotlib.pyplot as plt
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from mpl_toolkits.mplot3d import Axes3D
from libs.utils import get_R_z

class Matplotlib3DWidget(QWidget):
    def __init__(self, parent=None, pose_keypoints=[]):
        super(Matplotlib3DWidget, self).__init__(parent)
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111, projection='3d')

        # layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)

        self.pose_context()
        self.update_plot(initial_data())

    # Visualize with temporary pose indices
    def pose_context(self):
        self.torso = [[0, 1] , [1, 7], [7, 6], [6, 0]]
        self.armr = [[1, 3], [3, 5]]
        self.arml = [[0, 2], [2, 4]]
        self.legr = [[6, 8], [8, 10]]
        self.legl = [[7, 9], [9, 11]]
        self.body = [self.torso, self.arml, self.armr, self.legr, self.legl]
        self.colors = ['red', 'blue', 'green', 'black', 'orange']

    def update_plot(self, p3ds):
        self.ax.clear()

        # 座標系を調整するためにデータを変換
        #p3ds[:, [0, 1]] = p3ds[:, [1, 0]]  # x軸とy軸を入れ替える
        #p3ds[:, 2] = -p3ds[:, 2]  # z軸を反転させる
        # 座標系を調整するためにデータを変換
        #p3ds = p3ds[:, [2, 0, 1]]  # y->z, x->y, z->x に変換
        p3ds[:, 0] = -p3ds[:, 0]  # y軸を反転
        #p3ds[:, 2] = -p3ds[:, 2]
        # x軸を反転
        #p3ds[:, 0] = -p3ds[:, 0]
        R = get_R_z(np.pi/2)
        p3ds = R @ p3ds

        for bodypart, part_color in zip(self.body, self.colors):
            for _c in bodypart:
                # print(f"p3ds[_c[0],0]: {p3ds[_c[0],0]}- p3ds[_c[1],0]: {p3ds[_c[1],0]}")
                # print(f"p3ds[_c[0],1]: {p3ds[_c[0],1]}- p3ds[_c[1],1]: {p3ds[_c[1],1]}")
                # print(f"p3ds[_c[0],2]: {p3ds[_c[0],2]}- p3ds[_c[1],2]: {p3ds[_c[1],2]}")
                self.ax.plot(xs = [p3ds[_c[0],0], p3ds[_c[1],0]], ys = [p3ds[_c[0],1], p3ds[_c[1],1]], zs = [p3ds[_c[0],2], p3ds[_c[1],2]], linewidth = 4, c = part_color)

        # 軸の比率を統一
        #self.ax.set_box_aspect([1, 1, 1])

        # 視点の角度調整
        #ax.view_init(elev=60, azim=-45
        # カメラの視点を設定
        #self.ax.view_init(elev=60, azim=-270)  # 例として仰角30度、方位角180度に設定

        x_min, x_max = np.min(p3ds[:, 0]), np.max(p3ds[:, 0])
        y_min, y_max = np.min(p3ds[:, 1]), np.max(p3ds[:, 1])
        z_min, z_max = np.min(p3ds[:, 2]), np.max(p3ds[:, 2])

        # Add some padding to the limits
        padding = 10  # Adjust this value as needed
        x_min, x_max = x_min - padding, x_max + padding
        y_min, y_max = y_min - padding, y_max + padding
        z_min, z_max = z_min - padding, z_max + padding

        #ax.set_axis_off()
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_zticks([])

        self.ax.set_xlim3d(x_min, x_max)
        self.ax.set_xlabel('x')
        self.ax.set_ylim3d(y_min, y_max)
        self.ax.set_ylabel('y')
        self.ax.set_zlim3d(z_min, z_max)
        self.ax.set_zlabel('z')

        # Show the plot
        #self.ax.view_init(elev=90, azim=-90)

        self.canvas.draw()

def initial_data():
    # 初期データをプロット
    initial_data = np.array([
        [-9.81378778e+00, -1.24372782e+01,  7.32440659e+01],
        [-1.64275751e+01, -7.45205382e+00,  6.33793068e+01],
        [-1.10910598e+01, -6.99648844e+00,  7.78467957e+01],
        [-2.10451824e+01, -2.94512661e-02,  6.15220600e+01],
        [-8.42691311e+00, -2.10616607e+00,  7.80126077e+01],
        [-2.06730016e+01,  7.47726705e+00,  5.89097405e+01],
        [-1.37142256e+01,  3.80347145e+00,  7.64230344e+01],
        [-1.71672077e+01,  6.02623089e+00,  6.89905823e+01],
        [-9.19240959e+00,  1.15623532e+01,  7.43161194e+01],
        [-1.58462378e+01,  1.54214672e+01,  6.98437437e+01],
        [-1.18937695e+01,  2.15897357e+01,  7.87119709e+01],
        [-1.47568446e+01,  2.36223011e+01,  7.19959216e+01]
    ])
    initial_data = np.reshape(initial_data, (12, 3))
    return initial_data