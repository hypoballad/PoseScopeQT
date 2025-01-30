import sys, os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor
from views.main_window import Ui_MainWindow
from views.preference import Ui_PreferenceDialog
from controllers.preference_controller import PreferenceController
from views.camera_calibration import Ui_cameraCalibrationDialog
from models.sqlitedict_model import SqliteDictModel
from controllers.cameracalibration_controller import CameraCalibrationController, calibrate_camera_for_intrinsic_parameters
from views.stereo_calibration_ui import Ui_stereoCalibrateDialog
from views.stereo_calibration2_ui import Ui_stereoCalibrateDialog2
from views.camera_inspect_ui import Ui_cameraInspectDialog
from controllers.stereocalibration_controller import StereoCalibrationController
from controllers.stereocalibration_controller import StereoCalibrationController2
from controllers.stereocalibration_controller import StereoCalibrationCheckController
from controllers.result_controller import Matplotlib3DWidget
from controllers.mainwindow_controller import MainWindowController
from controllers.camerainspect_controller import CameraInspectController
import cv2 as cv

class CameraInspectDialog(QtWidgets.QDialog, Ui_cameraInspectDialog):
    def __init__(self, camera_index: int, db: SqliteDictModel):
        super().__init__()
        self.setupUi(self)
        self.controller = CameraInspectController(self, db)

class StereoCalibrationCheckDialog(QtWidgets.QDialog, Ui_stereoCalibrateDialog2):
    def __init__(self, db: SqliteDictModel):
        super().__init__()
        self.setupUi(self)
        self.controller = StereoCalibrationCheckController(self, db)

class StereoCalibrateDialog2(QtWidgets.QDialog, Ui_stereoCalibrateDialog2):
    def __init__(self, db: SqliteDictModel):
        super().__init__()
        self.setupUi(self)
        self.controller = StereoCalibrationController2(self, db)

    def showEvent(self, event):
        super().showEvent(event)
        # ダイアログが表示されたときに実行する処理
        QtCore.QTimer.singleShot(0, self.on_dialog_open)

    def on_dialog_open(self):
        # ダイアログが表示されたときに実行する処理をここに記述
        print("StereoCalibrateDialog2 has been opened")
        self.controller.stero_calibrate()    

class StereoCalibrateDialog(QtWidgets.QDialog, Ui_stereoCalibrateDialog):
    def __init__(self, db: SqliteDictModel):
        super().__init__()
        self.setupUi(self)
        self.controller = StereoCalibrationController(self, db)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Space:
            self.controller.start_calibration()
        else:
            super().keyPressEvent(event)

class CameraCalibrationDialog(QtWidgets.QDialog, Ui_cameraCalibrationDialog):
    def __init__(self, db: SqliteDictModel, camera_id: int):
        super().__init__()
        self.setupUi(self)
        self.controller = CameraCalibrationController(self, db, camera_id)
        self.startCalibrationButton.clicked.connect(self.start_calibration)
        #self.stopCalibrationButton.clicked.connect(self.close)

    def start_calibration(self):
        self.controller.start_calibration()

    def closeEvent(self, event):
        self.controller.closeEvent(event)
        super().closeEvent(event)

    # def close(self):
    #     self.controller.closeEvent()
    #     super().close()

