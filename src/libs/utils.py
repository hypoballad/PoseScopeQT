import numpy as np
from scipy import linalg
from PySide6 import QtWidgets
from PySide6.QtGui import QImage, QPixmap
import cv2 as cv
import ctypes

#direct linear transform
def DLT(P1, P2, point1, point2):

    A = [point1[1]*P1[2,:] - P1[1,:],
         P1[0,:] - point1[0]*P1[2,:],
         point2[1]*P2[2,:] - P2[1,:],
         P2[0,:] - point2[0]*P2[2,:]
        ]
    A = np.array(A).reshape((4,4))
    #print('A: ')
    #print(A)

    B = A.transpose() @ A
    
    U, s, Vh = linalg.svd(B, full_matrices = False)

    #print('Triangulated point: ')
    #print(Vh[3,0:3]/Vh[3,3])
    return Vh[3,0:3]/Vh[3,3]

def display_test_pattern(label: QtWidgets.QLabel, height: int, width: int, txt: str, bw=False):
    # テストパターンを生成して表示
    if bw:
        pattern = generate_bw_noise_pattern(height, width)
    else:
        pattern = generate_test_pattern(height, width)
    placeholder_img_rgp = cv.cvtColor(pattern, cv.COLOR_BGR2RGB)
    img_rgb = cv.putText(placeholder_img_rgp, txt, (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv.LINE_AA)
    h, w = img_rgb.shape[:2]
    qimg = QImage(img_rgb, w, h, w*3, QImage.Format_RGB888)
    label.setPixmap(QPixmap(qimg))

def generate_test_pattern(height, width):
    # カラーノイズパターンを生成
    pattern = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)
    return pattern

def generate_bw_noise_pattern(height, width):
    # 白黒の砂嵐パターンを生成
    pattern = np.random.randint(0, 256, (height, width), dtype=np.uint8)
    pattern = cv.cvtColor(pattern, cv.COLOR_GRAY2BGR)
    return pattern

def rotate_frame(frame, rotation_angle):
    """現在の回転角度に基づいてフレームを回転"""
    if rotation_angle == 90:
        return cv.rotate(frame, cv.ROTATE_90_CLOCKWISE)
    elif rotation_angle == 180:
        return cv.rotate(frame, cv.ROTATE_180)
    elif rotation_angle == 270:
        return cv.rotate(frame, cv.ROTATE_90_COUNTERCLOCKWISE)
    return frame  # 0度の場合はそのまま

def fit_to_label(frame, width, height, rotation_angle, padding=True):
    """回転後のフレームを適切にリサイズし、左右に余白を追加してセンターに表示"""
    # h, w = frame.shape[:2]

    # if rotation_angle in [90, 270]:
    #     # 90° or 270°: 縦長の画像なので、高さをラベルにフィットさせ、横は余白を追加
    #     scale = height / h
    #     resized_w, resized_h = int(w * scale), height
    # else:
    #     # 0° or 180°: そのまま横をフィットさせる
    #     scale = width / w
    #     resized_w, resized_h = width, int(h * scale)

    resized_w, resized_h = get_resized_wh(frame, width, height, rotation_angle)

    frame_resized = cv.resize(frame, (resized_w, resized_h))

    if not padding:
        return frame_resized
    
    # # 余白の計算 (左右に余白を追加)
    # left = (width - resized_w) // 2
    # right = width - resized_w - left
    # top, bottom = 0, 0  # 上下の余白は追加しない

    # # 余白を追加してセンター配置
    # frame_padded = cv.copyMakeBorder(frame_resized, top, bottom, left, right, cv.BORDER_CONSTANT, value=[0, 0, 0])

    frame_padded = set_padding(frame_resized, width, resized_w)

    return frame_padded

def get_resized_wh(frame, width, height, rotation_angle):
    h, w = frame.shape[:2]

    if rotation_angle in [90, 270]:
        # 90° or 270°: 縦長の画像なので、高さをラベルにフィットさせ、横は余白を追加
        scale = height / h
        resized_w, resized_h = int(w * scale), height
    else:
        # 0° or 180°: そのまま横をフィットさせる
        scale = width / w
        resized_w, resized_h = width, int(h * scale)

    return resized_w, resized_h

def set_padding(frame, width, resized_w):
    left = (width - resized_w) // 2
    right = width - resized_w - left
    top, bottom = 0, 0  # 上下の余白は追加しない

    # 余白を追加してセンター配置
    frame_padded = cv.copyMakeBorder(frame, top, bottom, left, right, cv.BORDER_CONSTANT, value=[0, 0, 0])
    return frame_padded

def get_screen_resolution():
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    screen_width = user32.GetSystemMetrics(0) 
    screen_height = user32.GetSystemMetrics(1)
    return screen_width, screen_height

def get_R_x(theta):
    R = np.array([[1, 0, 0],
                  [0, np.cos(theta), -np.sin(theta)],
                  [0, np.sin(theta),  np.cos(theta)]])
    return R