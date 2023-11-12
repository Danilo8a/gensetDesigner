# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'skin_exportar.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1020, 720)
        Form.setMinimumSize(QtCore.QSize(1020, 720))
        Form.setStyleSheet("QWidget{\n"
"border: none;\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setStyleSheet("#frame{\n"
"    background-color: rgb(255, 255, 255);\n"
"}")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.graph_container = QtWidgets.QFrame(self.frame)
        self.graph_container.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.graph_container.setFrameShadow(QtWidgets.QFrame.Raised)
        self.graph_container.setObjectName("graph_container")
        self.graph_layout = QtWidgets.QVBoxLayout(self.graph_container)
        self.graph_layout.setContentsMargins(0, 0, 0, 0)
        self.graph_layout.setSpacing(0)
        self.graph_layout.setObjectName("graph_layout")
        self.verticalLayout_2.addWidget(self.graph_container)
        self.data_container = QtWidgets.QFrame(self.frame)
        self.data_container.setMaximumSize(QtCore.QSize(16777215, 120))
        self.data_container.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.data_container.setFrameShadow(QtWidgets.QFrame.Raised)
        self.data_container.setObjectName("data_container")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.data_container)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.logo = QtWidgets.QFrame(self.data_container)
        self.logo.setMaximumSize(QtCore.QSize(150, 16777215))
        self.logo.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.logo.setFrameShadow(QtWidgets.QFrame.Raised)
        self.logo.setObjectName("logo")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.logo)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label = QtWidgets.QLabel(self.logo)
        self.label.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.logo)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2)
        self.horizontalLayout.addWidget(self.logo)
        self.data = QtWidgets.QFrame(self.data_container)
        self.data.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.data.setFrameShadow(QtWidgets.QFrame.Raised)
        self.data.setObjectName("data")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.data)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_3 = QtWidgets.QLabel(self.data)
        self.label_3.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_4.addWidget(self.label_3)
        self.frame_2 = QtWidgets.QFrame(self.data)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_4.addWidget(self.frame_2)
        self.horizontalLayout.addWidget(self.data)
        self.verticalLayout_2.addWidget(self.data_container)
        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Desarrollado con:"))
        self.label_2.setText(_translate("Form", "GenSet Designer"))
        self.label_3.setText(_translate("Form", "Datos de placa."))