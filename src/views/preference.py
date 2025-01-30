# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'preference.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QFormLayout, QHBoxLayout,
    QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QPushButton, QSizePolicy, QStackedWidget, QWidget)

class Ui_PreferenceDialog(object):
    def setupUi(self, PreferenceDialog):
        if not PreferenceDialog.objectName():
            PreferenceDialog.setObjectName(u"PreferenceDialog")
        PreferenceDialog.resize(602, 538)
        self.horizontalLayout = QHBoxLayout(PreferenceDialog)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.preferenceHLayout = QHBoxLayout()
        self.preferenceHLayout.setSpacing(6)
        self.preferenceHLayout.setObjectName(u"preferenceHLayout")
        self.listMenu = QListWidget(PreferenceDialog)
        QListWidgetItem(self.listMenu)
        QListWidgetItem(self.listMenu)
        QListWidgetItem(self.listMenu)
        self.listMenu.setObjectName(u"listMenu")

        self.preferenceHLayout.addWidget(self.listMenu)

        self.stackedWidget = QStackedWidget(PreferenceDialog)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.pageCalibrationSettings = QWidget()
        self.pageCalibrationSettings.setObjectName(u"pageCalibrationSettings")
        self.formLayoutWidget = QWidget(self.pageCalibrationSettings)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(10, 10, 261, 54))
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.camera0Label = QLabel(self.formLayoutWidget)
        self.camera0Label.setObjectName(u"camera0Label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.camera0Label)

        self.camera0LineEdit = QLineEdit(self.formLayoutWidget)
        self.camera0LineEdit.setObjectName(u"camera0LineEdit")
        self.camera0LineEdit.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.camera0LineEdit)

        self.formLayoutWidget_2 = QWidget(self.pageCalibrationSettings)
        self.formLayoutWidget_2.setObjectName(u"formLayoutWidget_2")
        self.formLayoutWidget_2.setGeometry(QRect(10, 40, 261, 31))
        self.formLayout_2 = QFormLayout(self.formLayoutWidget_2)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.camera1Label = QLabel(self.formLayoutWidget_2)
        self.camera1Label.setObjectName(u"camera1Label")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.camera1Label)

        self.camera1LineEdit = QLineEdit(self.formLayoutWidget_2)
        self.camera1LineEdit.setObjectName(u"camera1LineEdit")
        self.camera1LineEdit.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.camera1LineEdit)

        self.formLayoutWidget_3 = QWidget(self.pageCalibrationSettings)
        self.formLayoutWidget_3.setObjectName(u"formLayoutWidget_3")
        self.formLayoutWidget_3.setGeometry(QRect(10, 70, 261, 31))
        self.formLayout_3 = QFormLayout(self.formLayoutWidget_3)
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.formLayout_3.setContentsMargins(0, 0, 0, 0)
        self.frame_widthLabel = QLabel(self.formLayoutWidget_3)
        self.frame_widthLabel.setObjectName(u"frame_widthLabel")

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.frame_widthLabel)

        self.frame_widthLineEdit = QLineEdit(self.formLayoutWidget_3)
        self.frame_widthLineEdit.setObjectName(u"frame_widthLineEdit")
        self.frame_widthLineEdit.setMinimumSize(QSize(100, 0))
        self.frame_widthLineEdit.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout_3.setWidget(0, QFormLayout.FieldRole, self.frame_widthLineEdit)

        self.formLayoutWidget_4 = QWidget(self.pageCalibrationSettings)
        self.formLayoutWidget_4.setObjectName(u"formLayoutWidget_4")
        self.formLayoutWidget_4.setGeometry(QRect(10, 100, 261, 31))
        self.formLayout_4 = QFormLayout(self.formLayoutWidget_4)
        self.formLayout_4.setObjectName(u"formLayout_4")
        self.formLayout_4.setContentsMargins(0, 0, 0, 0)
        self.frame_heightLabel = QLabel(self.formLayoutWidget_4)
        self.frame_heightLabel.setObjectName(u"frame_heightLabel")

        self.formLayout_4.setWidget(0, QFormLayout.LabelRole, self.frame_heightLabel)

        self.frame_heightLineEdit = QLineEdit(self.formLayoutWidget_4)
        self.frame_heightLineEdit.setObjectName(u"frame_heightLineEdit")
        self.frame_heightLineEdit.setMinimumSize(QSize(100, 0))
        self.frame_heightLineEdit.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.formLayout_4.setWidget(0, QFormLayout.FieldRole, self.frame_heightLineEdit)

        self.formLayoutWidget_5 = QWidget(self.pageCalibrationSettings)
        self.formLayoutWidget_5.setObjectName(u"formLayoutWidget_5")
        self.formLayoutWidget_5.setGeometry(QRect(10, 130, 261, 32))
        self.formLayout_5 = QFormLayout(self.formLayoutWidget_5)
        self.formLayout_5.setObjectName(u"formLayout_5")
        self.formLayout_5.setContentsMargins(0, 0, 0, 0)
        self.mono_calibration_framesLabel = QLabel(self.formLayoutWidget_5)
        self.mono_calibration_framesLabel.setObjectName(u"mono_calibration_framesLabel")

        self.formLayout_5.setWidget(0, QFormLayout.LabelRole, self.mono_calibration_framesLabel)

        self.mono_calibration_framesLineEdit = QLineEdit(self.formLayoutWidget_5)
        self.mono_calibration_framesLineEdit.setObjectName(u"mono_calibration_framesLineEdit")
        self.mono_calibration_framesLineEdit.setMinimumSize(QSize(100, 0))
        self.mono_calibration_framesLineEdit.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.formLayout_5.setWidget(0, QFormLayout.FieldRole, self.mono_calibration_framesLineEdit)

        self.formLayoutWidget_6 = QWidget(self.pageCalibrationSettings)
        self.formLayoutWidget_6.setObjectName(u"formLayoutWidget_6")
        self.formLayoutWidget_6.setGeometry(QRect(10, 160, 261, 31))
        self.formLayout_6 = QFormLayout(self.formLayoutWidget_6)
        self.formLayout_6.setObjectName(u"formLayout_6")
        self.formLayout_6.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        self.formLayout_6.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        self.formLayout_6.setContentsMargins(0, 0, 0, 0)
        self.stereo_calibration_framesLabel = QLabel(self.formLayoutWidget_6)
        self.stereo_calibration_framesLabel.setObjectName(u"stereo_calibration_framesLabel")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stereo_calibration_framesLabel.sizePolicy().hasHeightForWidth())
        self.stereo_calibration_framesLabel.setSizePolicy(sizePolicy)

        self.formLayout_6.setWidget(0, QFormLayout.LabelRole, self.stereo_calibration_framesLabel)

        self.stereo_calibration_framesLineEdit = QLineEdit(self.formLayoutWidget_6)
        self.stereo_calibration_framesLineEdit.setObjectName(u"stereo_calibration_framesLineEdit")
        sizePolicy.setHeightForWidth(self.stereo_calibration_framesLineEdit.sizePolicy().hasHeightForWidth())
        self.stereo_calibration_framesLineEdit.setSizePolicy(sizePolicy)
        self.stereo_calibration_framesLineEdit.setMinimumSize(QSize(100, 0))
        self.stereo_calibration_framesLineEdit.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.formLayout_6.setWidget(0, QFormLayout.FieldRole, self.stereo_calibration_framesLineEdit)

        self.formLayoutWidget_7 = QWidget(self.pageCalibrationSettings)
        self.formLayoutWidget_7.setObjectName(u"formLayoutWidget_7")
        self.formLayoutWidget_7.setGeometry(QRect(10, 190, 261, 31))
        self.formLayout_7 = QFormLayout(self.formLayoutWidget_7)
        self.formLayout_7.setObjectName(u"formLayout_7")
        self.formLayout_7.setContentsMargins(0, 0, 0, 0)
        self.view_resizeLabel = QLabel(self.formLayoutWidget_7)
        self.view_resizeLabel.setObjectName(u"view_resizeLabel")

        self.formLayout_7.setWidget(0, QFormLayout.LabelRole, self.view_resizeLabel)

        self.view_resizeLineEdit = QLineEdit(self.formLayoutWidget_7)
        self.view_resizeLineEdit.setObjectName(u"view_resizeLineEdit")
        self.view_resizeLineEdit.setMinimumSize(QSize(100, 0))
        self.view_resizeLineEdit.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.formLayout_7.setWidget(0, QFormLayout.FieldRole, self.view_resizeLineEdit)

        self.formLayoutWidget_8 = QWidget(self.pageCalibrationSettings)
        self.formLayoutWidget_8.setObjectName(u"formLayoutWidget_8")
        self.formLayoutWidget_8.setGeometry(QRect(10, 220, 261, 31))
        self.formLayout_8 = QFormLayout(self.formLayoutWidget_8)
        self.formLayout_8.setObjectName(u"formLayout_8")
        self.formLayout_8.setContentsMargins(0, 0, 0, 0)
        self.checkerboard_box_size_scaleLabel = QLabel(self.formLayoutWidget_8)
        self.checkerboard_box_size_scaleLabel.setObjectName(u"checkerboard_box_size_scaleLabel")

        self.formLayout_8.setWidget(0, QFormLayout.LabelRole, self.checkerboard_box_size_scaleLabel)

        self.checkerboard_box_size_scaleLineEdit = QLineEdit(self.formLayoutWidget_8)
        self.checkerboard_box_size_scaleLineEdit.setObjectName(u"checkerboard_box_size_scaleLineEdit")
        self.checkerboard_box_size_scaleLineEdit.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout_8.setWidget(0, QFormLayout.FieldRole, self.checkerboard_box_size_scaleLineEdit)

        self.formLayoutWidget_9 = QWidget(self.pageCalibrationSettings)
        self.formLayoutWidget_9.setObjectName(u"formLayoutWidget_9")
        self.formLayoutWidget_9.setGeometry(QRect(10, 250, 261, 31))
        self.formLayout_9 = QFormLayout(self.formLayoutWidget_9)
        self.formLayout_9.setObjectName(u"formLayout_9")
        self.formLayout_9.setContentsMargins(0, 0, 0, 0)
        self.checkerboard_rowsLabel = QLabel(self.formLayoutWidget_9)
        self.checkerboard_rowsLabel.setObjectName(u"checkerboard_rowsLabel")

        self.formLayout_9.setWidget(0, QFormLayout.LabelRole, self.checkerboard_rowsLabel)

        self.checkerboard_rowsLineEdit = QLineEdit(self.formLayoutWidget_9)
        self.checkerboard_rowsLineEdit.setObjectName(u"checkerboard_rowsLineEdit")
        self.checkerboard_rowsLineEdit.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout_9.setWidget(0, QFormLayout.FieldRole, self.checkerboard_rowsLineEdit)

        self.formLayoutWidget_10 = QWidget(self.pageCalibrationSettings)
        self.formLayoutWidget_10.setObjectName(u"formLayoutWidget_10")
        self.formLayoutWidget_10.setGeometry(QRect(10, 280, 261, 31))
        self.formLayout_10 = QFormLayout(self.formLayoutWidget_10)
        self.formLayout_10.setObjectName(u"formLayout_10")
        self.formLayout_10.setContentsMargins(0, 0, 0, 0)
        self.checkerboard_columnsLabel = QLabel(self.formLayoutWidget_10)
        self.checkerboard_columnsLabel.setObjectName(u"checkerboard_columnsLabel")

        self.formLayout_10.setWidget(0, QFormLayout.LabelRole, self.checkerboard_columnsLabel)

        self.checkerboard_columnsLineEdit = QLineEdit(self.formLayoutWidget_10)
        self.checkerboard_columnsLineEdit.setObjectName(u"checkerboard_columnsLineEdit")
        self.checkerboard_columnsLineEdit.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout_10.setWidget(0, QFormLayout.FieldRole, self.checkerboard_columnsLineEdit)

        self.formLayoutWidget_11 = QWidget(self.pageCalibrationSettings)
        self.formLayoutWidget_11.setObjectName(u"formLayoutWidget_11")
        self.formLayoutWidget_11.setGeometry(QRect(10, 310, 261, 31))
        self.formLayout_11 = QFormLayout(self.formLayoutWidget_11)
        self.formLayout_11.setObjectName(u"formLayout_11")
        self.formLayout_11.setContentsMargins(0, 0, 0, 0)
        self.cooldownLabel = QLabel(self.formLayoutWidget_11)
        self.cooldownLabel.setObjectName(u"cooldownLabel")

        self.formLayout_11.setWidget(0, QFormLayout.LabelRole, self.cooldownLabel)

        self.cooldownLineEdit = QLineEdit(self.formLayoutWidget_11)
        self.cooldownLineEdit.setObjectName(u"cooldownLineEdit")
        self.cooldownLineEdit.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout_11.setWidget(0, QFormLayout.FieldRole, self.cooldownLineEdit)

        self.savePreferenceButton = QPushButton(self.pageCalibrationSettings)
        self.savePreferenceButton.setObjectName(u"savePreferenceButton")
        self.savePreferenceButton.setGeometry(QRect(10, 480, 75, 24))
        self.stackedWidget.addWidget(self.pageCalibrationSettings)
        self.pageCameraCalibration = QWidget()
        self.pageCameraCalibration.setObjectName(u"pageCameraCalibration")
        self.captureCamera0CaliblationButton = QPushButton(self.pageCameraCalibration)
        self.captureCamera0CaliblationButton.setObjectName(u"captureCamera0CaliblationButton")
        self.captureCamera0CaliblationButton.setGeometry(QRect(20, 60, 91, 24))
        self.execCalibration0Button = QPushButton(self.pageCameraCalibration)
        self.execCalibration0Button.setObjectName(u"execCalibration0Button")
        self.execCalibration0Button.setGeometry(QRect(20, 90, 141, 24))
        self.captureCamera1CaliblationButton = QPushButton(self.pageCameraCalibration)
        self.captureCamera1CaliblationButton.setObjectName(u"captureCamera1CaliblationButton")
        self.captureCamera1CaliblationButton.setGeometry(QRect(20, 130, 91, 24))
        self.execCalibration1Button = QPushButton(self.pageCameraCalibration)
        self.execCalibration1Button.setObjectName(u"execCalibration1Button")
        self.execCalibration1Button.setGeometry(QRect(20, 160, 131, 24))
        self.openCameraInspectButton = QPushButton(self.pageCameraCalibration)
        self.openCameraInspectButton.setObjectName(u"openCameraInspectButton")
        self.openCameraInspectButton.setGeometry(QRect(20, 20, 131, 24))
        self.stackedWidget.addWidget(self.pageCameraCalibration)
        self.pageStereoCalibration = QWidget()
        self.pageStereoCalibration.setObjectName(u"pageStereoCalibration")
        self.openStereoCalibrationButton = QPushButton(self.pageStereoCalibration)
        self.openStereoCalibrationButton.setObjectName(u"openStereoCalibrationButton")
        self.openStereoCalibrationButton.setGeometry(QRect(20, 20, 131, 31))
        self.stereoCameraCalibrationButton = QPushButton(self.pageStereoCalibration)
        self.stereoCameraCalibrationButton.setObjectName(u"stereoCameraCalibrationButton")
        self.stereoCameraCalibrationButton.setGeometry(QRect(20, 60, 131, 31))
        self.checkCalibrationButton = QPushButton(self.pageStereoCalibration)
        self.checkCalibrationButton.setObjectName(u"checkCalibrationButton")
        self.checkCalibrationButton.setGeometry(QRect(20, 100, 131, 31))
        self.stackedWidget.addWidget(self.pageStereoCalibration)

        self.preferenceHLayout.addWidget(self.stackedWidget)


        self.horizontalLayout.addLayout(self.preferenceHLayout)


        self.retranslateUi(PreferenceDialog)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(PreferenceDialog)
    # setupUi

    def retranslateUi(self, PreferenceDialog):
        PreferenceDialog.setWindowTitle(QCoreApplication.translate("PreferenceDialog", u"Dialog", None))

        __sortingEnabled = self.listMenu.isSortingEnabled()
        self.listMenu.setSortingEnabled(False)
        ___qlistwidgetitem = self.listMenu.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("PreferenceDialog", u"Calibration Preference", None));
        ___qlistwidgetitem1 = self.listMenu.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("PreferenceDialog", u"Camera Calibration", None));
        ___qlistwidgetitem2 = self.listMenu.item(2)
        ___qlistwidgetitem2.setText(QCoreApplication.translate("PreferenceDialog", u"Stereo Calibration", None));
        self.listMenu.setSortingEnabled(__sortingEnabled)

        self.camera0Label.setText(QCoreApplication.translate("PreferenceDialog", u"Camera0", None))
        self.camera0LineEdit.setText(QCoreApplication.translate("PreferenceDialog", u"0", None))
        self.camera1Label.setText(QCoreApplication.translate("PreferenceDialog", u"Camera1", None))
        self.camera1LineEdit.setText(QCoreApplication.translate("PreferenceDialog", u"1", None))
        self.frame_widthLabel.setText(QCoreApplication.translate("PreferenceDialog", u"frame_width", None))
        self.frame_widthLineEdit.setText(QCoreApplication.translate("PreferenceDialog", u"1920", None))
        self.frame_heightLabel.setText(QCoreApplication.translate("PreferenceDialog", u"Frame Height", None))
        self.frame_heightLineEdit.setText(QCoreApplication.translate("PreferenceDialog", u"1080", None))
        self.mono_calibration_framesLabel.setText(QCoreApplication.translate("PreferenceDialog", u"Mono Calibration Frames", None))
        self.mono_calibration_framesLineEdit.setText(QCoreApplication.translate("PreferenceDialog", u"10", None))
        self.stereo_calibration_framesLabel.setText(QCoreApplication.translate("PreferenceDialog", u"Stereo Calibration Frames", None))
        self.stereo_calibration_framesLineEdit.setText(QCoreApplication.translate("PreferenceDialog", u"10", None))
        self.view_resizeLabel.setText(QCoreApplication.translate("PreferenceDialog", u"View Resize", None))
        self.view_resizeLineEdit.setText(QCoreApplication.translate("PreferenceDialog", u"2", None))
        self.checkerboard_box_size_scaleLabel.setText(QCoreApplication.translate("PreferenceDialog", u"checkerboard_box_size_scale", None))
        self.checkerboard_box_size_scaleLineEdit.setText(QCoreApplication.translate("PreferenceDialog", u"3.4", None))
        self.checkerboard_rowsLabel.setText(QCoreApplication.translate("PreferenceDialog", u"checkerboard_rows", None))
        self.checkerboard_rowsLineEdit.setText(QCoreApplication.translate("PreferenceDialog", u"4", None))
        self.checkerboard_columnsLabel.setText(QCoreApplication.translate("PreferenceDialog", u"checkerboard_columns", None))
        self.checkerboard_columnsLineEdit.setText(QCoreApplication.translate("PreferenceDialog", u"7", None))
        self.cooldownLabel.setText(QCoreApplication.translate("PreferenceDialog", u"cooldown", None))
        self.cooldownLineEdit.setText(QCoreApplication.translate("PreferenceDialog", u"100", None))
        self.savePreferenceButton.setText(QCoreApplication.translate("PreferenceDialog", u"save", None))
        self.captureCamera0CaliblationButton.setText(QCoreApplication.translate("PreferenceDialog", u"Open Camera0", None))
        self.execCalibration0Button.setText(QCoreApplication.translate("PreferenceDialog", u"exec camera0 calibrate", None))
        self.captureCamera1CaliblationButton.setText(QCoreApplication.translate("PreferenceDialog", u"Open Camer1", None))
        self.execCalibration1Button.setText(QCoreApplication.translate("PreferenceDialog", u"exec camera1 calibrate", None))
        self.openCameraInspectButton.setText(QCoreApplication.translate("PreferenceDialog", u"Open Camera Inspect", None))
        self.openStereoCalibrationButton.setText(QCoreApplication.translate("PreferenceDialog", u"Save Stereo Frames", None))
        self.stereoCameraCalibrationButton.setText(QCoreApplication.translate("PreferenceDialog", u"Stereo Calibration", None))
        self.checkCalibrationButton.setText(QCoreApplication.translate("PreferenceDialog", u"Check Calibration", None))
    # retranslateUi

