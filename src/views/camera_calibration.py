# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'camera_calibration.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QPushButton,
    QSizePolicy, QWidget)

class Ui_cameraCalibrationDialog(object):
    def setupUi(self, cameraCalibrationDialog):
        if not cameraCalibrationDialog.objectName():
            cameraCalibrationDialog.setObjectName(u"cameraCalibrationDialog")
        cameraCalibrationDialog.resize(988, 600)
        self.labelCameraView = QLabel(cameraCalibrationDialog)
        self.labelCameraView.setObjectName(u"labelCameraView")
        self.labelCameraView.setGeometry(QRect(10, 10, 960, 540))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelCameraView.sizePolicy().hasHeightForWidth())
        self.labelCameraView.setSizePolicy(sizePolicy)
        self.startCalibrationButton = QPushButton(cameraCalibrationDialog)
        self.startCalibrationButton.setObjectName(u"startCalibrationButton")
        self.startCalibrationButton.setGeometry(QRect(30, 570, 75, 24))

        self.retranslateUi(cameraCalibrationDialog)

        QMetaObject.connectSlotsByName(cameraCalibrationDialog)
    # setupUi

    def retranslateUi(self, cameraCalibrationDialog):
        cameraCalibrationDialog.setWindowTitle(QCoreApplication.translate("cameraCalibrationDialog", u"Dialog", None))
        self.labelCameraView.setText("")
        self.startCalibrationButton.setText(QCoreApplication.translate("cameraCalibrationDialog", u"start capture", None))
    # retranslateUi

