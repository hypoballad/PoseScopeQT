import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
from PySide6 import QtWidgets
from PySide6.QtCore import QTimer, QThread, Signal
from libs.utils import display_test_pattern, rotate_frame, fit_to_label
from models.sqlitedict_model import SqliteDictModel
from .cameracalibration_controller import CameraInitializationThread
from PySide6.QtGui import QImage, QPixmap
import cv2 as cv

class CameraInspectController:
    def __init__(self, dialog: QtWidgets.QDialog, db: SqliteDictModel):
        super().__init__()
        self.dialog = dialog
        self.camera_id = 0
        self.width = 480
        self.height = 270
        self.db = db
        self.rotation_angle = self.db[f"camera{self.camera_id}_rotation_angle"]
        if self.rotation_angle == "":
            self.rotation_angle = 0
            self.db[f"camera{self.camera_id}_rotation_angle"] = self.rotation_angle

        display_test_pattern(dialog.cameraLabel, self.height, self.width, "Camera Inspect", bw=True)

        self.camera_ids = self.detect_camera_ids()
        self.show_info(f"Detected camera IDs: {self.camera_ids}")
        #print(f"Detected camera IDs: {self.camera_ids}")
        self.camera_thread = CameraInitializationThread(self.camera_id)
        self.camera_thread.initialized.connect(self.on_camera_initialized)
        self.camera_thread.start()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        # changeCameraButton のクリックイベントを接続
        self.dialog.changeCameraButton.clicked.connect(self.change_camera)

        # rotateCameraButton のクリックイベントを接続
        self.dialog.rotateButton.clicked.connect(self.on_camera_rotate)

    def detect_camera_ids(self, max_cameras=10):
        camera_ids = []
        for i in range(max_cameras):
            cap = cv.VideoCapture(i, cv.CAP_DSHOW)
            if cap.isOpened():
                camera_ids.append(i)
                cap.release()
        return camera_ids

    def on_camera_initialized(self, cap):
        self.cap = cap
        self.dialog.inspectTextEdit.setPlainText(f"Camera: {self.camera_id}")
        resolution=self.test_camera_resolution()
        for res in resolution:
            self.show_info(res)
        properties = self.camera_properties()
        self.display_camera_properties(properties)
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, self.height)
        self.cap.set(cv.CAP_PROP_FRAME_WIDTH, self.width)
        self.timer.start(30)  # 30msごとにフレームを更新

    def on_camera_rotate(self):
        """カメラ画像を90°回転し、回転状態をDBに保存"""
        self.rotation_angle = (self.rotation_angle + 90) % 360  # 90度ずつ回転
        self.db[f"camera{self.camera_id}_rotation_angle"] = self.rotation_angle  # DBに保存
        self.show_info(f"Camera rotated to {self.rotation_angle} degrees")

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame_rotated = rotate_frame(frame, self.rotation_angle)  # 回転処理を適用
            frame_resized = fit_to_label(frame_rotated, self.width, self.height, self.rotation_angle)
            frame_rgb = cv.cvtColor(frame_resized, cv.COLOR_BGR2RGB)
            h, w, ch = frame_rgb.shape
            bytes_per_line = ch * w
            qimg = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(qimg)
            self.dialog.cameraLabel.setPixmap(pixmap)

    def change_camera(self):
        # 現在のカメラを解放
        self.cap.release()
        self.timer.stop()
        self.dialog.inspectTextEdit.setPlainText("")

        # 次のカメラ ID に切り替え
        current_index = self.camera_ids.index(self.camera_id)
        next_index = (current_index + 1) % len(self.camera_ids)
        self.camera_id = self.camera_ids[next_index]
        
        self.rotation_angle = self.db[f"camera{self.camera_id}_rotation_angle"]
        if self.rotation_angle == "":
            self.rotation_angle = 0

        # 新しいカメラを初期化
        self.camera_thread = CameraInitializationThread(self.camera_id)
        self.camera_thread.initialized.connect(self.on_camera_initialized)
        self.camera_thread.start()

    def camera_properties(self):
        properties = [
            ("FPS", cv.CAP_PROP_FPS),
            ("Brightness", cv.CAP_PROP_BRIGHTNESS),
            ("Contrast", cv.CAP_PROP_CONTRAST),
            ("Saturation", cv.CAP_PROP_SATURATION),
            ("Hue", cv.CAP_PROP_HUE),
            ("Gain", cv.CAP_PROP_GAIN),
            ("Exposure", cv.CAP_PROP_EXPOSURE),
            ("White Balance", cv.CAP_PROP_WHITE_BALANCE_BLUE_U),
            ("Rectification", cv.CAP_PROP_RECTIFICATION)
        ]
        return properties

    def show_info(self, text):
        textEdit = self.dialog.inspectTextEdit.toPlainText()
        self.dialog.inspectTextEdit.setPlainText(textEdit + "\n" + text)    

    def display_camera_properties(self, camera_info):
        prop_text = self.dialog.inspectTextEdit.toPlainText() + "\n"

        for name, prop in camera_info:
            value0 = self.cap.get(prop)
            prop_text += f"{name} (Camera {self.camera_id}): {value0}\n"

        self.dialog.inspectTextEdit.setPlainText(prop_text)

    def test_camera_resolution(self):
        if not self.cap.isOpened():
            return f"Camera could not be opened"
        
        resolution_results = []
        # 解像度を試す
        for width, height in [(1920, 1080), (1280, 720), (640, 480)]:
            self.cap.set(cv.CAP_PROP_FRAME_WIDTH, width)
            self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, height)
            actual_width = self.cap.get(cv.CAP_PROP_FRAME_WIDTH)
            actual_height = self.cap.get(cv.CAP_PROP_FRAME_HEIGHT)
            resolution_results.append(f"Tried {width}x{height}, got {actual_width}x{actual_height}")
        
        return resolution_results