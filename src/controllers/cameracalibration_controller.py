import os, sys
from models.sqlitedict_model import SqliteDictModel
from libs.utils import rotate_frame, fit_to_label
import cv2 as cv
import numpy as np
from PySide6 import QtWidgets
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import QTimer, Qt, QThread, Signal
import copy
import glob

class CameraInitializationThread(QThread):
    initialized = Signal(cv.VideoCapture)

    def __init__(self, camera_index):
        super().__init__()
        self.camera_index = camera_index

    def run(self):
        cap = cv.VideoCapture(self.camera_index, cv.CAP_MSMF)
        self.initialized.emit(cap)

class CameraCalibrationController:

    def __init__(self, dialog: QtWidgets.QDialog, db: SqliteDictModel, camera_index=0):
        super().__init__()
        self.camera_index = camera_index
        self.dialog = dialog
        self.db = db

        ## frame save directory
        self.base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        self.frame_save_dir = os.path.join(self.base_dir, "frames")
        if not os.path.exists(self.frame_save_dir):
            os.makedirs(self.frame_save_dir)
        
        self.width = int(db["frame_width"])
        self.height = int(db["frame_height"])
        self.view_resize = int(db["view_resize"])
        cooldown_value = int(db["cooldown"])
        self.cooldown = copy.deepcopy(cooldown_value)
        self.cooldown_time = copy.deepcopy(cooldown_value)
        self.savecount = 0
        self.start = False

        # Get the size of the label
        label_size = self.dialog.labelCameraView.size()
        self.label_width = label_size.width()
        self.label_height = label_size.height()

        self.rotation_angle = self.db[f"camera{self.camera_index}_rotation_angle"]
        if self.rotation_angle == "":
            self.rotation_angle = 0
            self.db[f"camera{self.camera_id}_rotation_angle"] = self.rotation_angle

        # カメラ準備中の代替画像を表示
        self.display_placeholder_image()

        # カメラ初期化スレッドを開始
        self.init_thread = CameraInitializationThread(self.camera_index)
        self.init_thread.initialized.connect(self.on_camera_initialized)
        self.init_thread.start()

        # # タイマー設定（30msごとに更新）
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

    def on_camera_initialized(self, cap):
        self.cap = cap
        self.cap.set(3, self.width)
        self.cap.set(4, self.height)
        self.timer.start(30)  # カメラの初期化が完了した後にタイマーを開始

    def display_placeholder_image(self):
        placeholder_image = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        # 画像を半分のサイズにリサイズ
        placeholder_image_small = cv.resize(placeholder_image, None, fx=1/self.view_resize, fy=1/self.view_resize)
        # BGRからRGBに変換
        placeholder_image_rgb = cv.cvtColor(placeholder_image_small, cv.COLOR_BGR2RGB)
        cv.putText(placeholder_image_rgb, "Initializing Camera...", (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv.LINE_AA)
        self.display_image(placeholder_image_rgb)

    def display_placeholder_end_image(self):
        placeholder_image = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        # 画像を半分のサイズにリサイズ
        placeholder_image_small = cv.resize(placeholder_image, None, fx=1/self.view_resize, fy=1/self.view_resize)
        # BGRからRGBに変換
        placeholder_image_rgb = cv.cvtColor(placeholder_image_small, cv.COLOR_BGR2RGB)
        cv.putText(placeholder_image_rgb, "End Calibration", (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv.LINE_AA)
        self.display_image(placeholder_image_rgb)

    def display_image(self, img):
        qformat = QImage.Format.Format_RGB888
        img = QImage(img, img.shape[1], img.shape[0], img.strides[0], qformat)
        img = img.rgbSwapped()
        self.dialog.labelCameraView.setPixmap(QPixmap.fromImage(img))

    def update_frame(self):
        """カメラのフレームを取得し QLabel に表示"""

        if self.savecount > 10:
            self.timer.stop()
            cv.destroyAllWindows()
            self.cap.release()
            self.display_placeholder_end_image()
            return
    
        ret, frame = self.cap.read()
        if not ret:
            print("No video data received from camera. Exiting...")
            self.timer.stop()
            self.cap.release()
            return
        
         # 画像を縮小
        frame_rotated = rotate_frame(frame, self.rotation_angle)
        frame_resized = fit_to_label(frame_rotated, self.label_width, self.label_height, self.rotation_angle)
        #frame_small = cv.resize(frame, None, fx=1/self.view_resize, fy=1/self.view_resize)
        # テキストオーバーレイ
        if not self.start:
            cv.putText(frame_resized, "Press SPACEBAR to start collecting frames", (50, 50), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        else:
            self.cooldown_time -= 1
            cv.putText(frame_resized, f"Cooldown: {self.cooldown_time}", (50, 50), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv.putText(frame_resized, f"Num frames: {self.savecount}", (50, 100), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # フレームを保存
            if self.cooldown_time <= 0:
                #save_name = os.path.join('frames', str(self.camera_index) + '_' + str(self.savecount) + '.png')
                #base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))  
                save_name = os.path.join(self.base_dir, 'frames', f"camera{self.camera_index}" + '_' + str(self.savecount) + '.png')
                print(f"Saving frame to {save_name}")
                cv.imwrite(save_name, frame)
                self.savecount += 1
                self.cooldown_time = self.cooldown  # クールダウンをリセット

        # BGRからRGBに変換
        frame_small_rgb = cv.cvtColor(frame_resized, cv.COLOR_BGR2RGB)

        # OpenCV の画像を QImage に変換
        h, w, ch = frame_small_rgb.shape
        bytes_per_line = ch * w
        q_image = QImage(frame_small_rgb.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)

        # QLabel にセット
        self.dialog.labelCameraView.setPixmap(pixmap)

    # def start_calibration(self):
    #     self.timer.start(30)

    # def stop_calibration(self):
    #     self.timer.stop()

    def start_calibration(self):
        """キャプチャ開始"""
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

# #save camera intrinsic parameters to file
# def save_camera_intrinsics(save_path, camera_matrix, distortion_coefs, camera_name):

#     #create folder if it does not exist
#     if not os.path.exists(save_path):
#         os.mkdir(save_path)

#     out_filename = os.path.join(save_path, camera_name + '_intrinsics.dat')
#     outf = open(out_filename, 'w')

#     outf.write('intrinsic:\n')
#     for l in camera_matrix:
#         for en in l:
#             outf.write(str(en) + ' ')
#         outf.write('\n')

#     outf.write('distortion:\n')
#     for en in distortion_coefs[0]:
#         outf.write(str(en) + ' ')
#     outf.write('\n')


#Calibrate single camera to obtain camera intrinsic parameters from saved frames.
def calibrate_camera_for_intrinsic_parameters(images_prefix, db: SqliteDictModel):

    #NOTE: images_prefix contains camera name: "frames/camera0*".
    images_names = glob.glob(images_prefix)

    #read all frames
    images = [cv.imread(imname, 1) for imname in images_names]

    #criteria used by checkerboard pattern detector.
    #Change this if the code can't find the checkerboard. 
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 100, 0.001)

    rows = int(db['checkerboard_rows'])
    columns = int(db['checkerboard_columns'])
    world_scaling = float(db['checkerboard_box_size_scale']) #this will change to user defined length scale

    #coordinates of squares in the checkerboard world space
    objp = np.zeros((rows*columns,3), np.float32)
    objp[:,:2] = np.mgrid[0:rows,0:columns].T.reshape(-1,2)
    objp = world_scaling* objp

    #frame dimensions. Frames should be the same size.
    width = images[0].shape[1]
    height = images[0].shape[0]

    #Pixel coordinates of checkerboards
    imgpoints = [] # 2d points in image plane.

    #coordinates of the checkerboard in checkerboard world space.
    objpoints = [] # 3d point in real world space

    for i, frame in enumerate(images):
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        #find the checkerboard
        ret, corners = cv.findChessboardCorners(gray, (rows, columns), None)

        if ret == True:

            #Convolution size used to improve corner detection. Don't make this too large.
            conv_size = (11, 11)

            #opencv can attempt to improve the checkerboard coordinates
            corners = cv.cornerSubPix(gray, corners, conv_size, (-1, -1), criteria)
            cv.drawChessboardCorners(frame, (rows,columns), corners, ret)
            cv.putText(frame, 'If detected points are poor, press "s" to skip this sample', (25, 25), cv.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 1)

            cv.imshow('img', frame)
            k = cv.waitKey(0)

            if k & 0xFF == ord('s'):
                print('skipping')
                continue

            objpoints.append(objp)
            imgpoints.append(corners)
    
    ret, cmtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, (width, height), None, None)
    print('rmse:', ret)
    print('camera matrix:\n', cmtx)
    print('distortion coeffs:', dist)

    return cmtx, dist

