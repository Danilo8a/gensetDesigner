# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'data_motor.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(793, 190)
        Form.setStyleSheet("*{\n"
"border: none;\n"
"padding: 0px;\n"
"margin: 0px;\n"
"font: 57 9pt \"Inter Medium\";\n"
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
"QComboBox {\n"
"    border: 1px solid #C0C0C0;\n"
"    border-radius: 4px;\n"
"    background-color: #FFFFFF;\n"
"    padding: 2px;\n"
"}\n"
"\n"
"QComboBox:hover, QComboBox:focus {\n"
"    border: 2px solid #0078D7;\n"
"    border-radius: 4px;\n"
"}\n"
"")
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.container_data_motor = QtWidgets.QFrame(Form)
        self.container_data_motor.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.container_data_motor.setFrameShadow(QtWidgets.QFrame.Raised)
        self.container_data_motor.setObjectName("container_data_motor")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.container_data_motor)
        self.horizontalLayout.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.section_1 = QtWidgets.QFrame(self.container_data_motor)
        self.section_1.setMinimumSize(QtCore.QSize(0, 0))
        self.section_1.setMaximumSize(QtCore.QSize(100, 16777215))
        self.section_1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.section_1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.section_1.setObjectName("section_1")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.section_1)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.container_potencia = QtWidgets.QFrame(self.section_1)
        self.container_potencia.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.container_potencia.setFrameShadow(QtWidgets.QFrame.Raised)
        self.container_potencia.setObjectName("container_potencia")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.container_potencia)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.potencia_label = QtWidgets.QLabel(self.container_potencia)
        self.potencia_label.setMaximumSize(QtCore.QSize(80, 16777215))
        self.potencia_label.setObjectName("potencia_label")
        self.verticalLayout_3.addWidget(self.potencia_label)
        self.potencia_entry = QtWidgets.QLineEdit(self.container_potencia)
        self.potencia_entry.setMinimumSize(QtCore.QSize(0, 0))
        self.potencia_entry.setMaximumSize(QtCore.QSize(80, 16777215))
        self.potencia_entry.setMaxLength(100)
        self.potencia_entry.setObjectName("potencia_entry")
        self.verticalLayout_3.addWidget(self.potencia_entry)
        self.verticalLayout_2.addWidget(self.container_potencia)
        self.container_unidades = QtWidgets.QFrame(self.section_1)
        self.container_unidades.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.container_unidades.setFrameShadow(QtWidgets.QFrame.Raised)
        self.container_unidades.setObjectName("container_unidades")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.container_unidades)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.unidad_label = QtWidgets.QLabel(self.container_unidades)
        self.unidad_label.setObjectName("unidad_label")
        self.verticalLayout_4.addWidget(self.unidad_label)
        self.unidad_combo = QtWidgets.QComboBox(self.container_unidades)
        self.unidad_combo.setMinimumSize(QtCore.QSize(50, 0))
        self.unidad_combo.setMaximumSize(QtCore.QSize(60, 16777215))
        self.unidad_combo.setObjectName("unidad_combo")
        self.unidad_combo.addItem("")
        self.unidad_combo.addItem("")
        self.verticalLayout_4.addWidget(self.unidad_combo)
        self.verticalLayout_2.addWidget(self.container_unidades)
        self.container_fases = QtWidgets.QFrame(self.section_1)
        self.container_fases.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.container_fases.setFrameShadow(QtWidgets.QFrame.Raised)
        self.container_fases.setObjectName("container_fases")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.container_fases)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.fases_label = QtWidgets.QLabel(self.container_fases)
        self.fases_label.setObjectName("fases_label")
        self.verticalLayout_5.addWidget(self.fases_label)
        self.fases_combo = QtWidgets.QComboBox(self.container_fases)
        self.fases_combo.setMinimumSize(QtCore.QSize(50, 0))
        self.fases_combo.setMaximumSize(QtCore.QSize(60, 16777215))
        self.fases_combo.setObjectName("fases_combo")
        self.fases_combo.addItem("")
        self.fases_combo.addItem("")
        self.verticalLayout_5.addWidget(self.fases_combo)
        self.verticalLayout_2.addWidget(self.container_fases)
        self.horizontalLayout.addWidget(self.section_1)
        self.section_3 = QtWidgets.QFrame(self.container_data_motor)
        self.section_3.setMaximumSize(QtCore.QSize(200, 16777215))
        self.section_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.section_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.section_3.setObjectName("section_3")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.section_3)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        spacerItem = QtWidgets.QSpacerItem(20, 32, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_6.addItem(spacerItem)
        self.arranque_container = QtWidgets.QFrame(self.section_3)
        self.arranque_container.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.arranque_container.setFrameShadow(QtWidgets.QFrame.Raised)
        self.arranque_container.setObjectName("arranque_container")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.arranque_container)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setSpacing(2)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.arranque_label = QtWidgets.QLabel(self.arranque_container)
        self.arranque_label.setObjectName("arranque_label")
        self.verticalLayout_7.addWidget(self.arranque_label)
        self.arranque_combo = QtWidgets.QComboBox(self.arranque_container)
        self.arranque_combo.setMaximumSize(QtCore.QSize(200, 16777215))
        self.arranque_combo.setObjectName("arranque_combo")
        self.arranque_combo.addItem("")
        self.arranque_combo.addItem("")
        self.arranque_combo.addItem("")
        self.arranque_combo.addItem("")
        self.arranque_combo.addItem("")
        self.arranque_combo.addItem("")
        self.arranque_combo.addItem("")
        self.verticalLayout_7.addWidget(self.arranque_combo)
        self.verticalLayout_6.addWidget(self.arranque_container)
        self.tipo_container = QtWidgets.QFrame(self.section_3)
        self.tipo_container.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.tipo_container.setFrameShadow(QtWidgets.QFrame.Raised)
        self.tipo_container.setObjectName("tipo_container")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.tipo_container)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setSpacing(2)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.tipo_label = QtWidgets.QLabel(self.tipo_container)
        self.tipo_label.setObjectName("tipo_label")
        self.verticalLayout_8.addWidget(self.tipo_label)
        self.tipo_combo = QtWidgets.QComboBox(self.tipo_container)
        self.tipo_combo.setMaximumSize(QtCore.QSize(100, 16777215))
        self.tipo_combo.setObjectName("tipo_combo")
        self.tipo_combo.addItem("")
        self.tipo_combo.addItem("")
        self.verticalLayout_8.addWidget(self.tipo_combo)
        self.verticalLayout_6.addWidget(self.tipo_container)
        spacerItem1 = QtWidgets.QSpacerItem(20, 32, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_6.addItem(spacerItem1)
        self.checkBox = QtWidgets.QCheckBox(self.section_3)
        self.checkBox.setObjectName("checkBox")
        self.verticalLayout_6.addWidget(self.checkBox)
        self.horizontalLayout.addWidget(self.section_3)
        self.section_2 = QtWidgets.QFrame(self.container_data_motor)
        self.section_2.setMaximumSize(QtCore.QSize(200, 16777215))
        self.section_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.section_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.section_2.setObjectName("section_2")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.section_2)
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_12.setSpacing(0)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.frame = QtWidgets.QFrame(self.section_2)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setObjectName("label")
        self.verticalLayout_10.addWidget(self.label)
        self.comboBox = QtWidgets.QComboBox(self.frame)
        self.comboBox.setMaximumSize(QtCore.QSize(80, 16777215))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.verticalLayout_10.addWidget(self.comboBox)
        self.verticalLayout_12.addWidget(self.frame)
        self.frame_2 = QtWidgets.QFrame(self.section_2)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.label_2 = QtWidgets.QLabel(self.frame_2)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_9.addWidget(self.label_2)
        self.lineEdit = QtWidgets.QLineEdit(self.frame_2)
        self.lineEdit.setMaximumSize(QtCore.QSize(80, 16777215))
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout_9.addWidget(self.lineEdit)
        self.verticalLayout_12.addWidget(self.frame_2)
        self.frame_3 = QtWidgets.QFrame(self.section_2)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.label_3 = QtWidgets.QLabel(self.frame_3)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_11.addWidget(self.label_3)
        self.comboBox_2 = QtWidgets.QComboBox(self.frame_3)
        self.comboBox_2.setMaximumSize(QtCore.QSize(80, 16777215))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.verticalLayout_11.addWidget(self.comboBox_2)
        self.verticalLayout_12.addWidget(self.frame_3)
        spacerItem2 = QtWidgets.QSpacerItem(20, 28, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_12.addItem(spacerItem2)
        self.horizontalLayout.addWidget(self.section_2)
        self.avanzadas_container = QtWidgets.QFrame(self.container_data_motor)
        self.avanzadas_container.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.avanzadas_container.setFrameShadow(QtWidgets.QFrame.Raised)
        self.avanzadas_container.setObjectName("avanzadas_container")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(self.avanzadas_container)
        self.verticalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_13.setSpacing(2)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.fp_container = QtWidgets.QFrame(self.avanzadas_container)
        self.fp_container.setMinimumSize(QtCore.QSize(0, 0))
        self.fp_container.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.fp_container.setFrameShadow(QtWidgets.QFrame.Raised)
        self.fp_container.setObjectName("fp_container")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.fp_container)
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_14.setSpacing(0)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.label_4 = QtWidgets.QLabel(self.fp_container)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_14.addWidget(self.label_4)
        self.fp_motor = QtWidgets.QLineEdit(self.fp_container)
        self.fp_motor.setMinimumSize(QtCore.QSize(0, 20))
        self.fp_motor.setMaximumSize(QtCore.QSize(80, 16777215))
        self.fp_motor.setObjectName("fp_motor")
        self.verticalLayout_14.addWidget(self.fp_motor)
        self.verticalLayout_13.addWidget(self.fp_container)
        self.eficiencia_container = QtWidgets.QFrame(self.avanzadas_container)
        self.eficiencia_container.setMinimumSize(QtCore.QSize(0, 0))
        self.eficiencia_container.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.eficiencia_container.setFrameShadow(QtWidgets.QFrame.Raised)
        self.eficiencia_container.setObjectName("eficiencia_container")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout(self.eficiencia_container)
        self.verticalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_15.setSpacing(0)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.label_5 = QtWidgets.QLabel(self.eficiencia_container)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_15.addWidget(self.label_5)
        self.eficiencia_motor = QtWidgets.QLineEdit(self.eficiencia_container)
        self.eficiencia_motor.setMinimumSize(QtCore.QSize(0, 20))
        self.eficiencia_motor.setMaximumSize(QtCore.QSize(80, 16777215))
        self.eficiencia_motor.setObjectName("eficiencia_motor")
        self.verticalLayout_15.addWidget(self.eficiencia_motor)
        self.verticalLayout_13.addWidget(self.eficiencia_container)
        self.fp_arranque_container = QtWidgets.QFrame(self.avanzadas_container)
        self.fp_arranque_container.setMinimumSize(QtCore.QSize(0, 0))
        self.fp_arranque_container.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.fp_arranque_container.setFrameShadow(QtWidgets.QFrame.Raised)
        self.fp_arranque_container.setObjectName("fp_arranque_container")
        self.verticalLayout_16 = QtWidgets.QVBoxLayout(self.fp_arranque_container)
        self.verticalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_16.setSpacing(0)
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.label_6 = QtWidgets.QLabel(self.fp_arranque_container)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_16.addWidget(self.label_6)
        self.fp_arranque_motor = QtWidgets.QLineEdit(self.fp_arranque_container)
        self.fp_arranque_motor.setMinimumSize(QtCore.QSize(0, 20))
        self.fp_arranque_motor.setMaximumSize(QtCore.QSize(80, 16777215))
        self.fp_arranque_motor.setObjectName("fp_arranque_motor")
        self.verticalLayout_16.addWidget(self.fp_arranque_motor)
        self.verticalLayout_13.addWidget(self.fp_arranque_container)
        self.factor_carga_container = QtWidgets.QFrame(self.avanzadas_container)
        self.factor_carga_container.setMinimumSize(QtCore.QSize(0, 0))
        self.factor_carga_container.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.factor_carga_container.setFrameShadow(QtWidgets.QFrame.Raised)
        self.factor_carga_container.setObjectName("factor_carga_container")
        self.verticalLayout_17 = QtWidgets.QVBoxLayout(self.factor_carga_container)
        self.verticalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_17.setSpacing(0)
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.label_7 = QtWidgets.QLabel(self.factor_carga_container)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_17.addWidget(self.label_7)
        self.factor_carga_motor = QtWidgets.QLineEdit(self.factor_carga_container)
        self.factor_carga_motor.setMinimumSize(QtCore.QSize(0, 20))
        self.factor_carga_motor.setMaximumSize(QtCore.QSize(80, 16777215))
        self.factor_carga_motor.setObjectName("factor_carga_motor")
        self.verticalLayout_17.addWidget(self.factor_carga_motor)
        self.verticalLayout_13.addWidget(self.factor_carga_container)
        spacerItem3 = QtWidgets.QSpacerItem(20, 33, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_13.addItem(spacerItem3)
        self.horizontalLayout.addWidget(self.avanzadas_container)
        self.section_2.raise_()
        self.section_1.raise_()
        self.section_3.raise_()
        self.avanzadas_container.raise_()
        self.verticalLayout.addWidget(self.container_data_motor)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.potencia_label.setText(_translate("Form", "Potencia**"))
        self.unidad_label.setText(_translate("Form", "Unidad**"))
        self.unidad_combo.setItemText(0, _translate("Form", "HP"))
        self.unidad_combo.setItemText(1, _translate("Form", "KVA"))
        self.fases_label.setText(_translate("Form", "Fases**"))
        self.fases_combo.setItemText(0, _translate("Form", "1"))
        self.fases_combo.setItemText(1, _translate("Form", "3"))
        self.arranque_label.setText(_translate("Form", "Método de arranque**"))
        self.arranque_combo.setItemText(0, _translate("Form", "Directo"))
        self.arranque_combo.setItemText(1, _translate("Form", "Estrella - Delta"))
        self.arranque_combo.setItemText(2, _translate("Form", "Autotransformador 80"))
        self.arranque_combo.setItemText(3, _translate("Form", "Autotransformador 65"))
        self.arranque_combo.setItemText(4, _translate("Form", "Autotransformador 50"))
        self.arranque_combo.setItemText(5, _translate("Form", "Arrancador suave"))
        self.arranque_combo.setItemText(6, _translate("Form", "Variador de frecuencia"))
        self.tipo_label.setText(_translate("Form", "Tipo de motor**"))
        self.tipo_combo.setItemText(0, _translate("Form", "NEMA"))
        self.tipo_combo.setItemText(1, _translate("Form", "IEC"))
        self.checkBox.setText(_translate("Form", "Opciones avanzadas"))
        self.label.setText(_translate("Form", "Código de letra (NEMA)**"))
        self.comboBox.setItemText(0, _translate("Form", "A"))
        self.comboBox.setItemText(1, _translate("Form", "B"))
        self.comboBox.setItemText(2, _translate("Form", "C"))
        self.comboBox.setItemText(3, _translate("Form", "D"))
        self.comboBox.setItemText(4, _translate("Form", "E"))
        self.comboBox.setItemText(5, _translate("Form", "F"))
        self.comboBox.setItemText(6, _translate("Form", "G"))
        self.comboBox.setItemText(7, _translate("Form", "H"))
        self.comboBox.setItemText(8, _translate("Form", "I"))
        self.comboBox.setItemText(9, _translate("Form", "J"))
        self.comboBox.setItemText(10, _translate("Form", "K"))
        self.comboBox.setItemText(11, _translate("Form", "L"))
        self.comboBox.setItemText(12, _translate("Form", "M"))
        self.comboBox.setItemText(13, _translate("Form", "N"))
        self.comboBox.setItemText(14, _translate("Form", "O"))
        self.comboBox.setItemText(15, _translate("Form", "P"))
        self.comboBox.setItemText(16, _translate("Form", "Q"))
        self.comboBox.setItemText(17, _translate("Form", "R"))
        self.comboBox.setItemText(18, _translate("Form", "S"))
        self.comboBox.setItemText(19, _translate("Form", "T"))
        self.comboBox.setItemText(20, _translate("Form", "U"))
        self.comboBox.setItemText(21, _translate("Form", "V"))
        self.label_2.setText(_translate("Form", "Relación Ia/In (IEC)**"))
        self.label_3.setText(_translate("Form", "Pulsos (VFD)**"))
        self.comboBox_2.setItemText(0, _translate("Form", "6"))
        self.comboBox_2.setItemText(1, _translate("Form", "12"))
        self.comboBox_2.setItemText(2, _translate("Form", "24"))
        self.label_4.setText(_translate("Form", "Factor de potencia"))
        self.label_5.setText(_translate("Form", "Eficiencia (%)"))
        self.label_6.setText(_translate("Form", "Factor de potencia (arranque)"))
        self.label_7.setText(_translate("Form", "Factor de carga (%)"))