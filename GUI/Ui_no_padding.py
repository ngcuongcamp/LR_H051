# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\NguyenCuong\C\HO-51_SPLITED\GUI\no_padding.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(452, 222)
        MainWindow.setMinimumSize(QtCore.QSize(452, 222))
        MainWindow.setMaximumSize(QtCore.QSize(452, 222))
        MainWindow.setSizeIncrement(QtCore.QSize(452, 222))
        MainWindow.setBaseSize(QtCore.QSize(452, 222))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.ContentWrapper = QtWidgets.QGroupBox(self.centralwidget)
        self.ContentWrapper.setGeometry(QtCore.QRect(0, 0, 452, 222))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ContentWrapper.sizePolicy().hasHeightForWidth())
        self.ContentWrapper.setSizePolicy(sizePolicy)
        self.ContentWrapper.setMinimumSize(QtCore.QSize(452, 222))
        self.ContentWrapper.setMaximumSize(QtCore.QSize(452, 222))
        self.ContentWrapper.setSizeIncrement(QtCore.QSize(452, 240))
        self.ContentWrapper.setBaseSize(QtCore.QSize(480, 240))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.ContentWrapper.setFont(font)
        self.ContentWrapper.setStyleSheet("border: 2px solid #ccc; border-radius: 4px; background-color:rgb(237, 245, 255)")
        self.ContentWrapper.setTitle("")
        self.ContentWrapper.setObjectName("ContentWrapper")
        self.CameraSpan2 = QtWidgets.QGroupBox(self.ContentWrapper)
        self.CameraSpan2.setGeometry(QtCore.QRect(301, 3, 149, 218))
        self.CameraSpan2.setStyleSheet("background-color: #000")
        self.CameraSpan2.setTitle("")
        self.CameraSpan2.setObjectName("CameraSpan2")
        self.CameraLabel2 = QtWidgets.QLabel(self.CameraSpan2)
        self.CameraLabel2.setGeometry(QtCore.QRect(0, 0, 149, 33))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.CameraLabel2.setFont(font)
        self.CameraLabel2.setStyleSheet("\n"
"font: 10pt \"Segoe UI\"; border: none; color: #fff; background: none; font-weight:bold; background-color:rgba(0, 170, 255,0.5)")
        self.CameraLabel2.setAlignment(QtCore.Qt.AlignCenter)
        self.CameraLabel2.setObjectName("CameraLabel2")
        self.CameraFrame2 = QtWidgets.QLabel(self.CameraSpan2)
        self.CameraFrame2.setGeometry(QtCore.QRect(0, 0, 148, 218))
        self.CameraFrame2.setStyleSheet("border: 1px solid rgb(85, 85, 127);")
        self.CameraFrame2.setText("")
        self.CameraFrame2.setObjectName("CameraFrame2")
        self.CameraFrame2.raise_()
        self.CameraLabel2.raise_()
        self.CameraSpan1 = QtWidgets.QGroupBox(self.ContentWrapper)
        self.CameraSpan1.setGeometry(QtCore.QRect(152, 3, 148, 218))
        self.CameraSpan1.setStyleSheet("background-color: #000;")
        self.CameraSpan1.setTitle("")
        self.CameraSpan1.setObjectName("CameraSpan1")
        self.CameraLabel1 = QtWidgets.QLabel(self.CameraSpan1)
        self.CameraLabel1.setGeometry(QtCore.QRect(0, 0, 149, 33))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.CameraLabel1.setFont(font)
        self.CameraLabel1.setStyleSheet("\n"
"font: 10pt \"Segoe UI\"; border: none; color: #fff; background: none; font-weight:bold; background-color:rgba(0, 170, 255,0.5)")
        self.CameraLabel1.setAlignment(QtCore.Qt.AlignCenter)
        self.CameraLabel1.setObjectName("CameraLabel1")
        self.CameraFrame1 = QtWidgets.QLabel(self.CameraSpan1)
        self.CameraFrame1.setGeometry(QtCore.QRect(0, 0, 148, 218))
        self.CameraFrame1.setStyleSheet("border: 1px solid rgb(85, 85, 127);")
        self.CameraFrame1.setText("")
        self.CameraFrame1.setObjectName("CameraFrame1")
        self.CameraFrame1.raise_()
        self.CameraLabel1.raise_()
        self.ResultSpan = QtWidgets.QGroupBox(self.ContentWrapper)
        self.ResultSpan.setGeometry(QtCore.QRect(2, 3, 149, 218))
        self.ResultSpan.setStyleSheet("background-color:qlineargradient(spread:pad, x1:0, y1:0.0738636, x2:1, y2:0, stop:0 rgba(128, 128, 128, 255), stop:1 rgba(255, 255, 255, 255)); border: 1px solid rgb(85, 85, 127);")
        self.ResultSpan.setTitle("")
        self.ResultSpan.setObjectName("ResultSpan")
        self.ResultContent = QtWidgets.QLabel(self.ResultSpan)
        self.ResultContent.setGeometry(QtCore.QRect(1, 0, 148, 217))
        self.ResultContent.setStyleSheet("font-size: 16px;\n"
"font: 16pt \"Segoe UI\"; border: 1px solid #ccc; color: #999; background-color: #fff;")
        self.ResultContent.setAlignment(QtCore.Qt.AlignCenter)
        self.ResultContent.setObjectName("ResultContent")
        self.UpdateButton = QtWidgets.QPushButton(self.ResultSpan)
        self.UpdateButton.setGeometry(QtCore.QRect(28, 185, 95, 27))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.UpdateButton.sizePolicy().hasHeightForWidth())
        self.UpdateButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.UpdateButton.setFont(font)
        self.UpdateButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.UpdateButton.setStyleSheet("background-color:rgb(0, 111, 0); color: #fff; border: 1px solid #fff; border-radius: 8px; ")
        self.UpdateButton.setObjectName("UpdateButton")
        self.ResultLabel = QtWidgets.QLabel(self.ResultSpan)
        self.ResultLabel.setGeometry(QtCore.QRect(0, 0, 149, 33))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.ResultLabel.setFont(font)
        self.ResultLabel.setStyleSheet("\n"
"font: 10pt \"Segoe UI\"; border: none; color: #fff; background: none; font-weight:bold; background-color: rgba(85, 170, 255,0.9)")
        self.ResultLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.ResultLabel.setObjectName("ResultLabel")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Scanner L&R_H501"))
        self.CameraLabel2.setText(_translate("MainWindow", "CAMERA 2"))
        self.CameraLabel1.setText(_translate("MainWindow", "CAMERA 1"))
        self.ResultContent.setText(_translate("MainWindow", "NONE"))
        self.UpdateButton.setText(_translate("MainWindow", "UPDATE"))
        self.ResultLabel.setText(_translate("MainWindow", "RESULT"))
