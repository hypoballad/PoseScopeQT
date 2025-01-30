from .cameracalibration_controller import CameraInitializationThread
from .stereocalibration_controller import get_projection_matrix
from .result_controller import Matplotlib3DWidget
from models.sqlitedict_model import SqliteDictModel
from libs.utils import DLT
from PySide6 import QtWidgets
import ctypes
import cv2 as cv
import numpy as np
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import QTimer
import mediapipe as mp

def after_call(after_func):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            after_func(self)
            return result
        return wrapper
    return decorator

class MainWindowController:
    def __init__(self, window: QtWidgets.QMainWindow, db: SqliteDictModel, matplotlib_widget: Matplotlib3DWidget, pose_keypoints):
        super().__init__()
        self.window = window
        self.db = db
        self.matplotlib_widget = matplotlib_widget
        self.view_resize = int(db["view_resize"])
        self.width = int(db["frame_width"])
        self.height = int(db["frame_height"])
        self.pose_keypoints = pose_keypoints
        #self.pose_keypoints = [0, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]
        #self.pose_keypoints = [16, 14, 12, 11, 13, 15, 24, 23, 25, 26, 27, 28]

    @after_call(lambda self: self.display_placeholder_images())
    def set_initial_size(self):
        screen_width, screen_height = get_screen_resolution()

        # Adjust label sizes based on screen resolution
        if screen_width <= 2560 and screen_height <= 1440:
            self.label_width = 960
            self.label_height = 540
        else:
            self.label_width = 1280
            self.label_height = 1080

        self.window.camera0Label.setFixedSize(self.label_width, self.label_height)
        self.window.camera1Label.setFixedSize(self.label_width, self.label_height)

        result_label_height = self.label_height
        function_widget_height = self.label_height

        result_label_width = self.label_width
        function_widget_width = self.label_width

        self.window.resultWidget.setFixedSize(result_label_width, result_label_height)
        self.window.functionWidget.setFixedSize(function_widget_width, function_widget_height)

        # Calculate main window size based on widget sizes
        main_window_width = self.label_width * 2
        main_window_height = self.label_height * 2

        self.window.resize(main_window_width, main_window_height)
        self.window.move((screen_width - main_window_width) / 2, (screen_height - main_window_height) / 2)

    def display_placeholder_images(self):
        display_placeholder_image(self.window.camera0Label, 1, self.label_height, self.label_width, "Camera 0", bw=True)  
        display_placeholder_image(self.window.camera1Label, 1, self.label_height, self.label_width, "Camera 1", bw=True)   # 白黒ノイズ
        #display_placeholder_image(self.window.resultLabel, 1, self.label_height, self.label_width, "Result", bw=True)

    def start_capture(self):
        camera0_name = "camera0"
        cmtx0, dist0 = self.db.read_camera_params(camera0_name)
        R0, T0 = self.db.read_extrinsic_calibration_parameters(camera0_name)
        self.P0 = get_projection_matrix(cmtx0, R0, T0)
        camera1_name = "camera1"
        cmtx1, dist1 = self.db.read_camera_params(camera1_name)
        R1, T1 = self.db.read_extrinsic_calibration_parameters(camera1_name)
        self.P1 = get_projection_matrix(cmtx1, R1, T1)

        mp_pose = mp.solutions.pose
        self.pose0 = mp_pose.Pose(model_complexity=1, 
                                  smooth_landmarks=True, 
                                  enable_segmentation=False,
                                  smooth_segmentation=True,
                                  min_detection_confidence=0.5, 
                                  min_tracking_confidence=0.5)
        self.pose1 = mp_pose.Pose(model_complexity=1, 
                                  smooth_landmarks=True, 
                                  enable_segmentation=False,
                                  smooth_segmentation=True,
                                  min_detection_confidence=0.5, 
                                  min_tracking_confidence=0.5)

        self.kpts_cam0 = []
        self.kpts_cam1 = []
        self.kpts_3d = []

        self.camera0_initialized = False
        self.camera1_initialized = False
        self.camera0_idx = int(self.db["camera0"])
        print(f"camera0_idx: {self.camera0_idx}")
        self.camera0_thread = CameraInitializationThread(self.camera0_idx)
        self.camera0_thread.initialized.connect(self.on_camera0_initialized) 
        self.camera0_thread.start()

        # start camera1 initialization thread
        self.camera1_idx = int(self.db["camera1"])
        print(f"camera1_idx: {self.camera1_idx}")
        self.camera1_thread = CameraInitializationThread(self.camera1_idx)
        self.camera1_thread.initialized.connect(self.on_camera1_initialized) 
        self.camera1_thread.start()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame) 

    def on_camera0_initialized(self, cap):
        self.cap0 = cap
        self.cap0.set(3, self.label_width)
        self.cap0.set(4, self.label_height)
        self.camera0_initialized = True
        self.check_all_cameras_initialized()

    def on_camera1_initialized(self, cap):
        self.cap1 = cap
        self.cap1.set(3, self.label_width)
        self.cap1.set(4, self.label_height)
        self.camera1_initialized = True
        self.check_all_cameras_initialized()

    def check_all_cameras_initialized(self):
        if self.camera0_initialized and self.camera1_initialized:
            self.timer.start(30)    # start timer after both cameras are initialized

    def stop_capture(self):
        self.timer.stop()
        self.cap0.release()
        self.cap1.release()
        self.display_placeholder_images()

    def update_frame(self):
        ret0, frame0 = self.cap0.read()
        ret1, frame1 = self.cap1.read()

        if not ret0 or not ret1:
            print("Error: Cannot read frame from camera")
            return
        
        # convert BGR image to RGB
        frame0 = cv.cvtColor(frame0, cv.COLOR_BGR2RGB)
        frame1 = cv.cvtColor(frame1, cv.COLOR_BGR2RGB)

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        frame0.flags.writeable = False
        frame1.flags.writeable = False
        results0 = self.pose0.process(frame0)
        results1 = self.pose1.process(frame1)

        #reverse changes
        frame0.flags.writeable = True
        frame1.flags.writeable = True
        frame0 = cv.cvtColor(frame0, cv.COLOR_RGB2BGR)
        frame1 = cv.cvtColor(frame1, cv.COLOR_RGB2BGR)

        #check for keypoints detection
        frame0_keypoints = []
        if results0.pose_landmarks:
            for i, landmark in enumerate(results0.pose_landmarks.landmark):
                if i not in self.pose_keypoints: continue #only save keypoints that are indicated in pose_keypoints
                pxl_x = landmark.x * frame0.shape[1]
                pxl_y = landmark.y * frame0.shape[0]
                pxl_x = int(round(pxl_x))
                pxl_y = int(round(pxl_y))
                cv.circle(frame0,(pxl_x, pxl_y), 3, (0,0,255), -1) #add keypoint detection points into figure
                kpts = [pxl_x, pxl_y]
                frame0_keypoints.append(kpts)
        else:
            #if no keypoints are found, simply fill the frame data with [-1,-1] for each kpt
            frame0_keypoints = [[-1, -1]]*len(self.pose_keypoints)            

        #this will keep keypoints of this frame in memory
        #self.kpts_cam0.append(frame0_keypoints)

        frame1_keypoints = []
        if results1.pose_landmarks:
            for i, landmark in enumerate(results1.pose_landmarks.landmark):
                if i not in self.pose_keypoints: continue
                pxl_x = landmark.x * frame1.shape[1]
                pxl_y = landmark.y * frame1.shape[0]
                pxl_x = int(round(pxl_x))
                pxl_y = int(round(pxl_y))
                cv.circle(frame1,(pxl_x, pxl_y), 3, (0,0,255), -1)
                kpts = [pxl_x, pxl_y]
                frame1_keypoints.append(kpts)
        else:
            #if no keypoints are found, simply fill the frame data with [-1,-1] for each kpt
            frame1_keypoints = [[-1, -1]]*len(self.pose_keypoints)

        #calculate 3d position
        frame_p3ds = []
        for uv1, uv2 in zip(frame0_keypoints, frame1_keypoints):
            if uv1[0] == -1 or uv2[0] == -1:
                _p3d = [-1, -1, -1]
            else:
                _p3d = DLT(self.P0, self.P1, uv1, uv2) #calculate 3d position of keypoint
            frame_p3ds.append(_p3d)

        frame_p3ds = np.array(frame_p3ds).reshape((len(self.pose_keypoints), 3))
        print(frame_p3ds)
        self.matplotlib_widget.update_plot(frame_p3ds)

        frame0_small = cv.resize(frame0, (self.label_width, self.label_height))
        frame1_small = cv.resize(frame1, (self.label_width, self.label_height))
        frame0_small_rgb = cv.cvtColor(frame0_small, cv.COLOR_BGR2RGB)
        frame1_small_rgb = cv.cvtColor(frame1_small, cv.COLOR_BGR2RGB)

        heigcht0, width0, channel0 = frame0_small_rgb.shape
        heigcht1, width1, channel1 = frame1_small_rgb.shape
        bytes_per_line0 = 3 * width0
        bytes_per_line1 = 3 * width1
        qimage0 = QImage(frame0_small_rgb.data, width0, heigcht0, bytes_per_line0, QImage.Format.Format_RGB888)
        pixmap0 = QPixmap.fromImage(qimage0)
        qimage1 = QImage(frame1_small_rgb.data, width1, heigcht1, bytes_per_line1, QImage.Format.Format_RGB888)
        pixmap1 = QPixmap.fromImage(qimage1)
        self.window.camera0Label.setPixmap(pixmap0)
        self.window.camera1Label.setPixmap(pixmap1)
        

