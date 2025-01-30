# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'stereo_calibration.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel,
    QSizePolicy, QWidget)

class Ui_stereoCalibrateDialog(object):
    def setupUi(self, stereoCalibrateDialog):
        if not stereoCalibrateDialog.objectName():
            stereoCalibrateDialog.setObjectName(u"stereoCalibrateDialog")
        stereoCalibrateDialog.resize(1946, 628)
        self.horizontalLayout_2 = QHBoxLayout(stereoCalibrateDialog)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.camera0Label = QLabel(stereoCalibrateDialog)
        self.camera0Label.setObjectName(u"camera0Label")
        self.camera0Label.setMinimumSize(QSize(960, 540))
        self.camera0Label.setMaximumSize(QSize(960, 540))
        self.camera0Label.setStyleSheet(u"border: 1px solid black;")

        self.horizontalLayout.addWidget(self.camera0Label)

        self.camera1Label = QLabel(stereoCalibrateDialog)
        self.camera1Label.setObjectName(u"camera1Label")
        self.camera1Label.setMinimumSize(QSize(960, 540))
        self.camera1Label.setMaximumSize(QSize(960, 540))
        self.camera1Label.setStyleSheet(u"border: 1px solid black;")

        self.horizontalLayout.addWidget(self.camera1Label)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 1)

        self.horizontalLayout_2.addLayout(self.horizontalLayout)


        self.retranslateUi(stereoCalibrateDialog)

        QMetaObject.connectSlotsByName(stereoCalibrateDialog)
    # setupUi

    def retranslateUi(self, stereoCalibrateDialog):
        stereoCalibrateDialog.setWindowTitle(QCoreApplication.translate("stereoCalibrateDialog", u"Dialog", None))
        self.camera0Label.setText(QCoreApplication.translate("stereoCalibrateDialog", u"TextLabel", None))
        self.camera1Label.setText(QCoreApplication.translate("stereoCalibrateDialog", u"TextLabel", None))
    # retranslateUi

