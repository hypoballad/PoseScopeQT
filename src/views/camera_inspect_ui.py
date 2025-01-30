# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'camera_inspect.ui'
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
    QPushButton, QSizePolicy, QTextEdit, QVBoxLayout,
    QWidget)

class Ui_cameraInspectDialog(object):
    def setupUi(self, cameraInspectDialog):
        if not cameraInspectDialog.objectName():
            cameraInspectDialog.setObjectName(u"cameraInspectDialog")
        cameraInspectDialog.resize(500, 624)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(cameraInspectDialog.sizePolicy().hasHeightForWidth())
        cameraInspectDialog.setSizePolicy(sizePolicy)
        cameraInspectDialog.setMinimumSize(QSize(500, 0))
        cameraInspectDialog.setMaximumSize(QSize(500, 16777215))
        self.verticalLayout_2 = QVBoxLayout(cameraInspectDialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.changeCameraButton = QPushButton(cameraInspectDialog)
        self.changeCameraButton.setObjectName(u"changeCameraButton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.changeCameraButton.sizePolicy().hasHeightForWidth())
        self.changeCameraButton.setSizePolicy(sizePolicy1)
        self.changeCameraButton.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        self.horizontalLayout.addWidget(self.changeCameraButton)

        self.rotateButton = QPushButton(cameraInspectDialog)
        self.rotateButton.setObjectName(u"rotateButton")
        sizePolicy1.setHeightForWidth(self.rotateButton.sizePolicy().hasHeightForWidth())
        self.rotateButton.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.rotateButton)

        self.horizontalLayout.setStretch(0, 1)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.cameraLabel = QLabel(cameraInspectDialog)
        self.cameraLabel.setObjectName(u"cameraLabel")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(1)
        sizePolicy2.setHeightForWidth(self.cameraLabel.sizePolicy().hasHeightForWidth())
        self.cameraLabel.setSizePolicy(sizePolicy2)
        self.cameraLabel.setMinimumSize(QSize(480, 270))
        self.cameraLabel.setMaximumSize(QSize(480, 270))
        self.cameraLabel.setStyleSheet(u"border: 1px solid black;")

        self.verticalLayout.addWidget(self.cameraLabel)

        self.inspectTextEdit = QTextEdit(cameraInspectDialog)
        self.inspectTextEdit.setObjectName(u"inspectTextEdit")
        sizePolicy2.setHeightForWidth(self.inspectTextEdit.sizePolicy().hasHeightForWidth())
        self.inspectTextEdit.setSizePolicy(sizePolicy2)
        self.inspectTextEdit.setReadOnly(True)

        self.verticalLayout.addWidget(self.inspectTextEdit)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(cameraInspectDialog)

        QMetaObject.connectSlotsByName(cameraInspectDialog)
    # setupUi

    def retranslateUi(self, cameraInspectDialog):
        cameraInspectDialog.setWindowTitle(QCoreApplication.translate("cameraInspectDialog", u"Dialog", None))
        self.changeCameraButton.setText(QCoreApplication.translate("cameraInspectDialog", u"change", None))
        self.rotateButton.setText(QCoreApplication.translate("cameraInspectDialog", u"Rotate", None))
        self.cameraLabel.setText(QCoreApplication.translate("cameraInspectDialog", u"TextLabel", None))
    # retranslateUi