def get_screen_resolution():
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)
    return screen_width, screen_height

def display_placeholder_image(label: QtWidgets.QLabel, view_resize, height: int, width: int, camera_name: str, bw=False):
    # テストパターン画像を生成
    if bw:
        placeholder_image = generate_bw_noise_pattern(height, width)
    else:
        placeholder_image = generate_test_pattern(height, width)
    
    # BGRからRGBに変換
    placeholder_image_rgb = cv.cvtColor(placeholder_image, cv.COLOR_BGR2RGB)
    cv.putText(placeholder_image_rgb, f"{camera_name}", (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv.LINE_AA)
    display_image(label, view_resize, placeholder_image_rgb)

def generate_test_pattern(height, width):
    # カラーノイズパターンを生成
    pattern = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)
    return pattern

def generate_bw_noise_pattern(height, width):
    # 白黒の砂嵐パターンを生成
    pattern = np.random.randint(0, 256, (height, width), dtype=np.uint8)
    pattern = cv.cvtColor(pattern, cv.COLOR_GRAY2BGR)
    return pattern

def display_image(label: QtWidgets.QLabel, view_resize, image):
    # 画像をリサイズ
    image_small = cv.resize(image, None, fx=1/view_resize, fy=1/view_resize)
    # BGRからRGBに変換
    image_rgb = cv.cvtColor(image_small, cv.COLOR_BGR2RGB)
    qformat = QImage.Format.Format_RGB888
    # RGBからQImageに変換
    qimage = QImage(image_rgb.data, image_rgb.shape[1], image_rgb.shape[0], image_rgb.strides[0], qformat)
    label.setPixmap(QPixmap.fromImage(qimage))