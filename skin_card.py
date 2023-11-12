# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'skin_card.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_card_widget(object):
    def setupUi(self, card_widget):
        card_widget.setObjectName("card_widget")
        card_widget.resize(810, 180)
        card_widget.setMinimumSize(QtCore.QSize(0, 180))
        card_widget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        card_widget.setStyleSheet("*{\n"
"    border: none;\n"
"padding: 0px;\n"
"margin: 0px;\n"
"font: 57 10pt \"Inter Medium\";\n"
"}\n"
"\n"
"#content_card{\n"
"    border: 1px solid gray;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QFrame{\n"
"    border: none;\n"
"}\n"
"\n"
"#icon_card{\n"
"    background-color: rgb(255, 255, 255);\n"
"    border-right: 1px solid gray;\n"
"    border-top-left-radius: 4px;\n"
"    border-bottom-left-radius: 4px;\n"
"}\n"
"\n"
" QPushButton{\n"
"    background-color: rgba(255, 255, 255, 0);\n"
"    font: 57 10pt \"Inter Medium\";\n"
"    padding: 5px;\n"
"    border-radius: 2px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    border: 1px solid rgba(112, 112, 112, 150);\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"    background-color: rgb(171, 171, 171);\n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"QLineEdit {\n"
"    border: 1px solid #C0C0C0;\n"
"    border-radius: 4px;\n"
"    padding: 2px;\n"
"}\n"
"\n"
"QLineEdit:hover, QLineEdit:focus {\n"
"    border: 2px solid #0078D7;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"/*Etilos combox*/\n"
"QComboBox {\n"
"    border: 1px solid #C0C0C0;\n"
"    border-radius: 4px;\n"
"   background-color: #FFFFFF;\n"
"    padding: 2px;\n"
"}\n"
"QComboBox:hover, QComboBox:focus {\n"
"    border: 2px solid #0078D7;\n"
"    border-radius: 4px;\n"
"}\n"
"QComboBox::drop-down{\n"
"    border: 0px;\n"
"}\n"
"\n"
"QComboBox::drop-down:hover{\n"
"    background-color: rgb(216, 216, 216);\n"
"}\n"
"QComboBox::down-arrow{\n"
"    image: url(img/down.png);\n"
"    width: 15px;\n"
"    height: 15px;\n"
"    margin: 10px;\n"
"}\n"
"QComboBox QAbstractItemView{\n"
"    border: 1px solid rgba(0, 0, 0, 10%);\n"
"    padding: 2px;\n"
"    outline: 0px;\n"
"    box-shadow: none;\n"
"}\n"
"\n"
"QScrollBar:vertical {     \n"
"       border: 1px solid #999999;\n"
"        background:white;\n"
"        width:10px;\n"
"        border-radius: 4px;\n"
"        margin: 0px 0px 0px 0px;\n"
"    }\n"
"    QScrollBar::handle:vertical {\n"
"        background: rgb(42, 42, 43);\n"
"        min-height: 0px;\n"
"        border-radius: 4px;\n"
"    }\n"
"    QScrollBar::add-line:vertical {\n"
"        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"        stop: 0 rgb(32, 47, 130), stop: 0.5 rgb(32, 47, 130),  stop:1 rgb(32, 47, 130));\n"
"        height: 0px;\n"
"        subcontrol-position: bottom;\n"
"        subcontrol-origin: margin;\n"
"    }\n"
"    QScrollBar::sub-line:vertical {\n"
"        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"        stop: 0  rgb(32, 47, 130), stop: 0.5 rgb(32, 47, 130),  stop:1 rgb(32, 47, 130));\n"
"        height: 0 px;\n"
"        subcontrol-position: top;\n"
"        subcontrol-origin: margin;\n"
"    }\n"
"\n"
"QCheckBox{\n"
"    font: 57 10pt \"Inter Medium\";\n"
"}\n"
"QCheckBox::indicator {\n"
"    border: 1px solid rgb(111, 114, 115);\n"
"    border-radius: 2px;\n"
" }\n"
"QCheckBox::indicator:checked {\n"
"    background-color: rgb(73, 147, 220);\n"
"}\n"
"")
        self.verticalLayout = QtWidgets.QVBoxLayout(card_widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.content_card = QtWidgets.QFrame(card_widget)
        self.content_card.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.content_card.setFrameShadow(QtWidgets.QFrame.Raised)
        self.content_card.setObjectName("content_card")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.content_card)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.icon_card = QtWidgets.QFrame(self.content_card)
        self.icon_card.setMinimumSize(QtCore.QSize(150, 0))
        self.icon_card.setMaximumSize(QtCore.QSize(200, 16777215))
        self.icon_card.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.icon_card.setFrameShadow(QtWidgets.QFrame.Raised)
        self.icon_card.setObjectName("icon_card")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.icon_card)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.icon_title_container = QtWidgets.QFrame(self.icon_card)
        self.icon_title_container.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.icon_title_container.setFrameShadow(QtWidgets.QFrame.Raised)
        self.icon_title_container.setObjectName("icon_title_container")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.icon_title_container)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.title_load = QtWidgets.QLabel(self.icon_title_container)
        self.title_load.setMaximumSize(QtCore.QSize(16777215, 20))
        self.title_load.setAlignment(QtCore.Qt.AlignCenter)
        self.title_load.setObjectName("title_load")
        self.verticalLayout_3.addWidget(self.title_load)
        self.container_icon = QtWidgets.QFrame(self.icon_title_container)
        self.container_icon.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.container_icon.setFrameShadow(QtWidgets.QFrame.Raised)
        self.container_icon.setObjectName("container_icon")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.container_icon)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem = QtWidgets.QSpacerItem(69, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.icon_load = QtWidgets.QLabel(self.container_icon)
        self.icon_load.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_load.setText("")
        self.icon_load.setTextFormat(QtCore.Qt.AutoText)
        self.icon_load.setAlignment(QtCore.Qt.AlignCenter)
        self.icon_load.setObjectName("icon_load")
        self.horizontalLayout_4.addWidget(self.icon_load)
        spacerItem1 = QtWidgets.QSpacerItem(68, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.verticalLayout_3.addWidget(self.container_icon)
        self.verticalLayout_2.addWidget(self.icon_title_container)
        self.icon_card_button_container = QtWidgets.QFrame(self.icon_card)
        self.icon_card_button_container.setMaximumSize(QtCore.QSize(16777215, 40))
        self.icon_card_button_container.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.icon_card_button_container.setFrameShadow(QtWidgets.QFrame.Raised)
        self.icon_card_button_container.setObjectName("icon_card_button_container")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.icon_card_button_container)
        self.horizontalLayout_2.setContentsMargins(0, 5, 0, 10)
        self.horizontalLayout_2.setSpacing(2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.card_delete = QtWidgets.QPushButton(self.icon_card_button_container)
        self.card_delete.setObjectName("card_delete")
        self.horizontalLayout_2.addWidget(self.card_delete)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.verticalLayout_2.addWidget(self.icon_card_button_container)
        self.horizontalLayout.addWidget(self.icon_card)
        self.data_card = QtWidgets.QFrame(self.content_card)
        self.data_card.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.data_card.setFrameShadow(QtWidgets.QFrame.Raised)
        self.data_card.setObjectName("data_card")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.data_card)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.content_center_data = QtWidgets.QFrame(self.data_card)
        self.content_center_data.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.content_center_data.setFrameShadow(QtWidgets.QFrame.Raised)
        self.content_center_data.setObjectName("content_center_data")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.content_center_data)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(4)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.content_data_frame = QtWidgets.QFrame(self.content_center_data)
        self.content_data_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.content_data_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.content_data_frame.setObjectName("content_data_frame")
        self.content_data_layout = QtWidgets.QVBoxLayout(self.content_data_frame)
        self.content_data_layout.setContentsMargins(2, 2, 2, 2)
        self.content_data_layout.setSpacing(0)
        self.content_data_layout.setObjectName("content_data_layout")
        self.verticalLayout_5.addWidget(self.content_data_frame)
        self.frame_error_mess = QtWidgets.QFrame(self.content_center_data)
        self.frame_error_mess.setMaximumSize(QtCore.QSize(16777215, 20))
        self.frame_error_mess.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_error_mess.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_error_mess.setObjectName("frame_error_mess")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.frame_error_mess)
        self.verticalLayout_6.setContentsMargins(10, 0, 0, 0)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.error_message = QtWidgets.QLabel(self.frame_error_mess)
        self.error_message.setText("")
        self.error_message.setObjectName("error_message")
        self.verticalLayout_6.addWidget(self.error_message)
        self.verticalLayout_5.addWidget(self.frame_error_mess)
        self.horizontalLayout_3.addWidget(self.content_center_data)
        spacerItem4 = QtWidgets.QSpacerItem(15, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem4)
        self.cantidad_container = QtWidgets.QFrame(self.data_card)
        self.cantidad_container.setMaximumSize(QtCore.QSize(180, 16777215))
        self.cantidad_container.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.cantidad_container.setFrameShadow(QtWidgets.QFrame.Raised)
        self.cantidad_container.setObjectName("cantidad_container")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.cantidad_container)
        self.verticalLayout_4.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_4.setSpacing(2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        spacerItem5 = QtWidgets.QSpacerItem(20, 50, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem5)
        self.cantidad_label = QtWidgets.QLabel(self.cantidad_container)
        self.cantidad_label.setMaximumSize(QtCore.QSize(80, 16777215))
        self.cantidad_label.setObjectName("cantidad_label")
        self.verticalLayout_4.addWidget(self.cantidad_label)
        self.cantidad_input = QtWidgets.QLineEdit(self.cantidad_container)
        self.cantidad_input.setMaximumSize(QtCore.QSize(80, 16777215))
        self.cantidad_input.setObjectName("cantidad_input")
        self.verticalLayout_4.addWidget(self.cantidad_input)
        self.label = QtWidgets.QLabel(self.cantidad_container)
        self.label.setObjectName("label")
        self.verticalLayout_4.addWidget(self.label)
        self.step_combo = QtWidgets.QComboBox(self.cantidad_container)
        self.step_combo.setMaximumSize(QtCore.QSize(60, 16777215))
        self.step_combo.setObjectName("step_combo")
        self.step_combo.addItem("")
        self.step_combo.addItem("")
        self.step_combo.addItem("")
        self.step_combo.addItem("")
        self.step_combo.addItem("")
        self.step_combo.addItem("")
        self.step_combo.addItem("")
        self.step_combo.addItem("")
        self.step_combo.addItem("")
        self.step_combo.addItem("")
        self.verticalLayout_4.addWidget(self.step_combo)
        self.label_2 = QtWidgets.QLabel(self.cantidad_container)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_4.addWidget(self.label_2)
        self.lineEdit = QtWidgets.QLineEdit(self.cantidad_container)
        self.lineEdit.setMaximumSize(QtCore.QSize(60, 16777215))
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout_4.addWidget(self.lineEdit)
        spacerItem6 = QtWidgets.QSpacerItem(20, 50, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem6)
        self.horizontalLayout_3.addWidget(self.cantidad_container)
        self.horizontalLayout.addWidget(self.data_card)
        self.verticalLayout.addWidget(self.content_card)

        self.retranslateUi(card_widget)
        QtCore.QMetaObject.connectSlotsByName(card_widget)

    def retranslateUi(self, card_widget):
        _translate = QtCore.QCoreApplication.translate
        card_widget.setWindowTitle(_translate("card_widget", "Form"))
        self.title_load.setText(_translate("card_widget", "Título carga"))
        self.card_delete.setText(_translate("card_widget", "Eliminar"))
        self.cantidad_label.setText(_translate("card_widget", "Cantidad*"))
        self.label.setText(_translate("card_widget", "Step*"))
        self.step_combo.setItemText(0, _translate("card_widget", "1"))
        self.step_combo.setItemText(1, _translate("card_widget", "2"))
        self.step_combo.setItemText(2, _translate("card_widget", "3"))
        self.step_combo.setItemText(3, _translate("card_widget", "4"))
        self.step_combo.setItemText(4, _translate("card_widget", "5"))
        self.step_combo.setItemText(5, _translate("card_widget", "6"))
        self.step_combo.setItemText(6, _translate("card_widget", "7"))
        self.step_combo.setItemText(7, _translate("card_widget", "8"))
        self.step_combo.setItemText(8, _translate("card_widget", "9"))
        self.step_combo.setItemText(9, _translate("card_widget", "10"))
        self.label_2.setText(_translate("card_widget", "Factor de simultaneidad*"))
