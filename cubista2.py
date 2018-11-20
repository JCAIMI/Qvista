# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cubista2.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1233, 777)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_3 = QtWidgets.QFrame(self.centralwidget)
        self.frame_3.setMinimumSize(QtCore.QSize(0, 100))
        self.frame_3.setMaximumSize(QtCore.QSize(16777215, 100))
        self.frame_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setLineWidth(0)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_11 = QtWidgets.QFrame(self.frame_3)
        self.frame_11.setMinimumSize(QtCore.QSize(250, 0))
        self.frame_11.setMaximumSize(QtCore.QSize(250, 16777215))
        self.frame_11.setStyleSheet("background-color:#465A63;")
        self.frame_11.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_11.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_11.setLineWidth(0)
        self.frame_11.setObjectName("frame_11")
        self.label = QtWidgets.QLabel(self.frame_11)
        self.label.setGeometry(QtCore.QRect(20, 0, 201, 71))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("qVistaLogo.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.label_3 = QtWidgets.QLabel(self.frame_11)
        self.label_3.setGeometry(QtCore.QRect(-5, 60, 261, 41))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: rgb(170, 255, 255);")
        self.label_3.setTextFormat(QtCore.Qt.RichText)
        self.label_3.setScaledContents(False)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.label_3.raise_()
        self.label.raise_()
        self.horizontalLayout.addWidget(self.frame_11)
        self.frame_12 = QtWidgets.QFrame(self.frame_3)
        self.frame_12.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_12.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_12.setLineWidth(0)
        self.frame_12.setObjectName("frame_12")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_12)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.frame_14 = QtWidgets.QFrame(self.frame_12)
        self.frame_14.setStyleSheet("background-color: #465A63;")
        self.frame_14.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_14.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_14.setLineWidth(0)
        self.frame_14.setObjectName("frame_14")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_14)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout_4.addWidget(self.frame_14)
        self.frame_15 = QtWidgets.QFrame(self.frame_12)
        self.frame_15.setStyleSheet("background-color: #79909B;\n"
"color: #FFFFFF")
        self.frame_15.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_15.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_15.setLineWidth(0)
        self.frame_15.setObjectName("frame_15")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_15)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.lblTitolProjecte = QtWidgets.QLabel(self.frame_15)
        font = QtGui.QFont()
        font.setPointSize(21)
        self.lblTitolProjecte.setFont(font)
        self.lblTitolProjecte.setObjectName("lblTitolProjecte")
        self.horizontalLayout_4.addWidget(self.lblTitolProjecte)
        self.tbEnrera = QtWidgets.QToolButton(self.frame_15)
        self.tbEnrera.setMinimumSize(QtCore.QSize(40, 40))
        self.tbEnrera.setMaximumSize(QtCore.QSize(40, 40))
        self.tbEnrera.setStyleSheet("border-color: rgb(121, 144, 155);")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("imatges//arrow-left.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tbEnrera.setIcon(icon)
        self.tbEnrera.setIconSize(QtCore.QSize(40, 40))
        self.tbEnrera.setObjectName("tbEnrera")
        self.horizontalLayout_4.addWidget(self.tbEnrera)
        self.tbEndevant = QtWidgets.QToolButton(self.frame_15)
        self.tbEndevant.setMinimumSize(QtCore.QSize(40, 40))
        self.tbEndevant.setMaximumSize(QtCore.QSize(40, 40))
        self.tbEndevant.setStyleSheet("border-color: rgb(121, 144, 155);")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("imatges//arrow-right.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tbEndevant.setIcon(icon1)
        self.tbEndevant.setIconSize(QtCore.QSize(40, 40))
        self.tbEndevant.setObjectName("tbEndevant")
        self.horizontalLayout_4.addWidget(self.tbEndevant)
        self.verticalLayout_4.addWidget(self.frame_15)
        self.horizontalLayout.addWidget(self.frame_12)
        self.frame_13 = QtWidgets.QFrame(self.frame_3)
        self.frame_13.setMinimumSize(QtCore.QSize(40, 0))
        self.frame_13.setMaximumSize(QtCore.QSize(40, 16777215))
        self.frame_13.setStyleSheet("background-color: #465A63;")
        self.frame_13.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_13.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_13.setLineWidth(0)
        self.frame_13.setObjectName("frame_13")
        self.horizontalLayout.addWidget(self.frame_13)
        self.verticalLayout.addWidget(self.frame_3)
        self.frame_9 = QtWidgets.QFrame(self.centralwidget)
        self.frame_9.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_9.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_9.setLineWidth(0)
        self.frame_9.setObjectName("frame_9")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_9)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.frame_16 = QtWidgets.QFrame(self.frame_9)
        self.frame_16.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_16.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_16.setLineWidth(0)
        self.frame_16.setObjectName("frame_16")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_16)
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frameLlegenda = QtWidgets.QFrame(self.frame_16)
        self.frameLlegenda.setMinimumSize(QtCore.QSize(250, 0))
        self.frameLlegenda.setMaximumSize(QtCore.QSize(250, 16777215))
        self.frameLlegenda.setStyleSheet("background-color: #DDDDDD")
        self.frameLlegenda.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frameLlegenda.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameLlegenda.setLineWidth(0)
        self.frameLlegenda.setObjectName("frameLlegenda")
        self.horizontalLayout_2.addWidget(self.frameLlegenda)
        self.frameCentral = QtWidgets.QFrame(self.frame_16)
        self.frameCentral.setStyleSheet("")
        self.frameCentral.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frameCentral.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frameCentral.setLineWidth(0)
        self.frameCentral.setObjectName("frameCentral")
        self.horizontalLayout_2.addWidget(self.frameCentral)
        self.frame_19 = QtWidgets.QFrame(self.frame_16)
        self.frame_19.setMinimumSize(QtCore.QSize(40, 0))
        self.frame_19.setMaximumSize(QtCore.QSize(40, 16777215))
        self.frame_19.setStyleSheet("background-color: #DDDDDD\n"
"")
        self.frame_19.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_19.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_19.setLineWidth(0)
        self.frame_19.setObjectName("frame_19")
        self.gridLayout = QtWidgets.QGridLayout(self.frame_19)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.lytBotoneraLateral = QtWidgets.QVBoxLayout()
        self.lytBotoneraLateral.setContentsMargins(8, 8, 8, 8)
        self.lytBotoneraLateral.setSpacing(10)
        self.lytBotoneraLateral.setObjectName("lytBotoneraLateral")
        self.gridLayout.addLayout(self.lytBotoneraLateral, 0, 0, 1, 1)
        self.horizontalLayout_2.addWidget(self.frame_19)
        self.frameCentral.raise_()
        self.frameLlegenda.raise_()
        self.frame_19.raise_()
        self.verticalLayout_5.addWidget(self.frame_16)
        self.frame_2 = QtWidgets.QFrame(self.frame_9)
        self.frame_2.setMinimumSize(QtCore.QSize(250, 20))
        self.frame_2.setMaximumSize(QtCore.QSize(16777215, 20))
        self.frame_2.setStyleSheet("background-color: #DDDDDD")
        self.frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setLineWidth(0)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.verticalLayout_5.addWidget(self.frame_2)
        self.verticalLayout.addWidget(self.frame_9)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1233, 34))
        self.menubar.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(15)
        self.menubar.setFont(font)
        self.menubar.setStyleSheet("background-color: rgb(47, 69, 80);\n"
"color: rgb(255, 255, 255);\n"
"")
        self.menubar.setNativeMenuBar(False)
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_3.setText(_translate("MainWindow", "Sistema d\'Informació Territorial de Barcelona"))
        self.lblTitolProjecte.setText(_translate("MainWindow", "Qualificacions urbanístiques i suspensions"))
        self.tbEnrera.setText(_translate("MainWindow", "..."))
        self.tbEndevant.setText(_translate("MainWindow", "..."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