class PreferenceDialog(QtWidgets.QDialog, Ui_PreferenceDialog):
    def __init__(self, db: SqliteDictModel):
        super().__init__()
        self.setupUi(self)
        self.db = db
        self.preference_controller = PreferenceController(self, db)
        #self.stereo_calibration_controller = StereoCalibrationController(self, db)
        #self.filecomboBox.installEventFilter(self)
        
        #self.savePreferenceButton.setObjectName("savePushButton")
        self.listMenu.itemClicked.connect(self.on_item_clicked)
        self.savePreferenceButton.clicked.connect(self.save_settings)
        self.stackedWidget.setCurrentIndex(0)
        self.captureCamera0CaliblationButton.clicked.connect(self.on_capture_camera0_calibration_button_clicked)
        self.captureCamera1CaliblationButton.clicked.connect(self.on_capture_camera1_calibration_button_clicked)
        self.execCalibration0Button.clicked.connect(self.on_execCalibrationButton0_clicked)
        self.execCalibration1Button.clicked.connect(self.on_execCalibrationButton1_clicked)
        self.openStereoCalibrationButton.clicked.connect(self.on_stereo_calibration_button_clicked)
        self.stereoCameraCalibrationButton.clicked.connect(self.on_execStereoCalibration_button_clicked)
        self.openCameraInspectButton.clicked.connect(self.on_camera_inspect_button_clicked)

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.Type.MouseButtonPress and source is self.filecomboBox:
            self.preference_controller.open_file_dialog(self)
            return True
        return super().eventFilter(source, event)
    
    def save_settings(self):
        file_path = self.preference_controller.save_settings(self)
        self.file_path = file_path

    def on_camera_inspect_button_clicked(self):
        camera_index = int(self.db["camera0"])
        dlg = CameraInspectDialog(camera_index, self.db)
        dlg.exec()

    def on_capture_camera0_calibration_button_clicked(self):
        camera0 = int(self.db["camera0"])
        dlg = CameraCalibrationDialog(self.db, camera0)
        dlg.exec()

    def on_capture_camera1_calibration_button_clicked(self):
        camera1 = int(self.db["camera1"])
        dlg = CameraCalibrationDialog(self.db, camera1)
        dlg.exec()

    def on_execCalibrationButton0_clicked(self):
        base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        camera0 = int(self.db["camera0"])
        images_prefix = os.path.join(base_dir, 'frames', f"camera{camera0}*")
        cmtx0, dist0 = calibrate_camera_for_intrinsic_parameters(images_prefix, self.db)
        self.db.save_camera_intrinsics(cmtx0, dist0, 'camera0')
        # save_parameter_dir = os.path.join(base_dir, 'calibration_parameters')
        # save_camera_intrinsics(save_parameter_dir, cmtx0, dist0, 'camera0')

    def on_execCalibrationButton1_clicked(self):
        base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        camera1 = int(self.db["camera1"])
        images_prefix = os.path.join(base_dir, 'frames', f"camera{camera1}*")
        cmtx0, dist0 = calibrate_camera_for_intrinsic_parameters(images_prefix, self.db)
        self.db.save_camera_intrinsics(cmtx0, dist0, 'camera1')
        # save_parameter_dir = os.path.join(base_dir, 'calibration_parameters')
        # save_camera_intrinsics(save_parameter_dir, cmtx0, dist0, 'camera1')

    def on_stereo_calibration_button_clicked(self):
        dlg = StereoCalibrateDialog(self.db)
        dlg.exec()

    def on_execStereoCalibration_button_clicked(self):
        dlg = StereoCalibrateDialog2(self.db)
        dlg.exec()
        # self.stereo_calibration_controller.exec_stereo_calibration()

    def on_checkCalibrationButton_clicked(self):
        dlg = StereoCalibrationCheckDialog(self.db)
        dlg.exec()

    def on_item_clicked(self, item):
        print(item.text())
        if item.text() == "Calibration Preference":
            self.stackedWidget.setCurrentIndex(0)
        if item.text() == "Camera Calibration":
            self.stackedWidget.setCurrentIndex(1)
        if item.text() == "Stereo Calibration":
            self.stackedWidget.setCurrentIndex(2)

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, db: SqliteDictModel):
        super().__init__()
        self.setupUi(self)
        pose_keypoints = [16, 14, 12, 11, 13, 15, 24, 23, 25, 26, 27, 28]
        self.matplotlib_widget = Matplotlib3DWidget(pose_keypoints=pose_keypoints)
        # resultWidget にレイアウトが設定されているか確認
        if self.resultWidget.layout() is None:
            layout = QtWidgets.QVBoxLayout(self.resultWidget)
            self.resultWidget.setLayout(layout)
        self.resultWidget.layout().addWidget(self.matplotlib_widget)

        self.controller = MainWindowController(self, db, self.matplotlib_widget, pose_keypoints)
        self.controller.set_initial_size()
        self.actionPreference.triggered.connect(self.open_preference_dialog)
        self.captureButton.clicked.connect(self.toggle_capture_button)
        self.captureButton.setText("Start Capture")
        self.capturing = False

    def toggle_capture_button(self):
        if self.capturing:
            #self.controller.stop_capture()
            self.captureButton.setText("Start Capture")
            self.controller.stop_capture()
        else:
            self.controller.start_capture()
            self.captureButton.setText("Stop Capture")
        self.capturing = not self.capturing

    def open_preference_dialog(self):
        dlg = PreferenceDialog(db)
        dlg.exec()

def set_dark_mode(app):
    """ ダークモードのカラーパレットを設定 """
    dark_palette = QPalette()

    # 背景色
    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))  # 背景
    dark_palette.setColor(QPalette.WindowText, QColor(255, 255, 255))  # 文字色

    # 入力フィールド (QLineEdit) の背景
    dark_palette.setColor(QPalette.Base, QColor(60, 60, 60))  # QLineEdit の背景
    dark_palette.setColor(QPalette.Text, QColor(255, 255, 255))  # テキストの色

    # ボタンやメニュー
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))

    # ハイライト
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))

    # Light (メニューやボタンの明るい部分)
    dark_palette.setColor(QPalette.Light, QColor(75, 75, 75))

    # アプリに適用
    app.setPalette(dark_palette)
    app.setStyle("Fusion")

    # スタイルシートでQMenuBarとQLineEditを補正
    app.setStyleSheet("""
        QMenuBar {
            background-color: #2E2E2E;
            color: white;
        }
        QMenuBar::item:selected {
            background-color: #444444;
        }
        QLineEdit {
            background-color: #3C3C3C;
            color: white;
            border: 1px solid #555555;
            padding: 4px;
            border-radius: 3px;
        }
    """)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    set_dark_mode(app)
    base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))  
    db_path = os.path.join(base_dir, "PoseScopeQT.sqlite")
    db = SqliteDictModel(db_path)
    w = MainWindow(db)
    w.show()
    app.exec()
    db.close()
    cv.destroyAllWindows()
