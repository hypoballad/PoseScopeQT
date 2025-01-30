from PySide6 import QtWidgets
from models.sqlitedict_model import SqliteDictModel

class PreferenceController:
    # def __init__(self, combo_box: QtWidgets.QComboBox, db: SqliteDictModel):
    #     self.combo_box = combo_box

    def __init__(self, dialog: QtWidgets.QDialog, db: SqliteDictModel):
        self.db = db
        self.load_settings(dialog)

    def load_settings(self, dialog: QtWidgets.QDialog):
        """
        dialogはPreferenceDialogインスタンスを想定しており、
        以下のようなQLineEditが用意されているものとします:
          dialog.camera0LineEdit.setText(self.db["camera0"])
          dialog.camera1LineEdit.setText(self.db["camera1"])
          ... etc ...
        """

        dialog.camera0LineEdit.setText(self.db["camera0"])
        dialog.camera1LineEdit.setText(self.db["camera1"])
        dialog.frame_widthLineEdit.setText(self.db["frame_width"])
        dialog.frame_heightLineEdit.setText(self.db["frame_height"])
        dialog.mono_calibration_framesLineEdit.setText(self.db["mono_calibration_frames"])
        dialog.stereo_calibration_framesLineEdit.setText(self.db["stereo_calibration_frames"])
        dialog.view_resizeLineEdit.setText(self.db["view_resize"])
        dialog.checkerboard_box_size_scaleLineEdit.setText(self.db["checkerboard_box_size_scale"])
        dialog.checkerboard_rowsLineEdit.setText(self.db["checkerboard_rows"])
        dialog.checkerboard_columnsLineEdit.setText(self.db["checkerboard_columns"])
        dialog.cooldownLineEdit.setText(self.db["cooldown"])

    def save_settings(self, dialog: QtWidgets.QDialog):
        """
        dialogはPreferenceDialogインスタンスを想定しており、
        以下のようなQLineEditが用意されているものとします:
          dialog.camera0LineEdit.text()
          dialog.camera1LineEdit.text()
          ... etc ...
        """

        self.db["camera0"] = dialog.camera0LineEdit.text()
        self.db["camera1"] = dialog.camera1LineEdit.text()
        self.db["frame_width"] = dialog.frame_widthLineEdit.text()
        self.db["frame_height"] = dialog.frame_heightLineEdit.text()
        self.db["mono_calibration_frames"] = dialog.mono_calibration_framesLineEdit.text()
        self.db["stereo_calibration_frames"] = dialog.stereo_calibration_framesLineEdit.text()
        self.db["view_resize"] = dialog.view_resizeLineEdit.text()
        self.db["checkerboard_box_size_scale"] = dialog.checkerboard_box_size_scaleLineEdit.text()
        self.db["checkerboard_rows"] = dialog.checkerboard_rowsLineEdit.text()
        self.db["checkerboard_columns"] = dialog.checkerboard_columnsLineEdit.text()
        self.db["cooldown"] = dialog.cooldownLineEdit.text()

