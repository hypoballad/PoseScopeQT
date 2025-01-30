# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'stereo_calibration2.ui'
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
    QLineEdit, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_stereoCalibrateDialog2(object):
    def setupUi(self, stereoCalibrateDialog2):
        if not stereoCalibrateDialog2.objectName():
            stereoCalibrateDialog2.setObjectName(u"stereoCalibrateDialog2")
        stereoCalibrateDialog2.resize(1946, 687)
        self.horizontalLayout_2 = QHBoxLayout(stereoCalibrateDialog2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.camera0lineEdit = QLineEdit(stereoCalibrateDialog2)
        self.camera0lineEdit.setObjectName(u"camera0lineEdit")

        self.verticalLayout_2.addWidget(self.camera0lineEdit)

        self.camera0Label = QLabel(stereoCalibrateDialog2)
        self.camera0Label.setObjectName(u"camera0Label")
        self.camera0Label.setStyleSheet(u"border: 1px solid black;")

        self.verticalLayout_2.addWidget(self.camera0Label)

        self.nextButton0 = QPushButton(stereoCalibrateDialog2)
        self.nextButton0.setObjectName(u"nextButton0")

        self.verticalLayout_2.addWidget(self.nextButton0)

        self.skipButton0 = QPushButton(stereoCalibrateDialog2)
        self.skipButton0.setObjectName(u"skipButton0")

        self.verticalLayout_2.addWidget(self.skipButton0)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.camera1LineEdit = QLineEdit(stereoCalibrateDialog2)
        self.camera1LineEdit.setObjectName(u"camera1LineEdit")
        self.camera1LineEdit.setEnabled(False)

        self.verticalLayout.addWidget(self.camera1LineEdit)

        self.camera1Label = QLabel(stereoCalibrateDialog2)
        self.camera1Label.setObjectName(u"camera1Label")
        self.camera1Label.setStyleSheet(u"border: 1px solid black;")

        self.verticalLayout.addWidget(self.camera1Label)

        self.nextButton1 = QPushButton(stereoCalibrateDialog2)
        self.nextButton1.setObjectName(u"nextButton1")
        self.nextButton1.setEnabled(False)

        self.verticalLayout.addWidget(self.nextButton1)

        self.skipButton1 = QPushButton(stereoCalibrateDialog2)
        self.skipButton1.setObjectName(u"skipButton1")
        self.skipButton1.setEnabled(False)

        self.verticalLayout.addWidget(self.skipButton1)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.horizontalLayout_2.addLayout(self.horizontalLayout)


        self.retranslateUi(stereoCalibrateDialog2)

        QMetaObject.connectSlotsByName(stereoCalibrateDialog2)
    # setupUi

    def retranslateUi(self, stereoCalibrateDialog2):
        stereoCalibrateDialog2.setWindowTitle(QCoreApplication.translate("stereoCalibrateDialog2", u"Dialog", None))
        self.camera0Label.setText(QCoreApplication.translate("stereoCalibrateDialog2", u"TextLabel", None))
        self.nextButton0.setText(QCoreApplication.translate("stereoCalibrateDialog2", u"next", None))
        self.skipButton0.setText(QCoreApplication.translate("stereoCalibrateDialog2", u"skip", None))
        self.camera1Label.setText(QCoreApplication.translate("stereoCalibrateDialog2", u"TextLabel", None))
        self.nextButton1.setText(QCoreApplication.translate("stereoCalibrateDialog2", u"next", None))
        self.skipButton1.setText(QCoreApplication.translate("stereoCalibrateDialog2", u"skip", None))
    # retranslateUi

