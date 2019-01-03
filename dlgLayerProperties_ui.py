# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dlgLayerProperties.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_LayerProperties(object):
    def setupUi(self, LayerProperties):
        LayerProperties.setObjectName("LayerProperties")
        LayerProperties.resize(313, 384)
        self.gridLayout_2 = QtWidgets.QGridLayout(LayerProperties)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_3 = QtWidgets.QLabel(LayerProperties)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_5.addWidget(self.label_3)
        self.cbTipField = QtWidgets.QComboBox(LayerProperties)
        self.cbTipField.setMinimumSize(QtCore.QSize(140, 0))
        self.cbTipField.setMaximumSize(QtCore.QSize(140, 16777215))
        self.cbTipField.setObjectName("cbTipField")
        self.horizontalLayout_5.addWidget(self.cbTipField)
        self.gridLayout_2.addLayout(self.horizontalLayout_5, 1, 0, 1, 1)
        self.frame = QtWidgets.QFrame(LayerProperties)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setContentsMargins(-1, 0, -1, -1)
        self.gridLayout.setObjectName("gridLayout")
        self.chkScale = QtWidgets.QCheckBox(self.frame)
        self.chkScale.setObjectName("chkScale")
        self.gridLayout.addWidget(self.chkScale, 0, 0, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem = QtWidgets.QSpacerItem(30, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.lblMaxScale = QtWidgets.QLabel(self.frame)
        self.lblMaxScale.setEnabled(True)
        self.lblMaxScale.setObjectName("lblMaxScale")
        self.horizontalLayout_4.addWidget(self.lblMaxScale)
        self.maxScaleSpinBox = QtWidgets.QSpinBox(self.frame)
        self.maxScaleSpinBox.setEnabled(True)
        self.maxScaleSpinBox.setMinimumSize(QtCore.QSize(140, 0))
        self.maxScaleSpinBox.setMaximumSize(QtCore.QSize(16777215, 21))
        self.maxScaleSpinBox.setMinimum(1)
        self.maxScaleSpinBox.setMaximum(100000000)
        self.maxScaleSpinBox.setSingleStep(1000)
        self.maxScaleSpinBox.setProperty("value", 1000)
        self.maxScaleSpinBox.setObjectName("maxScaleSpinBox")
        self.horizontalLayout_4.addWidget(self.maxScaleSpinBox)
        self.gridLayout.addLayout(self.horizontalLayout_4, 1, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem1 = QtWidgets.QSpacerItem(30, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.lblMinScale = QtWidgets.QLabel(self.frame)
        self.lblMinScale.setEnabled(True)
        self.lblMinScale.setObjectName("lblMinScale")
        self.horizontalLayout_3.addWidget(self.lblMinScale)
        self.minScaleSpinBox = QtWidgets.QSpinBox(self.frame)
        self.minScaleSpinBox.setEnabled(True)
        self.minScaleSpinBox.setMinimumSize(QtCore.QSize(140, 0))
        self.minScaleSpinBox.setMaximumSize(QtCore.QSize(16777215, 21))
        self.minScaleSpinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.minScaleSpinBox.setAccelerated(True)
        self.minScaleSpinBox.setMinimum(1)
        self.minScaleSpinBox.setMaximum(100000000)
        self.minScaleSpinBox.setSingleStep(1000)
        self.minScaleSpinBox.setProperty("value", 1000000)
        self.minScaleSpinBox.setObjectName("minScaleSpinBox")
        self.horizontalLayout_3.addWidget(self.minScaleSpinBox)
        self.gridLayout.addLayout(self.horizontalLayout_3, 2, 0, 1, 1)
        self.gridLayout_2.addWidget(self.frame, 7, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lblDisplayField = QtWidgets.QLabel(LayerProperties)
        self.lblDisplayField.setObjectName("lblDisplayField")
        self.horizontalLayout_2.addWidget(self.lblDisplayField)
        self.cboDisplayFieldName = QtWidgets.QComboBox(LayerProperties)
        self.cboDisplayFieldName.setMinimumSize(QtCore.QSize(140, 0))
        self.cboDisplayFieldName.setMaximumSize(QtCore.QSize(200, 21))
        self.cboDisplayFieldName.setObjectName("cboDisplayFieldName")
        self.horizontalLayout_2.addWidget(self.cboDisplayFieldName)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(LayerProperties)
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 5, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(LayerProperties)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout_2.addWidget(self.buttonBox, 9, 0, 1, 1)
        self.sliderTransparencia = QtWidgets.QSlider(LayerProperties)
        self.sliderTransparencia.setOrientation(QtCore.Qt.Horizontal)
        self.sliderTransparencia.setObjectName("sliderTransparencia")
        self.gridLayout_2.addWidget(self.sliderTransparencia, 4, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(LayerProperties)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.txtLayerName = QtWidgets.QLineEdit(LayerProperties)
        self.txtLayerName.setMinimumSize(QtCore.QSize(140, 0))
        self.txtLayerName.setMaximumSize(QtCore.QSize(200, 21))
        self.txtLayerName.setCursorPosition(0)
        self.txtLayerName.setObjectName("txtLayerName")
        self.horizontalLayout.addWidget(self.txtLayerName)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 15, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_2.addItem(spacerItem3, 8, 0, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(20, 15, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_2.addItem(spacerItem4, 6, 0, 1, 1)

        self.retranslateUi(LayerProperties)
        self.buttonBox.accepted.connect(LayerProperties.accept)
        self.buttonBox.rejected.connect(LayerProperties.reject)
        QtCore.QMetaObject.connectSlotsByName(LayerProperties)

    def retranslateUi(self, LayerProperties):
        _translate = QtCore.QCoreApplication.translate
        LayerProperties.setWindowTitle(_translate("LayerProperties", "Layer properties"))
        self.label_3.setText(_translate("LayerProperties", "Camp a visualitzar quan  passem el cursor per damunt: "))
        self.chkScale.setText(_translate("LayerProperties", "Dependència de escala"))
        self.lblMaxScale.setText(_translate("LayerProperties", "Escala màxima"))
        self.lblMinScale.setText(_translate("LayerProperties", "Escala mínima"))
        self.lblDisplayField.setText(_translate("LayerProperties", "Camp a mostrar"))
        self.label_2.setText(_translate("LayerProperties", "Transparència de la capa"))
        self.label.setText(_translate("LayerProperties", "Nom del nivell"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    LayerProperties = QtWidgets.QDialog()
    ui = Ui_LayerProperties()
    ui.setupUi(LayerProperties)
    LayerProperties.show()
    sys.exit(app.exec_())

