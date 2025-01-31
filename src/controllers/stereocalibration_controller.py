import os, sys
from PySide6 import QtWidgets
from models.sqlitedict_model import SqliteDictModel
from .cameracalibration_controller import CameraInitializationThread
from libs.utils import rotate_frame, fit_to_label, get_screen_resolution
import copy
import numpy as np
import cv2 as cv
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import QTimer, Qt
import PySide6.QtCore as QtCore
import glob

class StereoCalibrationController:
    def __init__(self, dialog: QtWidgets.QDialog, db: SqliteDictModel):
        super().__init__()
        self.db = db
        self.dialog = dialog
        self.base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        if not os.path.exists(os.path.join(self.base_dir, 'frames_pair')):
            os.makedirs(os.path.join(self.base_dir, 'frames_pair'))
        self.view_resize = int(db["view_resize"])
        cooldown_value = int(db["cooldown"])
        self.cooldown = copy.deepcopy(cooldown_value)
        self.cooldown_time = copy.deepcopy(cooldown_value)
        self.width = int(db["frame_width"])
        self.height = int(db["frame_height"])
        self.start = False
        self.savecount = 0

        label_camera0_size = self.dialog.camera0Label.size()
        self.label_camera0_width = label_camera0_size.width()
        self.label_camera0_height = label_camera0_size.height()
        camera0 = int(self.db["camera0"])
        self.camera0_rotation_angle = int(db[f"camera{camera0}_rotation_angle"])
        print(f"camera0_rotation_angle: {self.camera0_rotation_angle}")

        label_camera1_size = self.dialog.camera1Label.size()
        self.label_camera1_width = label_camera1_size.width()
        self.label_camera1_height = label_camera1_size.height()
        camera1 = self.db["camera1"]
        self.camera1_rotation_angle = int(db[f"camera{camera1}_rotation_angle"])
        print(f"camera1_rotation_angle: {self.camera1_rotation_angle}")

        # カメラ準備中の代替画像を表示
        self.display_placeholder_image(dialog.camera0Label, "Camera 0") 
        self.display_placeholder_image(dialog.camera1Label, "Camera 1")
    
        # start camera0 initialization thread
        self.camera0_idx = int(db["camera0"])
        print(f"camera0_idx: {self.camera0_idx}")
        self.camera0_thread = CameraInitializationThread(self.camera0_idx)
        self.camera0_thread.initialized.connect(self.on_camera0_initialized) 
        self.camera0_thread.start()

        # start camera1 initialization thread
        self.camera1_idx = int(db["camera1"])
        print(f"camera1_idx: {self.camera1_idx}")
        self.camera1_thread = CameraInitializationThread(self.camera1_idx)
        self.camera1_thread.initialized.connect(self.on_camera1_initialized) 
        self.camera1_thread.start()

        self.camera0_initialized = False
        self.camera1_initialized = False

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

    def on_camera0_initialized(self, cap):
        if cap is None or not cap.isOpened():
            print(f"Failed to initialize camera 0 with index {self.camera0_idx}")
            return
        self.cap0 = cap
        self.cap0.set(3, self.width)
        self.cap0.set(4, self.height)
        self.camera0_initialized = True
        self.check_all_cameras_initialized()

    def on_camera1_initialized(self, cap):
        if cap is None or not cap.isOpened():
            print(f"Failed to initialize camera 1 with index {self.camera1_idx}")
            return
        self.cap1 = cap
        self.cap1.set(3, self.width)
        self.cap1.set(4, self.height)
        self.camera1_initialized = True
        self.check_all_cameras_initialized()

    def check_all_cameras_initialized(self):
        if self.camera0_initialized and self.camera1_initialized:
            self.timer.start(30)

    def display_placeholder_image(self, label: QtWidgets.QLabel, camera_name: str):
        placeholder_image = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        # BGRからRGBに変換
        placeholder_image_rgb = cv.cvtColor(placeholder_image, cv.COLOR_BGR2RGB)
        cv.putText(placeholder_image_rgb, f"Initializing {camera_name}...", (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv.LINE_AA)
        self.display_image(label, placeholder_image_rgb)

    def display_placeholder_end_image(self, label: QtWidgets.QLabel):
        placeholder_image = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        # BGRからRGBに変換
        placeholder_image_rgb = cv.cvtColor(placeholder_image, cv.COLOR_BGR2RGB)
        cv.putText(placeholder_image_rgb, f"End Calibration", (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv.LINE_AA)
        self.display_image(label, placeholder_image_rgb)

    def display_image(self, label: QtWidgets.QLabel, image):
        # 画像を半分のサイズにリサイズ
        image_small = cv.resize(image, None, fx=1/self.view_resize, fy=1/self.view_resize)
        # BGRからRGBに変換
        image_rgb = cv.cvtColor(image_small, cv.COLOR_BGR2RGB)
        qformat = QImage.Format.Format_RGB888
        # RGBからQImageに変換
        qimage = QImage(image_rgb.data, image_rgb.shape[1], image_rgb.shape[0], image_rgb.strides[0], qformat)
        label.setPixmap(QPixmap.fromImage(qimage))

    def update_frame(self):
        if self.savecount > 10:
            self.timer.stop()
            self.cap0.release()
            self.cap1.release()
            self.dialog.accept()
            self.timer.stop()
            self.display_placeholder_end_image(self.dialog.camera0Label)
            self.display_placeholder_end_image(self.dialog.camera1Label)
            return

        # フレームの更新処理をここに追加
        ret0, frame0 = self.cap0.read()
        ret1, frame1 = self.cap1.read()

        if not ret0 and not ret1:
            print(f"No video data received from camera. Exiting...")
            self.timer.stop()
            self.cap0.release()
            self.cap1.release()
            return
        
        #frame0_small = cv.resize(frame0, None, fx=1/self.view_resize, fy=1/self.view_resize)
        frame0_rotated = rotate_frame(frame0, self.camera0_rotation_angle)
        frame0_resized = fit_to_label(frame0_rotated, self.label_camera0_width, self.label_camera0_height, self.camera0_rotation_angle)
        
        #frame1_small = cv.resize(frame1, None, fx=1/self.view_resize, fy=1/self.view_resize)
        frame1_rotated = rotate_frame(frame1, self.camera1_rotation_angle)
        frame1_resized = fit_to_label(frame1_rotated, self.label_camera1_width, self.label_camera1_height, self.camera1_rotation_angle)

        if not self.start:
            cv.putText(frame0_resized, "Make sure both cameras can see the calibration pattern well", (50,50), cv.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 1)
            cv.putText(frame0_resized, "Press SPACEBAR to start collection frames", (50,100), cv.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 1)

            cv.putText(frame1_resized, "Make sure both cameras can see the calibration pattern well", (50,50), cv.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 1)
            cv.putText(frame1_resized, "Press SPACEBAR to start collection frames", (50,100), cv.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 1)

        if self.start:
            self.cooldown_time -= 1
            cv.putText(frame0_resized, "Cooldown: " + str(self.cooldown_time), (50,50), cv.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 1)
            cv.putText(frame0_resized, "Num frames: " + str(self.savecount), (50,100), cv.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 1)
            
            cv.putText(frame1_resized, "Cooldown: " + str(self.cooldown_time), (50,50), cv.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 1)
            cv.putText(frame1_resized, "Num frames: " + str(self.savecount), (50,100), cv.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 1)

            if self.cooldown_time <= 0:
                savename = os.path.join(self.base_dir, 'frames_pair', f"camera{self.camera0_idx}" + '_' + str(self.savecount) + '.png')
                cv.imwrite(savename, frame0)

                savename = os.path.join(self.base_dir, 'frames_pair', f"camera{self.camera1_idx}" + '_' + str(self.savecount) + '.png')
                cv.imwrite(savename, frame1)

                self.savecount += 1
                self.cooldown_time = self.cooldown

        frame0_small_rgb = cv.cvtColor(frame0_resized, cv.COLOR_BGR2RGB)
        frame1_small_rgb = cv.cvtColor(frame1_resized, cv.COLOR_BGR2RGB)

        h0, w0, ch0 = frame0_small_rgb.shape
        h1, w1, ch1 = frame1_small_rgb.shape
        bytes_per_line0 = ch0 * w0
        bytes_per_line1 = ch1 * w1
        qimage0 = QImage(frame0_small_rgb.data, w0, h0, bytes_per_line0, QImage.Format.Format_RGB888)
        pixmap0 = QPixmap.fromImage(qimage0)
        qimage1 = QImage(frame1_small_rgb.data, w1, h1, bytes_per_line1, QImage.Format.Format_RGB888)
        pixmap1 = QPixmap.fromImage(qimage1)
        self.dialog.camera0Label.setPixmap(pixmap0)
        self.dialog.camera1Label.setPixmap(pixmap1)

    def start_calibration(self):
        self.start = True


    def keyPressEvent(self, event):
        """キー入力イベント処理"""
        if event.key() == Qt.Key.Key_Space:
            self.start = True
        elif event.key() == Qt.Key.Key_Escape:
            self.close()

    def closeEvent(self, event):
        """ウィンドウを閉じる際にカメラを解放"""
        self.cap.release()
        event.accept()

    # def exec_stereo_calibration(self):
    #     #read camera parameters
    #     cmtx0, dist0 = read_camera_params(os.path.join(self.base_dir, 'calibration_parameters', 'camera0_intrinsics.dat'))
    #     cmtx1, dist1 = read_camera_params(os.path.join(self.base_dir, 'calibration_parameters', 'camera1_intrinsics.dat'))
    #     frames_prefix_c0 = os.path.join(self.base_dir, 'frames_pair', 'camera0*')
    #     frames_prefix_c1 = os.path.join(self.base_dir, 'frames_pair', 'camera1*')
    #     R, T = stereo_calibrate(self.db, cmtx0, dist0, cmtx1, dist1, frames_prefix_c0, frames_prefix_c1)
    #     # save_parameter_dir = os.path.join(self.base_dir, 'calibration_parameters')
    #     # save_camera_intrinsics(save_parameter_dir, R, T, 'stereo')

def display_placeholder_image(label: QtWidgets.QLabel, view_resize, height: int, width: int, camera_name: str):
    placeholder_image = np.zeros((height, width, 3), dtype=np.uint8)
    # BGRからRGBに変換
    placeholder_image_rgb = cv.cvtColor(placeholder_image, cv.COLOR_BGR2RGB)
    cv.putText(placeholder_image_rgb, f"Initializing {camera_name}...", (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv.LINE_AA)
    display_image(label, view_resize, placeholder_image_rgb)

def display_image(label: QtWidgets.QLabel, view_resize, image):
    # 画像を半分のサイズにリサイズ
    image_small = cv.resize(image, None, fx=1/view_resize, fy=1/view_resize)
    # BGRからRGBに変換
    image_rgb = cv.cvtColor(image_small, cv.COLOR_BGR2RGB)
    qformat = QImage.Format.Format_RGB888
    # RGBからQImageに変換
    qimage = QImage(image_rgb.data, image_rgb.shape[1], image_rgb.shape[0], image_rgb.strides[0], qformat)
    label.setPixmap(QPixmap.fromImage(qimage))

class StereoCalibrationCheckController:
    def __init__(self, dialog: QtWidgets.QDialog, db: SqliteDictModel):
        super().__init__()
        self.db = db
        self.dialog = dialog
        self.base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        self.width = int(db["frame_width"])
        self.height = int(db["frame_height"])
        self.view_resize = int(db["view_resize"])

        screen_width, screen_height = get_screen_resolution()
        if screen_width <= 2560 and screen_height <= 1440:
            self.label_width = 960
            self.label_height = 540
        else:
            self.label_width = 1280
            self.label_height = 1080

        self.dialog.camera0Label.setFixedSize(self.label_width, self.label_height)
        # label_camera0_size = self.dialog.camera0Label.size()
        # self.label_camera0_width = label_camera0_size.width()
        # self.label_camera0_height = label_camera0_size.height()
        camera0 = int(self.db["camera0"])
        self.camera0_rotation_angle = int(db[f"camera{camera0}_rotation_angle"])
        print(f"camera0_rotation_angle: {self.camera0_rotation_angle}")

        self.dialog.camera1Label.setFixedSize(self.label_width, self.label_height)
        # label_camera1_size = self.dialog.camera1Label.size()
        # self.label_camera1_width = label_camera1_size.width()
        # self.label_camera1_height = label_camera1_size.height()
        camera1 = self.db["camera1"]
        self.camera1_rotation_angle = int(db[f"camera{camera1}_rotation_angle"])
        print(f"camera1_rotation_angle: {self.camera1_rotation_angle}")

        # カメラ準備中の代替画像を表示
        display_placeholder_image(dialog.camera0Label, self.view_resize, self.height, self.width, "Camera 0") 
        display_placeholder_image(dialog.camera1Label, self.view_resize, self.height, self.width, "Camera 1")

        # start camera0 initialization thread
        self.zshift = 60.
        self.camera0_idx = int(db["camera0"])
        print(f"camera0_idx: {self.camera0_idx}")
        self.camera0_thread = CameraInitializationThread(self.camera0_idx)
        self.camera0_thread.initialized.connect(self.on_camera0_initialized) 
        self.camera0_thread.start()

        # start camera1 initialization thread
        self.camera1_idx = int(db["camera1"])
        print(f"camera1_idx: {self.camera1_idx}")
        self.camera1_thread = CameraInitializationThread(self.camera1_idx)
        self.camera1_thread.initialized.connect(self.on_camera1_initialized) 
        self.camera1_thread.start()

        self.camera0_initialized = False
        self.camera1_initialized = False

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame) 

        # ボタンのクリックイベントをスロットに接続
        self.dialog.skipButton0.clicked.connect(self.on_skip_button_clicked)

    def wait_for_button_click(self):
        loop = QtCore.QEventLoop()
        self.dialog.nextButton0.clicked.connect(loop.quit)
        loop.exec()

    def on_skip_button_clicked(self):
        self.timer.stop()
        print("Timer stopped due to skip button click")

    def update_frame(self):
        ret0, frame0 = self.cap0.read()
        ret1, frame1 = self.cap1.read()

        if not ret0 or not ret1:
            print('Video stream not returning frame data')
            quit()

        #follow RGB colors to indicate XYZ axes respectively
        colors = [(0,0,255), (0,255,0), (255,0,0)]
        #draw projections to camera0
        origin = tuple(self.pixel_points_camera0[0].astype(np.int32))
        for col, _p in zip(colors, self.pixel_points_camera0[1:]):
            _p = tuple(_p.astype(np.int32))
            cv.line(frame0, origin, _p, col, 2)
        
        #draw projections to camera1
        origin = tuple(self.pixel_points_camera1[0].astype(np.int32))
        for col, _p in zip(colors, self.pixel_points_camera1[1:]):
            _p = tuple(_p.astype(np.int32))
            cv.line(frame1, origin, _p, col, 2)

        #frame0_small = cv.resize(frame0, None, fx=1/self.view_resize, fy=1/self.view_resize)
        frame0_rotated = rotate_frame(frame0, self.camera0_rotation_angle)
        frame0_resized = fit_to_label(frame0_rotated, self.label_width, self.label_height, self.camera0_rotation_angle)

        #frame1_small = cv.resize(frame1, None, fx=1/self.view_resize, fy=1/self.view_resize)
        frame1_rotated = rotate_frame(frame1, self.camera1_rotation_angle)
        frame1_resized = fit_to_label(frame1_rotated, self.label_width, self.label_height, self.camera1_rotation_angle)
        
        frame0_rgb = cv.cvtColor(frame0_resized, cv.COLOR_BGR2RGB)
        frame1_rgb = cv.cvtColor(frame1_resized, cv.COLOR_BGR2RGB)
        hegith0, width0, channel0 = frame0_rgb.shape
        hegith1, width1, channel1 = frame1_rgb.shape
        bytes_per_line0 = channel0 * width0
        bytes_per_line1 = channel1 * width1
        qimage0 = QImage(frame0_rgb.data, width0, hegith0, bytes_per_line0, QImage.Format.Format_RGB888)
        pixmap0 = QPixmap.fromImage(qimage0)
        qimage1 = QImage(frame1_rgb.data, width1, hegith1, bytes_per_line1, QImage.Format.Format_RGB888)
        pixmap1 = QPixmap.fromImage(qimage1)
        self.dialog.camera0Label.setPixmap(pixmap0)
        self.dialog.camera1Label.setPixmap(pixmap1)

        self.wait_for_button_click()
        
        # cv.imshow('frame0', frame0)
        # cv.imshow('frame1', frame1)

        # k = cv.waitKey(1)
        # if k == 27: break

    def on_camera0_initialized(self, cap):
        cmtx0, dist0, R0, T0 = self.db.load_numpy_array_from_sqlitedict('camera0_data')
        P0 = get_projection_matrix(cmtx0, R0, T0)
        coordinate_points = np.array([[0.,0.,0.],
                                    [1.,0.,0.],
                                    [0.,1.,0.],
                                    [0.,0.,1.]])
        z_shift = np.array([0.,0.,self.zshift]).reshape((1, 3))
        draw_axes_points = 5 * coordinate_points + z_shift
        pixel_points_camera0 = []
        for _p in draw_axes_points:
            X = np.array([_p[0], _p[1], _p[2], 1.])
            
            #project to camera0
            uv = P0 @ X
            uv = np.array([uv[0], uv[1]])/uv[2]
            pixel_points_camera0.append(uv)

        self.pixel_points_camera0 = np.array(pixel_points_camera0)
        if cap is None or not cap.isOpened():
            print(f"Failed to initialize camera 0 with index {self.camera0_idx}")
            return
        self.cap0 = cap
        self.cap0.set(3, self.width)
        self.cap0.set(4, self.height)
        self.camera0_initialized = True
        self.check_all_cameras_initialized()

    def on_camera1_initialized(self, cap):
        cmtx1, dist1, R1, T1 = self.db.load_numpy_array_from_sqlitedict('camera1_data')
        P1 = get_projection_matrix(cmtx1, R1, T1)
        coordinate_points = np.array([[0.,0.,0.],
                                    [1.,0.,0.],
                                    [0.,1.,0.],
                                    [0.,0.,1.]])
        z_shift = np.array([0.,0.,self.zshift]).reshape((1, 3))
        draw_axes_points = 5 * coordinate_points + z_shift
        pixel_points_camera1 = []
        for _p in draw_axes_points:
            X = np.array([_p[0], _p[1], _p[2], 1.])
            
            #project to camera1
            uv = P1 @ X
            uv = np.array([uv[0], uv[1]])/uv[2]
            pixel_points_camera1.append(uv)
        
        self.pixel_points_camera1 = np.array(pixel_points_camera1)
        if cap is None or not cap.isOpened():
            print(f"Failed to initialize camera 1 with index {self.camera1_idx}")
            return
        self.cap1 = cap
        self.cap1.set(3, self.width)
        self.cap1.set(4, self.height)
        self.camera1_initialized = True
        self.check_all_cameras_initialized()

    def check_all_cameras_initialized(self):
        if self.camera0_initialized and self.camera1_initialized:
            self.timer.start(30)    


class StereoCalibrationController2:
    def __init__(self, dialog: QtWidgets.QDialog, db: SqliteDictModel):
        super().__init__()
        self.db = db
        self.dialog = dialog
        self.base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        if not os.path.exists(os.path.join(self.base_dir, 'camera_parameters')):
            os.makedirs(os.path.join(self.base_dir, 'camera_parameters'))
        self.width = int(db["frame_width"])
        self.height = int(db["frame_height"])
        self.view_resize = int(db["view_resize"])

        # ボタンのクリックイベントをスロットに接続
        self.dialog.nextButton0.clicked.connect(self.on_next_button_clicked)
        self.dialog.skipButton0.clicked.connect(self.on_skip_button_clicked)

        # ボタンのクリック状態を保持するフラグ
        self.next_button_clicked = False
        self.skip_button_clicked = False

    def on_next_button_clicked(self):
        self.next_button_clicked = True
        self.skip_button_clicked = False

    def on_skip_button_clicked(self):
        self.next_button_clicked = False
        self.skip_button_clicked = True

    def wait_for_button_click(self):
        loop = QtCore.QEventLoop()
        self.dialog.nextButton0.clicked.connect(loop.quit)
        self.dialog.skipButton0.clicked.connect(loop.quit)
        # button.clicked.connect(loop.quit)
        loop.exec()
    
    def display_log_to_lineedit0(self, text: str):
        self.dialog.camera0lineEdit.setText(text)

    def stero_calibrate(self):
        cmtx0, dist0 = self.db.read_camera_params(camera_name='camera0')
        cmtx1, dist1 = self.db.read_camera_params(camera_name='camera1')
        #cmtx0, dist0 = read_camera_params(os.path.join(self.base_dir, 'calibration_parameters', 'camera0_intrinsics.dat'))
        #cmtx1, dist1 = read_camera_params(os.path.join(self.base_dir, 'calibration_parameters', 'camera1_intrinsics.dat'))
        R, T = self.start_calibration(cmtx0, dist0, cmtx1, dist1)
        R0 = np.eye(3, dtype=np.float32)
        T0 = np.array([0., 0., 0.]).reshape((3, 1))
        self.db.save_extrinsic_calibration_parameters(R0, T0, camera_name='camera0')
        self.db.save_extrinsic_calibration_parameters(R, T, camera_name='camera1')
        #self.save_extrinsic_calibration_parameters(R0, T0, R, T)
        R1 = R; T1 = T #to avoid confusion, camera1 R and T are labeled R1 and T1
        camera0_data = [cmtx0, dist0, R0, T0]
        camera1_data = [cmtx1, dist1, R1, T1]
        self.db.save_numpy_array_to_sqlitedict('camera0_data', camera0_data)
        self.db.save_numpy_array_to_sqlitedict('camera1_data', camera1_data)

    # deprecated
    def save_extrinsic_calibration_parameters(self, R0, T0, R1, T1, prefix = ''):
        camera0_rot_trans_filename = os.path.join(self.base_dir, 'camera_parameters', prefix + 'camera0_rot_trans.dat')
        outf = open(camera0_rot_trans_filename, 'w')
        outf.write('R:\n')
        for l in R0:
            for en in l:
                outf.write(str(en) + ' ')
            outf.write('\n')

        outf.write('T:\n')
        for l in T0:
            for en in l:
                outf.write(str(en) + ' ')
            outf.write('\n')
        outf.close()

        #R1 and T1 are just stereo calibration returned values
        camera1_rot_trans_filename = os.path.join(self.base_dir, 'camera_parameters', prefix + 'camera1_rot_trans.dat')
        outf = open(camera1_rot_trans_filename, 'w')

        outf.write('R:\n')
        for l in R1:
            for en in l:
                outf.write(str(en) + ' ')
            outf.write('\n')

        outf.write('T:\n')
        for l in T1:
            for en in l:
                outf.write(str(en) + ' ')
            outf.write('\n')
        outf.close()

        return R0, T0, R1, T1

    def start_calibration(self, mtx0, dist0, mtx1, dist1):
        camera0_idx = int(self.db["camera0"])
        camera1_idx = int(self.db["camera1"])
        frames_prefix_c0 = os.path.join(self.base_dir, 'frames_pair', f"camera{camera0_idx}*")
        frames_prefix_c1 = os.path.join(self.base_dir, 'frames_pair', f"camera{camera1_idx}*")
        
        #read the synched frames
        c0_images_names = sorted(glob.glob(frames_prefix_c0))
        c1_images_names = sorted(glob.glob(frames_prefix_c1))

        #open images
        c0_images = [cv.imread(imname, 1) for imname in c0_images_names]
        c1_images = [cv.imread(imname, 1) for imname in c1_images_names]

        #change this if stereo calibration not good.
        criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 100, 0.001)

        #calibration pattern settings
        rows = int(self.db['checkerboard_rows'])
        columns = int(self.db['checkerboard_columns'])
        world_scaling = float(self.db['checkerboard_box_size_scale'])

        #coordinates of squares in the checkerboard world space
        objp = np.zeros((rows*columns,3), np.float32)
        objp[:,:2] = np.mgrid[0:rows,0:columns].T.reshape(-1,2)
        objp = world_scaling* objp

        #frame dimensions. Frames should be the same size.
        width = c0_images[0].shape[1]
        height = c0_images[0].shape[0]

        #Pixel coordinates of checkerboards
        imgpoints_left = [] # 2d points in image plane.
        imgpoints_right = []

        #coordinates of the checkerboard in checkerboard world space.
        objpoints = [] # 3d point in real world space

        for frame0, frame1 in zip(c0_images, c1_images):
            gray1 = cv.cvtColor(frame0, cv.COLOR_BGR2GRAY)
            gray2 = cv.cvtColor(frame1, cv.COLOR_BGR2GRAY)
            c_ret1, corners1 = cv.findChessboardCorners(gray1, (rows, columns), None)
            c_ret2, corners2 = cv.findChessboardCorners(gray2, (rows, columns), None)
            print(f"c_ret1: {c_ret1}, c_ret2: {c_ret2}")
            if c_ret1 == True and c_ret2 == True:

                corners1 = cv.cornerSubPix(gray1, corners1, (11, 11), (-1, -1), criteria)
                corners2 = cv.cornerSubPix(gray2, corners2, (11, 11), (-1, -1), criteria)

                p0_c1 = corners1[0,0].astype(np.int32)
                p0_c2 = corners2[0,0].astype(np.int32)

                
                cv.putText(frame0, 'O', (p0_c1[0], p0_c1[1]), cv.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 1)
                cv.drawChessboardCorners(frame0, (rows,columns), corners1, c_ret1)
                frame0_small = cv.resize(frame0, None, fx=1/self.view_resize, fy=1/self.view_resize)
                frame0_small_rgb = cv.cvtColor(frame0_small, cv.COLOR_BGR2RGB)
                heigcht0, width0, channel0 = frame0_small_rgb.shape
                bytes_per_line0 = 3 * width0
                qimage0 = QImage(frame0_small_rgb.data, width0, heigcht0, bytes_per_line0, QImage.Format.Format_RGB888)
                pixmap0 = QPixmap.fromImage(qimage0)
                self.dialog.camera0Label.setPixmap(pixmap0)
                # cv.imshow('img', frame0)

                
                cv.putText(frame1, 'O', (p0_c2[0], p0_c2[1]), cv.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 1)
                cv.drawChessboardCorners(frame1, (rows,columns), corners2, c_ret2)
                frame1_small = cv.resize(frame1, None, fx=1/self.view_resize, fy=1/self.view_resize)
                frame1_small_rgb = cv.cvtColor(frame1_small, cv.COLOR_BGR2RGB)
                heigcht1, width1, channel1 = frame1_small_rgb.shape
                bytes_per_line1 = 3 * width1
                qimage1 = QImage(frame1_small_rgb.data, width1, heigcht1, bytes_per_line1, QImage.Format.Format_RGB888)
                pixmap1 = QPixmap.fromImage(qimage1)
                self.dialog.camera1Label.setPixmap(pixmap1)
                # cv.imshow('img2', frame1)

                # ボタンがクリックされるまで待機
                self.wait_for_button_click()

                if self.skip_button_clicked:
                    print('skipping')
                    continue

                # k = cv.waitKey(0)

                # if k & 0xFF == ord('s'):
                #     print('skipping')
                #     continue

                objpoints.append(objp)
                imgpoints_left.append(corners1)
                imgpoints_right.append(corners2)

        stereocalibration_flags = cv.CALIB_FIX_INTRINSIC
        ret, CM1, dist0, CM2, dist1, R, T, E, F = cv.stereoCalibrate(objpoints, imgpoints_left, imgpoints_right, mtx0, dist0,
                                                                    mtx1, dist1, (width, height), criteria = criteria, flags = stereocalibration_flags)

        self.display_log_to_lineedit0(f"rmse: {ret}")
        print('rmse: ', ret)
        return R, T

# deprecated
def read_camera_params(filepath: str):
    """
    指定されたファイルからカメラの内部パラメータと歪み係数を読み込む。

    Args:
        filepath (str): カメラパラメータが保存されたテキストファイルのパス。

    Returns:
        tuple[np.ndarray, np.ndarray]: カメラ行列 (cmtx), 歪み係数 (dist)
    """
    intrinsic_data = []
    distortion_data = []
    mode = None

    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if "intrinsic:" in line:
                mode = "intrinsic"
                continue
            elif "distortion:" in line:
                mode = "distortion"
                continue

            if mode == "intrinsic":
                intrinsic_data.append(list(map(float, line.split())))
            elif mode == "distortion":
                distortion_data.extend(map(float, line.split()))

    # numpy 配列に変換
    cmtx = np.array(intrinsic_data, dtype=np.float64)
    dist = np.array(distortion_data, dtype=np.float64)

    return cmtx, dist

#Converts Rotation matrix R and Translation vector T into a homogeneous representation matrix
def _make_homogeneous_rep_matrix(R, t):
    P = np.zeros((4,4))
    P[:3,:3] = R
    P[:3, 3] = t.reshape(3)
    P[3,3] = 1
 
    return P
# Turn camera calibration data into projection matrix
def get_projection_matrix(cmtx, R, T):
    P = cmtx @ _make_homogeneous_rep_matrix(R, T)[:3,:]
    return P