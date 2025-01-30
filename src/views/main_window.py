# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QHBoxLayout, QLabel,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1401, 900)
        MainWindow.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.actionPreference = QAction(MainWindow)
        self.actionPreference.setObjectName(u"actionPreference")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.horizontalLayout_2 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout1 = QHBoxLayout()
        self.horizontalLayout1.setObjectName(u"horizontalLayout1")
        self.camera1Label = QLabel(self.centralwidget)
        self.camera1Label.setObjectName(u"camera1Label")
        sizePolicy.setHeightForWidth(self.camera1Label.sizePolicy().hasHeightForWidth())
        self.camera1Label.setSizePolicy(sizePolicy)
        self.camera1Label.setStyleSheet(u"border: 1px solid black;")
        self.camera1Label.setScaledContents(True)

        self.horizontalLayout1.addWidget(self.camera1Label)

        self.camera0Label = QLabel(self.centralwidget)
        self.camera0Label.setObjectName(u"camera0Label")
        sizePolicy.setHeightForWidth(self.camera0Label.sizePolicy().hasHeightForWidth())
        self.camera0Label.setSizePolicy(sizePolicy)
        self.camera0Label.setStyleSheet(u"border: 1px solid black;")
        self.camera0Label.setScaledContents(True)

        self.horizontalLayout1.addWidget(self.camera0Label)

        self.horizontalLayout1.setStretch(0, 1)
        self.horizontalLayout1.setStretch(1, 1)

        self.verticalLayout.addLayout(self.horizontalLayout1)

        self.horizontalLayout2 = QHBoxLayout()
        self.horizontalLayout2.setObjectName(u"horizontalLayout2")
        self.functionWidget = QWidget(self.centralwidget)
        self.functionWidget.setObjectName(u"functionWidget")
        self.captureButton = QPushButton(self.functionWidget)
        self.captureButton.setObjectName(u"captureButton")
        self.captureButton.setGeometry(QRect(10, 20, 91, 31))
        self.checkBox = QCheckBox(self.functionWidget)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setGeometry(QRect(20, 70, 101, 20))

        self.horizontalLayout2.addWidget(self.functionWidget)

        self.resultWidget = QWidget(self.centralwidget)
        self.resultWidget.setObjectName(u"resultWidget")
        self.resultWidget.setStyleSheet(u"border: 1px solid black;")

        self.horizontalLayout2.addWidget(self.resultWidget)


        self.verticalLayout.addLayout(self.horizontalLayout2)

        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 1)

        self.horizontalLayout_2.addLayout(self.verticalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 1401, 33))
        self.menuFile = QMenu(self.menuBar)
        self.menuFile.setObjectName(u"menuFile")
        MainWindow.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionPreference)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        self.actionPreference.setText(QCoreApplication.translate("MainWindow", u"Preference", None))
        self.camera1Label.setText(QCoreApplication.translate("MainWindow", u"camera0", None))
        self.camera0Label.setText(QCoreApplication.translate("MainWindow", u"camera1", None))
        self.captureButton.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.checkBox.setText(QCoreApplication.translate("MainWindow", u"CheckBox", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        pass
    # retranslateUi

