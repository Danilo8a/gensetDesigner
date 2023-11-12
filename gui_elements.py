import cmath
import json
import math
import pickle
import sqlite3
import sys

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation
from PyQt5.QtGui import QImage, QMouseEvent, QMovie
from PyQt5.QtWidgets import QApplication

from FunctionPoints import FunctionPoints
from skin_temp_mess import Ui_Form as temp_mess
from skin_card import Ui_card_widget
from data_lum import Ui_Form as data_lum
from data_motor import Ui_Form as data_motor
from data_nonlineal import Ui_Form as data_nonlineal
from data_resistencia import Ui_Form as data_resistor
from dialog_simple_skin import Ui_Dialog
from data_air import Ui_Form as data_air
from skin_load_view import Ui_Form as load_skin
from skin_data_dim import Ui_Form as data_dim_skin
from skin_nuevo_genset import Ui_Form as datadb
from skin_project_item import Ui_Form as project


class GUIInputDBData(QtWidgets.QDialog):
    end_signal = QtCore.pyqtSignal(bool)

    CORRECT_LINE_EDIT_CONTENT_STYLES = "QLineEdit{background-color: rgb(42, 42, 43);border: 1px solid rgb(86, 88, 89);" \
                                       "border-radius: 5px;color: rgb(255, 255, 255);padding: 2px;}QLineEdit:focus{" \
                                       "border: 1px solid rgb(52, 129, 200);}QLineEdit:hover{border: 1px solid white;}"

    INCORRECT_LINE_EDIT_CONTENT_STYLES = "QLineEdit{background-color: rgb(42, 42, 43);border: 1px solid #F82727;" \
                                         "border-radius: 5px;color: rgb(255, 255, 255);padding: 2px;}QLineEdit:focus{" \
                                         "border: 1px solid rgb(52, 129, 200);}QLineEdit:hover{border: 1px solid white;}"

    CORRECT_TABLE_WIDGET_CONTENT_STYLES = "QHeaderView::section{background: rgb(60, 63, 65);border: 1px solid rgba(112, 112, 112, 150);}QTableCornerButton::section{background: rgb(60, 63, 65);}QTableWidget {border: 1px solid rgba(112, 112, 112, 150);border-radius: 5px;gridline-color: rgba(112, 112, 112, 150);text-align: center; vertical-align: middle;}QScrollBar:vertical {border: 1px solid #999999;background:white;width:10px;border-radius: 2px;margin: 0px 0px 0px 0px;}QScrollBar::handle:vertical {background: rgb(42, 42, 43);min-height: 0px;border-radius: 2px;}QScrollBar::add-line:vertical {background: qlineargradient(x1:0, y1:0, x2:1, y2:0,stop: 0 rgb(32, 47, 130), stop: 0.5 rgb(32, 47, 130),  stop:1 rgb(32, 47, 130));height: 0px;subcontrol-position: bottom;subcontrol-origin: margin;}QScrollBar::sub-line:vertical {background: qlineargradient(x1:0, y1:0, x2:1, y2:0,stop: 0  rgb(32, 47, 130), stop: 0.5 rgb(32, 47, 130),  stop:1 rgb(32, 47, 130));height: 0 px;subcontrol-position: top;subcontrol-origin: margin;}QScrollBar:horizontal {border: 1px solid #999999;background:white;height:10px;border-radius: 2px;margin: 0px 0px 0px 0px;}QScrollBar::handle:horizontal {background: rgb(42, 42, 43);min-height: 0px;border-radius: 2px;}QScrollBar::add-line:horizontal {background: qlineargradient(x1:0, y1:0, x2:1, y2:0,stop: 0 rgb(32, 47, 130), stop: 0.5 rgb(32, 47, 130),  stop:1 rgb(32, 47, 130));width: 0px;subcontrol-position: bottom;subcontrol-origin: margin;}QScrollBar::sub-line:horizontal {background: qlineargradient(x1:0, y1:0, x2:1, y2:0,stop: 0  rgb(32, 47, 130), stop: 0.5 rgb(32, 47, 130),  stop:1 rgb(32, 47, 130));width: 0 px;subcontrol-position: top;subcontrol-origin: margin;}"

    INCORRECT_TABLE_WIDGET_CONTENT_STYLES = "QHeaderView::section{background: rgb(60, 63, 65);border: 1px solid rgba(112, 112, 112, 150);}QTableCornerButton::section{background: rgb(60, 63, 65);}QTableWidget {border: 1px solid red;border-radius: 5px;gridline-color: rgba(112, 112, 112, 150);text-align: center; vertical-align: middle;}QScrollBar:vertical {border: 1px solid #999999;background:white;width:10px;border-radius: 2px;margin: 0px 0px 0px 0px;}QScrollBar::handle:vertical {background: rgb(42, 42, 43);min-height: 0px;border-radius: 2px;}QScrollBar::add-line:vertical {background: qlineargradient(x1:0, y1:0, x2:1, y2:0,stop: 0 rgb(32, 47, 130), stop: 0.5 rgb(32, 47, 130),  stop:1 rgb(32, 47, 130));height: 0px;subcontrol-position: bottom;subcontrol-origin: margin;}QScrollBar::sub-line:vertical {background: qlineargradient(x1:0, y1:0, x2:1, y2:0,stop: 0  rgb(32, 47, 130), stop: 0.5 rgb(32, 47, 130),  stop:1 rgb(32, 47, 130));height: 0 px;subcontrol-position: top;subcontrol-origin: margin;}QScrollBar:horizontal {border: 1px solid #999999;background:white;height:10px;border-radius: 2px;margin: 0px 0px 0px 0px;}QScrollBar::handle:horizontal {background: rgb(42, 42, 43);min-height: 0px;border-radius: 2px;}QScrollBar::add-line:horizontal {background: qlineargradient(x1:0, y1:0, x2:1, y2:0,stop: 0 rgb(32, 47, 130), stop: 0.5 rgb(32, 47, 130),  stop:1 rgb(32, 47, 130));width: 0px;subcontrol-position: bottom;subcontrol-origin: margin;}QScrollBar::sub-line:horizontal {background: qlineargradient(x1:0, y1:0, x2:1, y2:0,stop: 0  rgb(32, 47, 130), stop: 0.5 rgb(32, 47, 130),  stop:1 rgb(32, 47, 130));width: 0 px;subcontrol-position: top;subcontrol-origin: margin;}"

    def __init__(self, parent):
        super().__init__(parent)
        self.ui = datadb()
        self.ui.setupUi(self)
        # Quitando el frame
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowOpacity(1)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.ui.container_nuevo_titulo.mouseMoveEvent = self._mouse_move_menu
        self.ui.container_nuevo_titulo.mousePressEvent = self._press_mouse_bar

        self.ui.cerrar_nuevo.clicked.connect(self._close_dialog)
        self.ui.toolButton.clicked.connect(self._aceptar)
        self.is_checked = False

        self.mouseMoveEvent = self._check_values
        self.enterEvent = self._check_values
        self.leaveEvent = self._check_values

        self.ui.tabla_input.resizeColumnsToContents()

    def _check_values(self, event):
        line_edits = self.findChildren(QtWidgets.QLineEdit)
        line_edits.pop(line_edits.index(self.ui.voltaje))
        aux_str = [line_edits.pop(line_edits.index(self.ui.lineEdit_9)),
                   line_edits.pop(line_edits.index(self.ui.lineEdit_11)),
                   line_edits.pop(line_edits.index(self.ui.lineEdit_10)),
                   line_edits.pop(line_edits.index(self.ui.lineEdit_12))]

        self.is_checked = True
        check_word = []
        for line in line_edits:
            if len(line.text()) == 0:
                line.setStyleSheet(self.INCORRECT_LINE_EDIT_CONTENT_STYLES)
                check_word.append(False)
            else:
                try:
                    if "." in line.text():
                        aux = float(line.text())
                    else:
                        aux = int(line.text())

                    line.setText(str(abs(aux)))
                    line.setStyleSheet(self.CORRECT_LINE_EDIT_CONTENT_STYLES)
                    check_word.append(True)
                except ValueError:
                    line.setStyleSheet(self.INCORRECT_LINE_EDIT_CONTENT_STYLES)
                    check_word.append(False)

        for line in aux_str:
            if len(line.text()) == 0:
                line.setStyleSheet(self.INCORRECT_LINE_EDIT_CONTENT_STYLES)
                check_word.append(False)
            else:
                line.setStyleSheet(self.CORRECT_LINE_EDIT_CONTENT_STYLES)
                check_word.append(True)

        if len(self.ui.voltaje.text()) == 0:
            self.ui.voltaje.setStyleSheet(self.INCORRECT_LINE_EDIT_CONTENT_STYLES)
            self.ui.tabla_input.verticalHeaderItem(0).setText("V1")
            self.ui.tabla_input.verticalHeaderItem(1).setText("V2")
            self.ui.tabla_input.verticalHeaderItem(2).setText("V3")
            check_word.append(False)
        else:
            list_voltage = self.ui.voltaje.text().strip().split(",")
            if len(list_voltage) == 1 and not self.ui.voltaje.text().isnumeric():
                self.ui.voltaje.setStyleSheet(self.INCORRECT_LINE_EDIT_CONTENT_STYLES)
                self.ui.tabla_input.verticalHeaderItem(0).setText("V1")
                self.ui.tabla_input.verticalHeaderItem(1).setText("V2")
                self.ui.tabla_input.verticalHeaderItem(2).setText("V3")
                check_word.append(False)
            elif len(list_voltage) == 1 and self.ui.voltaje.text().isnumeric():
                self.ui.voltaje.setStyleSheet(self.CORRECT_LINE_EDIT_CONTENT_STYLES)
                self.ui.tabla_input.verticalHeaderItem(0).setText(self.ui.voltaje.text())
                check_word.append(True)
                self.ui.tabla_input.verticalHeaderItem(1).setText("V2")
                self.ui.tabla_input.verticalHeaderItem(2).setText("V3")
            elif 0 < len(list_voltage) <= 3 and len(list(filter(lambda x: x.isnumeric(), list_voltage))) == len(
                    list_voltage):
                for i in list_voltage:
                    self.ui.tabla_input.verticalHeaderItem(list_voltage.index(i)).setText(i)
                    self.ui.voltaje.setStyleSheet(self.CORRECT_LINE_EDIT_CONTENT_STYLES)
                if len(list_voltage) == 2:
                    self.ui.tabla_input.verticalHeaderItem(2).setText("V3")
                check_word.append(True)
            else:
                check_word.append(False)

            for i in range(0, len(list_voltage)):
                for j in range(0, 13):
                    item = self.ui.tabla_input.item(i, j)
                    if item is None:
                        self.ui.tabla_input.setStyleSheet(self.INCORRECT_TABLE_WIDGET_CONTENT_STYLES)
                        check_word.append(False)
                        break
                    elif item.text() == "":
                        self.ui.tabla_input.setItem(i, j, None)
                        self.ui.tabla_input.setStyleSheet(self.INCORRECT_TABLE_WIDGET_CONTENT_STYLES)
                        check_word.append(False)
                        break
                    elif not item.text().isnumeric():
                        self.ui.tabla_input.setStyleSheet(self.INCORRECT_TABLE_WIDGET_CONTENT_STYLES)
                        check_word.append(False)
                        break
                    elif item.text().isnumeric():
                        self.ui.tabla_input.setStyleSheet(self.CORRECT_TABLE_WIDGET_CONTENT_STYLES)
                        check_word.append(True)

        for i in check_word:
            self.is_checked &= i

    def _aceptar(self):
        self._check_values(None)
        aux_dialog = GUIBaseDialog(None, GUIBaseDialog.SET_ICON_DIALOG_ERROR)
        if self.is_checked:
            aux = {
                "voltaje": self.ui.voltaje.text().strip().split(","),
                "potencia_kva": float(self.ui.lineEdit.text()),
                "potencia_kw": float(self.ui.lineEdit_2.text()),
                "frecuencia": int(self.ui.lineEdit_3.text()),
                "fases": int(self.ui.comboBox.currentText()),
                "xd": float(self.ui.lineEdit_4.text()),
                "xd_p": float(self.ui.lineEdit_5.text()),
                "xd_pp": float(self.ui.lineEdit_6.text()),
                "aislamiento": self.ui.comboBox_2.currentText(),
                "modelo": self.ui.lineEdit_9.text(),
                "fabricante": self.ui.lineEdit_11.text(),
                "combustible": self.ui.lineEdit_10.text(),
                "xq": float(self.ui.lineEdit_7.text()),
                "xq_pp": float(self.ui.lineEdit_8.text()),
                "url": self.ui.lineEdit_12.text()
            }
            list_voltaje = self.ui.voltaje.text().split(",")
            aux_dict = {}
            aux_y = [0, 2, 5, 7, 10, 12, 15, 17, 20, 22, 25, 27, 30]

            for i in list_voltaje:
                aux_x = []
                for j in range(0, len(aux_y)):
                    k = list_voltaje.index(i)
                    aux_x.append(float(self.ui.tabla_input.item(k, j).text()))
                if len(aux_x) == len(set(aux_x)):
                    aux_dict[i] = pickle.dumps(FunctionPoints(aux_x, aux_y))
                else:
                    aux_dialog.setDialogMessTitle("Curva de Voltaje Dip Incorrecta.")
                    aux_dialog.setDialogMessInformation(
                        f"Alguna de las curvas de voltaje dip ingresadas en la tabla contiene valores repetidos."
                        f" Compruebe los datos recolectados antes de ingresar valores en la tabla."
                    )
                    aux_dialog.exec()
                    return
            self.add_machine(
                aux["voltaje"],
                aux["potencia_kva"],
                aux["potencia_kw"],
                aux["frecuencia"],
                aux["fases"],
                aux["xd"],
                aux["xd_p"],
                aux["xd_pp"],
                aux["xq"],
                aux["xq_pp"],
                aux["aislamiento"],
                aux["modelo"],
                aux["combustible"],
                aux["fabricante"],
                aux["url"],
                aux_dict
            )
            self.end_signal.emit(True)
            self.close()

    def add_machine(self, voltage, power_kva, power_kw, frequency, phase, xd, xd_prima, xd_primaprima, xq,
                    xq_primaprima,
                    insulation_system, alternator_model, fuel, manufacturer, url, curve):
        # creamos la conexión a la base de datos
        conn = sqlite3.connect('gensets.db.db')

        # formateamos el voltaje como una cadena de texto
        voltage_str = ",".join(str(v) for v in voltage)

        # insertamos la máquina en la tabla
        conn.execute(
            f"INSERT INTO machine (voltage, power_kva, power_kw, frequency, phase, xd, xd_prima, xd_primaprima, xq, xq_primaprima, insulation_system, alternator_model, fuel, manufacturer, url, curve) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (voltage_str, power_kva, power_kw, frequency, phase, json.dumps(xd), json.dumps(xd_prima),
             json.dumps(xd_primaprima), json.dumps(xq), json.dumps(xq_primaprima), insulation_system, alternator_model,
             fuel, manufacturer, url, pickle.dumps(curve)))

        # guardamos los cambios y cerramos la conexión
        conn.commit()
        conn.close()

    def _mouse_move_menu(self, event):
        # Movimiento de la ventana
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.clickPosition)
            self.clickPosition = event.globalPos()
            event.accept()

    def _press_mouse_bar(self, event):
        self.deltaX = event.globalPos() - self.pos()
        self.deltaX = self.deltaX.x()
        self.clickPosition = event.globalPos()
        self.lastPointClicked = event.globalPos()

    def _close_dialog(self):
        self.close()


class GUIProjectItem(QtWidgets.QWidget):
    delete_signal = QtCore.pyqtSignal(dict)
    open_me_signal = QtCore.pyqtSignal(dict)

    def __init__(self, parent, name, path, time):
        super().__init__(parent)
        self.ui = project()
        self.ui.setupUi(self)
        # Quitando el frame
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowOpacity(1)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.name = name
        self.path = path
        self.fecha = time

        self.ui.nombre_proyecto.setText(name)
        self.ui.ruta_proyecto.setText(path)
        self.ui.fecha_modificacion.setText(time)

        self.ui.eliminar.clicked.connect(self.delete)
        self.mousePressEvent = self.open_me

    def delete(self):
        aux_dialog = GUIBaseDialog(self.parent(), GUIBaseDialog.SET_ICON_DIALOG_INFORMATION)
        aux_dialog.setDialogMessTitle("¿Está seguro que desea eliminar el proyecto?")
        aux_dialog.setDialogMessInformation("Si presiona aceptar, la referencia al proyecto será eliminada.")
        if aux_dialog.exec():
            self.parent().layout().removeWidget(self)
            self.deleteLater()
            self.delete_signal.emit({
                "to_delete": self
            })

    def open_me(self, event):
        self.open_me_signal.emit({
            "to_open": self
        })


class GUIBaseDialog(QtWidgets.QDialog):
    # Constantes para los íconos de las ventanas
    SET_ICON_DIALOG_QUESTION = 0
    SET_ICON_DIALOG_INFORMATION = 1
    SET_ICON_DIALOG_ERROR = 2
    SET_ICON_DIALOG_WARN = 3
    SET_ICON_DIALOG_NO_ICON = 4

    def __init__(self, parent, type_mess_dialog: int):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # Quita el marco del sistema operativo
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowOpacity(1)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # Movimiento de la ventana de diálogo
        self.ui.mess_title.mouseMoveEvent = self._mouse_move_menu
        self.ui.mess_title.mousePressEvent = self._press_mouse_bar
        self.ui.plain_text_report.setVisible(False)

        # Asignación del ícono
        if type_mess_dialog == 0:
            self.ui.icon_dialog.setPixmap(QtGui.QPixmap("./img/dialog_question_icon.png"))
        elif type_mess_dialog == 1:
            self.ui.icon_dialog.setPixmap(QtGui.QPixmap("./img/dialog_information_icon.png"))
        elif type_mess_dialog == 2:
            self.ui.icon_dialog.setPixmap(QtGui.QPixmap("./img/dialog_error_icon.png"))
        elif type_mess_dialog == 3:
            self.ui.icon_dialog.setPixmap(QtGui.QPixmap("./img/dialog_warn_icon.png"))

        # Acciones de la ventana de diálogo
        self.ui.dialog_cerrar.clicked.connect(self._close_dialog)
        self.ui.mess_button_box.accepted.connect(self.accept)
        self.ui.mess_button_box.rejected.connect(self.reject)

    def setDialogMessTitle(self, title: str):
        self.ui.mess_title.setText(title)

    def setDialogMessInformation(self, info: str):
        self.ui.mess_info.setText(info)

    def _close_dialog(self):
        self.close()

    def _mouse_move_menu(self, event):
        # Movimiento de la ventana
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.clickPosition)
            self.clickPosition = event.globalPos()
            event.accept()

    def _press_mouse_bar(self, event):
        self.deltaX = event.globalPos() - self.pos()
        self.deltaX = self.deltaX.x()
        self.clickPosition = event.globalPos()
        self.lastPointClicked = event.globalPos()

    def set_plain_mess(self, mess):
        self.ui.plain_text_report.setVisible(True)
        self.ui.plain_text_report.setPlainText(mess)


class GUILoadView(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = load_skin()
        self.ui.setupUi(self)

        # Obtener el tamaño del padre
        parent_width = self.parent().width()
        parent_height = self.parent().height()

        # Obtener el tamaño del widget
        widget_height = self.height()

        # Calcular la posición central
        x = parent_width // 2
        y = (parent_height - widget_height) // 2

        # Mover el widget a la posición central
        self.move(x, y)

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowOpacity(1)

        movie = QMovie('./img/load.gif')
        movie.setScaledSize(self.ui.preloader.size())
        self.ui.preloader.setMovie(movie)
        movie.start()

    def update_message(self, mess):
        self.ui.load_mess.setText(mess)

    def update_location(self, pos: tuple):
        x = (pos[0] - self.width()) // 2
        y = (pos[1] - self.height()) // 2
        self.move(x, y)


class GUITemporalMessage(QtWidgets.QDialog):
    POSITION_BL = 0
    POSITION_BR = 1
    POSITION_TL = 2
    POSITION_TR = 3
    POSITION_TC = 4
    POSITION_BC = 5

    SET_ICON_DIALOG_QUESTION = 10
    SET_ICON_DIALOG_INFORMATION = 11
    SET_ICON_DIALOG_ERROR = 12

    def __init__(self, parent, title, mess, icon_mess, position=POSITION_BR, fade=True, fade_time=5000,
                 close_time=10000):
        super().__init__(parent)
        self.ui = temp_mess()
        self.ui.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.position = position
        self.fade = fade
        self.ui.title_mess.setText(title)
        self.ui.label.setText(mess)
        self.ui.close_button.clicked.connect(self._close_dialog)

        # Quita el marco del sistema operativo
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowOpacity(1)

        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(fade_time)  # Duración en milisegundos
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)

        self.timer = QTimer()
        self.timer.setInterval(close_time)  # Tiempo en milisegundos
        self.timer.timeout.connect(self.close_dialog)

        # Estableciendo el ícono
        self.icon_mess = icon_mess
        if icon_mess == 10:
            self.ui.icon.setPixmap(QtGui.QPixmap("./img/pregunta.png"))
        elif icon_mess == 11:
            self.ui.icon.setPixmap(QtGui.QPixmap("./img/exclamacion.png"))
        elif icon_mess == 12:
            self.ui.icon.setPixmap(QtGui.QPixmap("./img/error.png"))

        self.br = [
            int(self.parent().width() - self.size().width() - 20),
            int(self.parent().height() - self.size().height() + 5)
        ]
        self.bl = [
            10,
            int(self.parent().height() - self.size().height() + 20)
        ]
        self.tl = [
            10,
            40
        ]
        self.tr = [
            int(self.parent().width() - self.size().width() - 10),
            40
        ]
        self.tc = [
            int(self.parent().width() / 2 - self.size().width() / 2),
            40
        ]
        self.bc = [
            int(self.parent().width() / 2 - self.size().width() / 2),
            int(self.parent().height() - self.size().height() + 10)
        ]

        if position == self.POSITION_TL:
            self.move(self.parent().pos().x() + self.tl[0], self.parent().pos().y() + self.tl[1])
            self.x_init = self.tl[0]
            self.y_init = self.tl[1]
        elif position == self.POSITION_BR:
            self.move(self.parent().pos().x() + self.br[0], self.parent().pos().y() + self.br[1])
            self.x_init = self.br[0]
            self.y_init = self.br[1]
        elif position == self.POSITION_BL:
            self.move(self.parent().pos().x() + self.bl[0], self.parent().pos().y() + self.bl[1])
            self.x_init = self.bl[0]
            self.y_init = self.bl[1]
        elif position == self.POSITION_TR:
            self.move(self.parent().pos().x() + self.tr[0], self.parent().pos().y() + self.tr[1])
            self.x_init = self.tr[0]
            self.y_init = self.tr[1]
        elif position == self.POSITION_TC:
            self.move(self.parent().pos().x() + self.tc[0], self.parent().pos().y() + self.tc[1])
            self.x_init = self.tc[0]
            self.y_init = self.tc[1]
        elif position == self.POSITION_BC:
            self.move(int(self.parent().pos().x() + self.bc[0]), int(self.parent().pos().y() + self.bc[1]))
            self.x_init = self.bc[0]
            self.y_init = self.bc[1]

        self.setMouseTracking(True)
        self.show()

    def _close_dialog(self):
        self.accept()
        self.setParent(None)
        self.deleteLater()
        self.close()

    def showEvent(self, event):
        super().showEvent(event)
        self.timer.start()

    def close_dialog(self):
        self.timer.stop()
        if self.fade:
            self.animation.start()
            self.animation.finished.connect(self.close)
        else:
            self.close()

    def enterEvent(self, event: QMouseEvent):
        self.timer.stop()
        self.animation.stop()
        self.setWindowOpacity(1.0)

    def leaveEvent(self, event: QMouseEvent):
        self.timer.start()
        self.animation.start()

    def get_title(self):
        return self.ui.title_mess.text()

    def get_mess(self):
        return self.ui.label.text()

    def get_icon_type(self):
        return self.icon_mess

    def get_position(self):
        return self.position


class GUIDataSizing(QtWidgets.QDialog):
    data_for_emit = QtCore.pyqtSignal(dict)
    actualizar = QtCore.pyqtSignal(bool)
    CORRECT_LINE_EDIT_CONTENT_STYLES = "QLineEdit{background-color: rgb(42, 42, 43);border: 1px solid rgb(86, 88, 89);" \
                                       "border-radius: 5px;color: rgb(255, 255, 255);padding: 2px;}QLineEdit:focus{" \
                                       "border: 1px solid rgb(52, 129, 200);}QLineEdit:hover{border: 1px solid white;}"

    INCORRECT_LINE_EDIT_CONTENT_STYLES = "QLineEdit{background-color: rgb(42, 42, 43);border: 1px solid #F82727;" \
                                         "border-radius: 5px;color: rgb(255, 255, 255);padding: 2px;}QLineEdit:focus{" \
                                         "border: 1px solid rgb(52, 129, 200);}QLineEdit:hover{border: 1px solid white;}"

    def __init__(self, parent):
        super().__init__(parent)
        self.ui = data_dim_skin()
        self.ui.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.is_checked = False
        self.values = dict()

        # Quita el marco del sistema operativo
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowOpacity(1)

        self.ui.voltaje_dip.setEnabled(False)
        self._toogle_iso_8528()

        self.ui.title_frame.mousePressEvent = self._press_mouse_bar
        self.ui.title_frame.mouseMoveEvent = self._mouse_move_menu
        self.ui.close_button.clicked.connect(self._close_dialog)

        self.mouseMoveEvent = self._check_values
        self.mousePressEvent = self._check_values
        self.enterEvent = self._check_values
        self.leaveEvent = self._check_values

        self.ui.siguiente_dim.clicked.connect(self._continue_sizing_process)
        self.ui.iso_8528.currentIndexChanged.connect(self._toogle_iso_8528)

        self._linea_voltage = 208

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Enter:
            print("Hola")

    def _toogle_iso_8528(self):
        if self.ui.iso_8528.currentText() == "G1":
            self.ui.voltaje_dip.setText("25")
        elif self.ui.iso_8528.currentText() == "G2":
            self.ui.voltaje_dip.setText("20")
        else:
            self.ui.voltaje_dip.setText("15")

    def _continue_sizing_process(self):
        self._check_values(None)
        aux_dialog = GUIBaseDialog(None, GUIBaseDialog.SET_ICON_DIALOG_ERROR)
        if self.is_checked:
            self.values = {
                "name": self.ui.nombre_proyecto.text(),
                "voltaje": self.ui.sistem_voltaje.currentText(),
                "fases": int(self.ui.combo_fases.currentText()),
                "frecuencia": int(self.ui.frecuencia_sistema.currentText()),
                "altura": float(self.ui.altura_msnm.text()),
                "temperatura": float(self.ui.temperatura_sistema.text()),
                "tiempo_servicio": float(self.ui.tiempo_servicio.text()),
                "reserva": float(self.ui.porcentaje_reserva.text()),
                "voltaje_dip": int(self.ui.voltaje_dip.text()),
                "combustible": self.ui.tipo_combustible.currentText(),
                "ciclo_trabajo": self.ui.ciclo_trabajo.currentText(),
                "ISO_8528": self.ui.iso_8528.currentText(),
                "THD": float(self.ui.thd.text()),
                "Descripcion": self.ui.descripcion.text(),
                "Contacto": self.ui.contacto.text()
            }
            conn = sqlite3.connect('gensets.db.db')
            c = conn.cursor()
            c.execute(
                "SELECT voltage, frequency FROM machine WHERE frequency = ? AND voltage LIKE ? AND phase = ?",
                [self.values["frecuencia"], f"%{self.values['voltaje']}%", self.values["fases"]]
            )
            results = c.fetchall()
            conn.close()
            if self.values['tiempo_servicio'] > 8760:
                aux_dialog.setDialogMessTitle("Tiempo de servicio incorrecto.")
                aux_dialog.setDialogMessInformation(
                    f"Según la norma NFAP 110, el tiempo anual de servicio de un grupo electrógeno no debe superar las 8250 h/año."
                    f" El sistema actual posee un tiempo estimado de serivicio anual de {int(self.values['tiempo_servicio'])}h/año, superior al indicado por la norma.")
                aux_dialog.exec()
            elif self.values['THD'] < 5 or self.values['THD'] > 15:
                aux_dialog.setDialogMessTitle("TDH fuera de rango.")
                aux_dialog.setDialogMessInformation(
                    f"La distorsión armónica total para el diseño de un sistema con grupos electrógenos, debe encontrarse en el rango del 5% al 15%.")
                aux_dialog.exec()
            elif self.values['temperatura'] < 5 or self.values['temperatura'] > 80:
                aux_dialog.setDialogMessTitle("Temperatura fuera de rango.")
                aux_dialog.setDialogMessInformation(
                    f"La temperatura indicada se encuentra fuera del rango óptimo de diseño, comprendido entre 5°C y 80°C.")
                aux_dialog.exec()
            elif self.values['altura'] < 0 or self.values['altura'] > 4500:
                aux_dialog.setDialogMessTitle("Altura (m.s.n.m.) fuera de rango.")
                aux_dialog.setDialogMessInformation(
                    f"La altura indicada se encuentra fuera del rango óptimo de diseño, comprendido entre 0 y 4500 m.s.n.m.")
                aux_dialog.exec()
            elif len(results) > 0:
                self.data_for_emit.emit(self.values)
            else:
                GUITemporalMessage(self.parent(), "Generadores no disponibles.",
                                   "La base de datos no cuenta con generadores"
                                   " que tengan estas características", 11, position=4)

        else:
            aux_dialog.setDialogMessTitle("Error al ingresar los datos.")
            aux_dialog.setDialogMessInformation("Uno o más datos no poseen el formato correcto.")
            aux_dialog.exec()

    def _close_dialog(self):
        self.close()

    def _mouse_move_menu(self, event):
        # Movimiento de la ventana
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.clickPosition)
            self.clickPosition = event.globalPos()
            event.accept()

    def _press_mouse_bar(self, event):
        self.deltaX = event.globalPos() - self.pos()
        self.deltaX = self.deltaX.x()
        self.clickPosition = event.globalPos()
        self.lastPointClicked = event.globalPos()

    def _check_values(self, event):
        line_edits = self.findChildren(QtWidgets.QLineEdit)
        only_text = [line_edits.pop(line_edits.index(self.ui.nombre_proyecto)),
                     line_edits.pop(line_edits.index(self.ui.voltaje_dip)),
                     line_edits.pop(line_edits.index(self.ui.descripcion)),
                     line_edits.pop(line_edits.index(self.ui.contacto))]
        check_word = []
        self.is_checked = True
        for line in only_text:
            if len(line.text()) == 0:
                line.setStyleSheet(self.INCORRECT_LINE_EDIT_CONTENT_STYLES)
                check_word.append(False)
            else:
                line.setStyleSheet(self.CORRECT_LINE_EDIT_CONTENT_STYLES)
                check_word.append(True)

        for line in line_edits:
            if len(line.text()) == 0:
                line.setStyleSheet(self.INCORRECT_LINE_EDIT_CONTENT_STYLES)
                check_word.append(False)
            else:
                try:
                    if "." in line.text():
                        aux = float(line.text())
                    else:
                        aux = int(line.text())
                    line.setText(str(abs(aux)))
                    line.setStyleSheet(self.CORRECT_LINE_EDIT_CONTENT_STYLES)
                    check_word.append(True)
                except ValueError:
                    line.setStyleSheet(self.INCORRECT_LINE_EDIT_CONTENT_STYLES)
                    check_word.append(False)

        for i in check_word:
            self.is_checked &= i


class AbstractCardListElement(QtWidgets.QWidget):

    def __init__(self, parent, data_panel=None, initial_values=None):
        super().__init__(parent)
        self.ui = Ui_card_widget()
        self.ui.setupUi(self)
        self.ui.error_message.setText("")
        self.ui.cantidad_input.setText("1")
        self.ui.lineEdit.setText("1")

        self.ui.data_card.mousePressEvent = self._display_power
        self.ui.data_card.enterEvent = self._display_power
        self.ui.data_card.leaveEvent = self._display_power
        self.ui.data_card.keyPressEvent = self._enter_press
        self.ui.error_message.setText(f"Potencia de arranque: {0.0}kW - {0.0}kVA | Potencia en marcha: {0.0}kW - {0.0}kVA")

        if initial_values is not None and initial_values is not False and initial_values is not True:
            self._setup_parameters(initial_values)

        if data_panel is not None:
            self.data_panel = data_panel
            self.ui.content_data_layout.addWidget(data_panel)
            self.data_panel.signal_error.connect(self._actualizar_error)
        self.ui.card_delete.clicked.connect(self._remove_me)

    def _display_power(self, event):

        if self.data_panel.is_checked():
            power = self.get_apparent_power()
            active_star = round(power["power_star"], 2)
            reactive_star = power["reactive_star"]
            s_star = round(math.sqrt(active_star**2 + reactive_star**2), 2)

            active_run = round(power["power_run"], 2)
            reactive_run = power["reactive_run"]
            s_run = round(math.sqrt(active_run ** 2 + reactive_run ** 2), 2)
            self.ui.error_message.setText(f"Potencia de arranque: {active_star}kW - {s_star}kVA | Potencia en marcha: {active_run}kW - {s_run}kVA")
        else:
            self.ui.error_message.setText(f"Potencia de arranque: {0.0}kW - {0.0}kVA | Potencia en marcha: {0.0}kW - {0.0}kVA")

    def _enter_press(self, event):
        if event.key() == Qt.Key_Enter:
            self._display_power(None)

    def _actualizar_error(self, mess: str):
        self.ui.error_message.setText(mess)

    def get_values(self) -> dict:
        return self.data_panel.get_values() | {
            "Cantidad": int(self.ui.cantidad_input.text()),
            "Step": int(self.ui.step_combo.currentText()),
            "Factor_simultaneidad": float(self.ui.lineEdit.text())
        }

    def _check_values(self):
        pass

    def get_apparent_power(self) -> dict:
        pass

    def _remove_me(self):
        self.parent().layout().removeWidget(self)
        self.deleteLater()

    def set_icon(self, image: QImage = None, url: str = ""):
        if image is not None:
            pix_map = QtGui.QPixmap.fromImage(image)
        elif url != "":
            pix_map = QtGui.QPixmap(url)
        else:
            raise AttributeError("Debe ingresar una imagen mediante 'image' o 'url'")

        self.ui.icon_load.setPixmap(pix_map)
        self.ui.icon_load.setScaledContents(True)

    def set_card_title(self, title: str):
        self.ui.title_load.setText(title)

    def get_data_for_package(self):
        pass

    def _setup_parameters(self, input_dict):
        pass


# Carga adaptada
class LumCardListElement(AbstractCardListElement):

    def __init__(self, parent, initial_values=None):
        self.panel = DataLum(self)
        super().__init__(parent, data_panel=self.panel, initial_values=initial_values)

    def get_step(self):
        return self.get_values()["Step"]

    def _setup_parameters(self, input_dict):
        if "Potencia" in input_dict:
            self.panel.ui.potencia_iluminacion.setText(str(input_dict["Potencia"]))
        if "Unidad" in input_dict:
            if input_dict["Unidad"] == "kW":
                self.panel.ui.unidad_iluminacion.setCurrentIndex(0)
            else:
                self.panel.ui.unidad_iluminacion.setCurrentIndex(1)
        if "Tipo iluminacion" in input_dict:
            if input_dict["Tipo iluminacion"] == "LED":
                self.panel.ui.tipo_iluminacion.setCurrentIndex(0)
            elif input_dict["Tipo iluminacion"] == "Fluorescente":
                self.panel.ui.tipo_iluminacion.setCurrentIndex(1)
            elif input_dict["Tipo iluminacion"] == "Incandescente":
                self.panel.ui.tipo_iluminacion.setCurrentIndex(2)
            elif input_dict["Tipo iluminacion"] == "HID":
                self.panel.ui.tipo_iluminacion.setCurrentIndex(3)
        if "FP" in input_dict:
            self.panel.ui.fp_lum.setText(str(input_dict["FP"]))

        self.ui.cantidad_input.setText(str(input_dict["Cantidad"]))
        self.ui.step_combo.setCurrentText(str(input_dict["Step"]))
        self.ui.lineEdit.setText(str(input_dict["Factor_simultaneidad"]))

    def get_description(self) -> dict:
        return {
            "step": self.get_values()["Step"],
            "Description": f"{self.get_values()['Cantidad']} Luminaria de {self.get_values()['Potencia']} {self.get_values()['Unidad']}",
            "starting type": "Directo",
            "kW": self.get_apparent_power()['power_run'],
            "kVA": self.get_apparent_power()['power_run'] / self.get_values()["FP"],
            "kW_start": "--",
            "kVA_start": "--",
            "Volt_dip": "--"
        }

    def get_apparent_power(self) -> dict:
        power_factor = self.get_values()["FP"]
        Potencia = self.get_values()["Potencia"]
        unidad = self.get_values()["Unidad"]
        tipo = self.get_values()["Tipo iluminacion"]
        cantidad = self.get_values()["Cantidad"]
        step = self.get_values()["Step"]
        f_sim = self.get_values()["Factor_simultaneidad"]

        if tipo == "Incandescente":
            power_factor = 1

        if unidad == "kVA":
            aux_power = Potencia * cantidad * f_sim
        else:
            aux_power = Potencia * cantidad * f_sim / power_factor
        return {
            "power_star": aux_power * power_factor,
            "reactive_star": abs(cmath.sqrt(aux_power ** 2 - (aux_power * power_factor) ** 2)),
            "power_run": aux_power * power_factor,
            "reactive_run": abs(cmath.sqrt(aux_power ** 2 - (aux_power * power_factor) ** 2)),
            "step": step
        }

    def get_data_for_package(self):
        return {
            "type": "LumCardListElement",
            "data": self.get_values()
        }


# Carga adaptada
class MotorCardListElement(AbstractCardListElement):

    def __init__(self, parent, initial_values=None, fases=3):
        self.panel = DataMotor(self)
        super().__init__(parent, data_panel=self.panel, initial_values=initial_values)
        if fases == 1:
            self.panel.ui.fases_combo.setCurrentText("1")
            self.panel.ui.fases_combo.setEnabled(False)

    def get_step(self):
        return self.get_values()["Step"]

    def get_description(self) -> dict:
        return {
            "step": self.get_values()["Step"],
            "Description": f"{self.get_values()['Cantidad']} Motor de {self.get_values()['Potencia']} {self.get_values()['Unidad']} de {self.get_values()['Fases']} fases",
            "starting type": self.get_values()['Metodo_arranque'],
            "kW": self.get_apparent_power()['power_run'],
            "kVA": abs(cmath.sqrt(
                self.get_apparent_power()['power_run'] ** 2 + self.get_apparent_power()['reactive_run'] ** 2)),
            "kW_start": self.get_apparent_power()['power_star'],
            "kVA_start": abs(cmath.sqrt(
                self.get_apparent_power()['power_star'] ** 2 + self.get_apparent_power()['reactive_star'] ** 2)),
            "Volt_dip": "--"
        }

    def get_apparent_power(self) -> dict:
        values = self.get_values()

        codigo = {
            "A": 1.57,
            "B": 3.35,
            "C": 3.77,
            "D": 4.25,
            "E": 4.75,
            "F": 5.30,
            "G": 5.95,
            "H": 6.70,
            "J": 7.55,
            "K": 8.50,
            "L": 9.50,
            "M": 10.60,
            "N": 11.85,
            "P": 13.25,
            "R": 15,
            "S": 17,
            "T": 19,
            "U": 21.20,
            "V": 23
        }

        if not self.get_values()["Avanzado"]:
            fp = 0.8
            eficiencia = 0.95
            fp_arr = 0.2
            f_carga = 1
        else:
            fp = values["factor_power"]
            eficiencia = values["eficiencia"]
            fp_arr = values["factor_arr"]
            f_carga = values["factor_carga"]

        if values["Metodo_arranque"] == "Directo" or values["Metodo_arranque"] == "Variador de frecuencia":
            f_l = 1 ** 2
        elif values["Metodo_arranque"] == "Estrella - Delta":
            f_l = 1 / 3
        elif values["Metodo_arranque"] == "Autotransformador 80":
            f_l = 0.80 ** 2
        elif values["Metodo_arranque"] == "Autotransformador 65":
            f_l = 0.65 ** 2
        elif values["Metodo_arranque"] == "Autotransformador 50":
            f_l = 0.500 ** 2
        elif values["Metodo_arranque"] == "Arrancador suave":
            f_l = 0.40

        if values["Tipo"] == "NEMA":
            if values["Unidad"] == "HP":
                power_run = ((values["Potencia"] * 0.746) / (fp * eficiencia)) * values["Cantidad"] * f_carga * values[
                    "Factor_simultaneidad"]
                power = values["Potencia"] * float(codigo[values["Codigo"]]) * f_l * values["Cantidad"]
            else:
                power = (((values["Potencia"] * fp * eficiencia) / 0.746) * float(codigo[values["Codigo"]])) * values["Cantidad"] * f_l
                power_run = values["Potencia"] * values["Cantidad"] * f_carga * values["Factor_simultaneidad"]
        else:
            if values["Unidad"] == "Hp":
                power = ((values["Potencia"] * 0.746) / fp ) * values["Cantidad"] * f_l * values["Relacion"]
                power_run = ((values["Potencia"] * 0.746) / (fp * eficiencia)) * values["Cantidad"] * f_carga * values[
                    "Factor_simultaneidad"]
            else:
                power = values["Potencia"] * values["Cantidad"] * f_l * values["Relacion"] / eficiencia
                power_run = values["Potencia"] * values["Cantidad"] * f_carga * values["Factor_simultaneidad"]

        if values["Metodo_arranque"] == "Variador de frecuencia":
            power = power_run
            if not self.get_values()["Avanzado"]:
                fp_arr = fp

        return {
            "power_star": power * fp_arr,
            "reactive_star": abs(cmath.sqrt((power ** 2) - (power * fp_arr) ** 2)),
            "power_run": power_run * fp,
            "reactive_run": abs(cmath.sqrt((power_run ** 2) - (power_run * fp) ** 2)),
            "step": values["Step"]
        }

    def get_data_for_package(self):
        return {
            "type": "MotorCardListElement",
            "data": self.get_values()
        }

    def _setup_parameters(self, input_dict):
        if "Potencia" in input_dict:
            self.panel.ui.potencia_entry.setText(str(input_dict["Potencia"]))
        if "Unidad" in input_dict:
            self.panel.ui.unidad_combo.setCurrentText(str(input_dict["Unidad"]))
        if "Fases" in input_dict:
            self.panel.ui.fases_combo.setCurrentText(str(input_dict["Fases"]))
        if "Metodo_arranque" in input_dict:
            self.panel.ui.arranque_combo.setCurrentText(str(input_dict["Metodo_arranque"]))
        if "Tipo" in input_dict:
            if input_dict["Tipo"] == "NEMA":
                self.panel.ui.tipo_combo.setCurrentIndex(0)
            else:
                self.panel.ui.tipo_combo.setCurrentIndex(1)
        if "Avanzado" in input_dict:
            if input_dict["Avanzado"]:
                self.panel.ui.checkBox.setChecked(True)
            else:
                self.panel.ui.checkBox.setChecked(False)
        if "Codigo" in input_dict:
            self.panel.ui.comboBox.setCurrentText(str(input_dict["Codigo"]))
        if "Relacion" in input_dict:
            self.panel.ui.lineEdit.setText(str(input_dict["Relacion"]))
        if "VFD" in input_dict:
            self.panel.ui.comboBox_2.setCurrentText(str(input_dict["VFD"]))
        if "factor_power" in input_dict:
            self.panel.ui.fp_motor.setText(str(input_dict["factor_power"]))
        if "eficiencia" in input_dict:
            self.panel.ui.eficiencia_motor.setText(str(input_dict["eficiencia"] * 100))
        if "factor_arr" in input_dict:
            self.panel.ui.fp_arranque_motor.setText(str(input_dict["factor_arr"]))
        if "factor_carga" in input_dict:
            self.panel.ui.factor_carga_motor.setText(str(input_dict["factor_carga"] * 100))

        self.ui.cantidad_input.setText(str(input_dict["Cantidad"]))
        self.ui.step_combo.setCurrentText(str(input_dict["Step"]))
        self.ui.lineEdit.setText(str(input_dict["Factor_simultaneidad"]))


# Carga adaptada
class ResistanceCardListElement(AbstractCardListElement):

    def __init__(self, parent, initial_values=None, fases=3):
        self.panel = DataResistor(self)
        super().__init__(parent, self.panel, initial_values=initial_values)
        if fases == 1:
            self.panel.ui.fases_combo.setCurrentText("1")
            self.panel.ui.fases_combo.setEnabled(False)

    def get_apparent_power(self) -> dict:
        return {
            "power_star": self.get_values()["Potencia"] * self.get_values()["Cantidad"] * self.get_values()[
                "Factor_simultaneidad"],
            "power_run": self.get_values()["Potencia"] * self.get_values()["Cantidad"] * self.get_values()[
                "Factor_simultaneidad"],
            "reactive_star": 0,
            "reactive_run": 0,
            "step": self.get_values()["Step"]
        }

    def _setup_parameters(self, input_dict):
        if "Potencia" in input_dict:
            self.panel.ui.potencia_entry.setText(str(input_dict["Potencia"]))
        if "FP" in input_dict:
            self.panel.ui.fp_entry.setText(str(input_dict["FP"]))
        if "Fases" in input_dict:
            self.panel.ui.fases_combo.setCurrentText(str(input_dict["Fases"]))

        self.ui.cantidad_input.setText(str(input_dict["Cantidad"]))
        self.ui.step_combo.setCurrentText(str(input_dict["Step"]))
        self.ui.lineEdit.setText(str(input_dict["Factor_simultaneidad"]))

    def get_step(self):
        return self.get_values()["Step"]

    def get_description(self) -> dict:
        return {
            "step": self.get_values()["Step"],
            "Description": f"{self.get_values()['Cantidad']} Resistencia de {self.get_values()['Potencia']} kVA de {self.get_values()['Fases']} fases",
            "starting type": "Directo",
            "kW": self.get_apparent_power()['power_run'],
            "kVA": self.get_apparent_power()['power_run'],
            "kW_start": "--",
            "kVA_start": "--",
            "Volt_dip": "--"
        }

    def get_data_for_package(self):
        return {
            "type": "ResistanceCardListElement",
            "data": self.get_values()
        }


# Carga adaptada
class NonLinealCardListElement(AbstractCardListElement):

    def __init__(self, parent, initial_values=None):
        self.panel = DataNonLinealLoads(self)
        super().__init__(parent, self.panel, initial_values=initial_values)

    def get_step(self):
        return self.get_values()["Step"]

    def get_description(self) -> dict:
        return {
            "step": self.get_values()["Step"],
            "Description": f"{self.get_values()['Cantidad']} {self.get_values()['Equipo']} de {self.get_values()['Potencia']} {self.get_values()['Unidad']}",
            "starting type": "Directo",
            "kW": self.get_apparent_power()['power_run'],
            "kVA": abs(cmath.sqrt(
                self.get_apparent_power()['power_run'] ** 2 + self.get_apparent_power()['reactive_run'] ** 2)),
            "kW_start": "--",
            "kVA_start": "--",
            "Volt_dip": "--"
        }

    def get_apparent_power(self) -> dict:
        potencia = self.get_values()["Potencia"]
        cantidad = self.get_values()["Cantidad"]
        unidad = self.get_values()["Unidad"]
        factor_power = self.get_values()["FP"]
        efi = self.get_values()["Eficiencia"]

        if unidad == "kVA":
            power = potencia * cantidad * self.get_values()["Factor_simultaneidad"] / efi
        else:
            power = (potencia / (factor_power * efi)) * cantidad * self.get_values()["Factor_simultaneidad"]

        return {
            "power_star": power * factor_power,
            "reactive_star": abs(cmath.sqrt(power ** 2 - (power * factor_power) ** 2)),
            "power_run": power * factor_power,
            "reactive_run": abs(cmath.sqrt(power ** 2 - (power * factor_power) ** 2)),
            "step": self.get_values()["Step"]
        }

    def get_data_for_package(self):
        return {
            "type": "NonLinealCardListElement",
            "data": self.get_values()
        }

    def _setup_parameters(self, input_dict):
        if "Potencia" in input_dict:
            self.panel.ui.potencia_entry.setText(str(input_dict["Potencia"]))
        if "Unidad" in input_dict:
            self.panel.ui.unidad_potencia_combo.setCurrentText(str(input_dict["Unidad"]))
        if "Pulsos" in input_dict:
            self.panel.ui.pulsos_combo.setCurrentText(str(input_dict["Pulsos"]))
        if "Equipo" in input_dict:
            self.panel.ui.comboBox.setCurrentText(str(input_dict["Equipo"]))
        if "FP" in input_dict:
            self.panel.ui.fp_non_lineal.setText(str(input_dict["FP"]))
        if "Eficiencia" in input_dict:
            self.panel.ui.eficiencia_non_lineal.setText(str(input_dict["Eficiencia"] * 100))

        self.ui.cantidad_input.setText(str(input_dict["Cantidad"]))
        self.ui.step_combo.setCurrentText(str(input_dict["Step"]))
        self.ui.lineEdit.setText(str(input_dict["Factor_simultaneidad"]))


# Carga adaptada
class LinearLoadCardListElement(AbstractCardListElement):

    def __init__(self, parent, initial_values=None, fases=3):
        self.panel = DataLinealLoads(self)
        super().__init__(parent, self.panel, initial_values=initial_values)
        if fases == 1:
            self.panel.ui.fases_combo.setCurrentText("1")
            self.panel.ui.fases_combo.setEnabled(False)

    def get_step(self):
        return self.get_values()["Step"]

    def get_description(self) -> dict:
        return {
            "step": self.get_values()["Step"],
            "Description": f"{self.get_values()['Cantidad']} Carga estática de  {self.get_values()['Potencia']} KVA de {self.get_values()['Fases']} fases",
            "starting type": "Directo",
            "kW": self.get_apparent_power()['power_run'],
            "kVA": abs(cmath.sqrt(
                self.get_apparent_power()['power_run'] ** 2 + self.get_apparent_power()['reactive_run'] ** 2)),
            "kW_start": "--",
            "kVA_start": "--",
            "Volt_dip": "--"
        }

    def get_apparent_power(self) -> dict:
        power = self.get_values()["Potencia"] * self.get_values()["Factor_simultaneidad"]
        fp = self.get_values()["FP"]
        cantidad = self.get_values()["Cantidad"]

        # Considera si la carga es inductiva o capacitiva
        if self.get_values()["FP_I_C"] == "Inductivo":
            fp_performance = 1
        else:
            fp_performance = -1

        return {
            "power_star": power * cantidad * fp,
            "reactive_star": abs(cmath.sqrt((power * cantidad) ** 2 - (power * cantidad * fp) ** 2)) * fp_performance,
            "power_run": power * cantidad * fp,
            "reactive_run": abs(cmath.sqrt((power * cantidad) ** 2 - (power * cantidad * fp) ** 2)) * fp_performance,
            "step": self.get_values()["Step"]
        }

    def get_data_for_package(self):
        return {
            "type": "LinearLoadCardListElement",
            "data": self.get_values()
        }

    def _setup_parameters(self, input_dict):
        if "Potencia" in input_dict:
            self.panel.ui.potencia_entry.setText(str(input_dict["Potencia"]))
        if "FP" in input_dict:
            self.panel.ui.fp_entry.setText(str(input_dict["FP"]))
        if "Fases" in input_dict:
            self.panel.ui.fases_combo.setCurrentText(str(input_dict["Fases"]))
        if "FP_I_C" in input_dict:
            self.panel.ui.fp_ad_atr.setCurrentText(str(input_dict["FP_I_C"]))

        self.ui.cantidad_input.setText(str(input_dict["Cantidad"]))
        self.ui.step_combo.setCurrentText(str(input_dict["Step"]))
        self.ui.lineEdit.setText(str(input_dict["Factor_simultaneidad"]))


class AirCardListElement(AbstractCardListElement):

    def __init__(self, parent, voltaje, initial_values=None, fases=3):
        self.panel = DataAir(self)
        self.voltaje = voltaje
        super().__init__(parent, self.panel, initial_values=initial_values)
        if fases == 1:
            self.panel.ui.comboBox.setCurrentText("1")
            self.panel.ui.comboBox.setEnabled(False)
        self.codigo = {
            "A": 1.57,
            "B": 3.35,
            "C": 3.77,
            "D": 4.25,
            "E": 4.75,
            "F": 5.30,
            "G": 5.95,
            "H": 6.70,
            "J": 7.55,
            "K": 8.50,
            "L": 9.50,
            "M": 10.60,
            "N": 11.85,
            "P": 13.25,
            "R": 15,
            "S": 17,
            "T": 19,
            "U": 21.20,
            "V": 23
        }


    def get_step(self):
        return self.get_values()["Step"]

    def get_description(self) -> dict:
        return {
            "step": self.get_values()["Step"],
            "Description": f"{self.get_values()['Cantidad']} Aire acondicionado de {self.get_values()['Potencia']} {self.get_values()['Unidad']} de {self.get_values()['Fases']} fases",
            "starting type": self.get_values()["Metodo_arranque"],
            "kW": self.get_apparent_power()['power_run'],
            "kVA": abs(cmath.sqrt(
                self.get_apparent_power()['power_run'] ** 2 + self.get_apparent_power()['reactive_run'] ** 2)),
            "kW_start": self.get_apparent_power()['power_star'],
            "kVA_start": abs(cmath.sqrt(
                self.get_apparent_power()['power_star'] ** 2 + self.get_apparent_power()['reactive_star'] ** 2)),
            "Volt_dip": "--"
        }

    def get_apparent_power(self) -> dict:
        power = self.get_values()["Potencia"]
        unidad = self.get_values()["Unidad"]
        metodo = self.get_values()["Metodo_arranque"]
        tipo = self.get_values()["Tipo"]
        cantidad = self.get_values()["Cantidad"]
        lra = 1
        fase = self.get_values()["Fases"]
        Voltaje = self.voltaje
        fp_arr = 0.2

        if tipo == "LRA":
            lra = self.get_values()["LRA"]

        if not self.get_values()["Avanzado"]:
            letra = "G"
            fp = 0.9
            eficiencia = 9.7
            efi = 0.95

        else:
            fp = self.get_values()["FP"]
            eficiencia = self.get_values()["EER"]
            efi = self.get_values()["Eficiencia"]
            fp_arr = self.get_values()["FP_A"]

            if tipo == "NEMA":
                letra = self.get_values()["Letra"]

        if unidad == "Ton":
            Aux_p = (power * 12000) / (eficiencia * 1000)
        elif unidad == "BTU":
            Aux_p = (power / (eficiencia * 1000))
        else:
            if fase == 1:
                Aux_p = (Voltaje * power * fp) / 1000
            else:
                Aux_p = abs((cmath.sqrt(3) * Voltaje * fp * power) / 1000)

        if metodo == "Directo":
            f_l = 1
        elif metodo == "Estrella - Delta":
            f_l = 1 / 3
        else:
            f_l = 0.40

        power = Aux_p * self.get_values()["Factor_simultaneidad"] * cantidad / fp

        if tipo == "NEMA":
            power_ar = ((((Aux_p * efi)/ 0.746) * self.codigo[letra]) * f_l * cantidad)

        else:
            power_ar = (Aux_p / fp) * lra * f_l * cantidad

        return {
            "power_star": power_ar * fp_arr,
            "reactive_star": abs(cmath.sqrt((power_ar) ** 2 - (power_ar * fp_arr) ** 2)),
            "power_run": power * fp,
            "reactive_run": abs(cmath.sqrt((power) ** 2 - (power * fp) ** 2)),
            "step": self.get_values()["Step"]
        }

    def get_data_for_package(self):
        return {
            "type": "AirCardListElement",
            "data": self.get_values()
        }

    def _setup_parameters(self, input_dict):
        if "Potencia" in input_dict:
            self.panel.ui.potencia_entry.setText(str(input_dict["Potencia"]))
        if "FP" in input_dict:
            self.panel.ui.fp_air.setText(str(input_dict["FP"]))
        if "Fases" in input_dict:
            self.panel.ui.comboBox.setCurrentText(str(input_dict["Fases"]))
        if "FP_A" in input_dict:
            self.panel.ui.fp_arr_air.setText(str(input_dict["FP_A"]))
        if "Unidad" in input_dict:
            self.panel.ui.unidad_aa.setCurrentText(str(input_dict["Unidad"]))
        if "Metodo_arranque" in input_dict:
            self.panel.ui.tipo_arranque.setCurrentText(str(input_dict["Metodo_arranque"]))
        if "Tipo" in input_dict:
            self.panel.ui.tipo_norma.setCurrentText(str(input_dict["Tipo"]))
        if "Avanzado" in input_dict:
            if input_dict["Avanzado"]:
                self.panel.ui.checkBox.setChecked(True)
            else:
                self.panel.ui.checkBox.setChecked(False)
        if "EER" in input_dict:
            self.panel.ui.eer_air.setText(str(input_dict["EER"]))
        if "LRA" in input_dict:
            self.panel.ui.lra_entry.setText(str(input_dict["LRA"]))
        if "Letra" in input_dict:
            self.panel.ui.letra_aire_combo.setCurrentText(str(input_dict["Letra"]))
        if "Eficiencia" in input_dict:
            self.panel.ui.eficiencia_real_aire.setText(str(input_dict["Eficiencia"]))

        self.ui.cantidad_input.setText(str(input_dict["Cantidad"]))
        self.ui.step_combo.setCurrentText(str(input_dict["Step"]))
        self.ui.lineEdit.setText(str(input_dict["Factor_simultaneidad"]))


class AbstractDataPanel(QtWidgets.QWidget):
    signal_error = QtCore.pyqtSignal(str)
    is_correct = False

    CORRECT_LINE_EDIT_CONTENT_STYLES = "QLineEdit {\nborder: 1px solid #C0C0C0;\nborder-radius: 4px;\npadding: 2px;\n}\n" \
                                       "QLineEdit:hover, QLineEdit:focus {\nborder: 2px solid #0078D7;\nborder-radius: 4px;\n}\n"
    INCORRECT_LINE_EDIT_CONTENT_STYLES = "QLineEdit {\nborder: 1px solid #F82727;\nborder-radius: 4px;\npadding: 2px;\n}\n" \
                                         "QLineEdit:hover, QLineEdit:focus {\nborder: 2px solid #0078D7;\nborder-radius: 4px;\n}\n"

    def __init__(self, parent: AbstractCardListElement, ui_setup):
        super().__init__()
        if not isinstance(parent, AbstractCardListElement):
            raise ValueError("El parent de un AbstractDataPanel debe ser una instancia de AbstractCardListElement.")
        self.ui = ui_setup
        self.ui.setupUi(self)
        self.parent = parent
        self.leaveEvent = self._check_values

    def get_values(self) -> dict:
        pass

    def _check_values(self, event):
        line_edits = self.findChildren(QtWidgets.QLineEdit) + [self.parent.ui.cantidad_input]
        self.is_correct = True
        for line in line_edits:
            if line.parent().isVisible():
                if len(line.text()) == 0:
                    line.setStyleSheet(self.INCORRECT_LINE_EDIT_CONTENT_STYLES)
                    self.is_correct &= False
                else:
                    try:
                        if "." in line.text():
                            aux = float(line.text())
                        else:
                            aux = int(line.text())
                        line.setText(str(abs(aux)))
                        line.setStyleSheet(self.CORRECT_LINE_EDIT_CONTENT_STYLES)
                        self.is_correct &= True
                    except ValueError:
                        line.setStyleSheet(self.INCORRECT_LINE_EDIT_CONTENT_STYLES)
                        self.is_correct &= False

    def is_checked(self) -> bool:
        self._check_values(None)
        return self.is_correct


class DataLum(AbstractDataPanel):

    def __init__(self, parent):
        self.data = data_lum()
        super().__init__(parent, self.data)
        self.ui.fp_lum.setText("0.9")

    def get_values(self):
        return {
            "Potencia": float(self.ui.potencia_iluminacion.text()),
            "Unidad": self.ui.unidad_iluminacion.currentText(),
            "Tipo iluminacion": self.ui.tipo_iluminacion.currentText(),
            "FP": float(self.ui.fp_lum.text())
        }


class DataMotor(AbstractDataPanel):

    def __init__(self, parent):
        self.data = data_motor()
        super().__init__(parent, self.data)
        self.ui.frame_2.setVisible(False)
        self.ui.frame_3.setVisible(False)
        # Esconder opciones avanzadas
        self.ui.fp_container.setVisible(False)
        self.ui.eficiencia_container.setVisible(False)
        self.ui.fp_arranque_container.setVisible(False)
        self.ui.factor_carga_container.setVisible(False)

        self.ui.tipo_combo.currentIndexChanged.connect(self._combo_changed)
        self.ui.arranque_combo.currentIndexChanged.connect(self._arranque_changed)
        self.ui.checkBox.toggled.connect(self._advanced)

        # Datos avanzados por defecto
        self.ui.fp_motor.setText("0.8")
        self.ui.eficiencia_motor.setText("95")
        self.ui.fp_arranque_motor.setText("0.2")
        self.ui.factor_carga_motor.setText("100")

    def _combo_changed(self, i):
        if i == 0:
            self.ui.frame.setVisible(True)
            self.ui.frame_2.setVisible(False)
        else:
            self.ui.frame.setVisible(False)
            self.ui.frame_2.setVisible(True)

    def _advanced(self, event):
        if self.ui.checkBox.isChecked():
            self.ui.fp_container.setVisible(True)
            self.ui.eficiencia_container.setVisible(True)
            self.ui.fp_arranque_container.setVisible(True)
            self.ui.factor_carga_container.setVisible(True)
        else:
            self.ui.fp_container.setVisible(False)
            self.ui.eficiencia_container.setVisible(False)
            self.ui.fp_arranque_container.setVisible(False)
            self.ui.factor_carga_container.setVisible(False)

    def _arranque_changed(self, i):
        if i == 6:
            self.ui.frame_3.setVisible(True)
        else:
            self.ui.frame_3.setVisible(False)

    def get_values(self) -> dict:
        aux = {
            "Potencia": float(self.ui.potencia_entry.text()),
            "Unidad": self.ui.unidad_combo.currentText(),
            "Fases": int(self.ui.fases_combo.currentText()),
            "Metodo_arranque": self.ui.arranque_combo.currentText(),
            "Tipo": self.ui.tipo_combo.currentText(),
            "Avanzado": self.ui.checkBox.isChecked()
        }
        if aux["Tipo"] == "NEMA":
            aux = aux | {"Codigo": self.ui.comboBox.currentText()}
        if aux["Tipo"] == "IEC":
            aux = aux | {"Relacion": float(self.ui.lineEdit.text())}
        if aux["Metodo_arranque"] == "Variador de frecuencia":
            aux = aux | {"VFD": int(self.ui.comboBox_2.currentText())}
        if aux["Avanzado"]:
            aux = aux | {
                "factor_power": float(self.ui.fp_motor.text()),
                "eficiencia": float(self.ui.eficiencia_motor.text()) / 100,
                "factor_arr": float(self.ui.fp_arranque_motor.text()),
                "factor_carga": float(self.ui.factor_carga_motor.text()) / 100
            }

        return aux


class DataResistor(AbstractDataPanel):

    def __init__(self, parent):
        self.data = data_resistor()
        super().__init__(parent, self.data)
        self.ui.fp_entry.setEnabled(False)
        self.ui.fp_ad_atr.setEnabled(False)
        self.ui.fp_entry.setText("1")

    def get_values(self) -> dict:
        return {
            "Potencia": float(self.ui.potencia_entry.text()),
            "Fases": int(self.ui.fases_combo.currentText()),
            "FP": float(self.ui.fp_entry.text())
        }


class DataLinealLoads(AbstractDataPanel):

    def __init__(self, parent):
        self.data = data_resistor()
        super().__init__(parent, self.data)

    def get_values(self) -> dict:
        return {
            "Potencia": float(self.ui.potencia_entry.text()),
            "Fases": int(self.ui.fases_combo.currentText()),
            "FP": float(self.ui.fp_entry.text()),
            "FP_I_C": self.ui.fp_ad_atr.currentText()
        }


class DataNonLinealLoads(AbstractDataPanel):

    def __init__(self, parent):
        self.data = data_nonlineal()
        super().__init__(parent, self.data)
        self.ui.fp_non_lineal.setText("0.95")
        self.ui.eficiencia_non_lineal.setText("100")

    def get_values(self) -> dict:
        return {
            "Potencia": float(self.ui.potencia_entry.text()),
            "Unidad": self.ui.unidad_potencia_combo.currentText(),
            "Pulsos": int(self.ui.pulsos_combo.currentText()),
            "Equipo": self.ui.comboBox.currentText(),
            "FP": float(self.ui.fp_non_lineal.text()),
            "Eficiencia": float(self.ui.eficiencia_non_lineal.text()) / 100
        }


class DataAir(AbstractDataPanel):

    def __init__(self, parent):
        self.data = data_air()
        super().__init__(parent, self.data)
        self.ui.content_tipo_4.setVisible(False)
        self.ui.label_3.setVisible(False)

        self.ui.frame_3.setVisible(False)
        self.ui.content_eficiencia.setVisible(False)
        self.ui.frame_5.setVisible(False)
        self.ui.frame_8.setVisible(False)

        self.ui.eer_air.setText("9.7")
        self.ui.fp_air.setText("0.9")
        self.ui.fp_arr_air.setText("0.5")
        self.ui.eficiencia_real_aire.setText("95")

        if self.ui.tipo_norma.currentIndex() == 0:
            self.ui.frame_4.setVisible(True)
        else:
            self.ui.frame_4.setVisible(False)
        self.ui.checkBox.toggled.connect(self._advanced_selected)
        self.ui.tipo_norma.currentIndexChanged.connect(self._tipo_arranque)

    def _advanced_selected(self, event):
        if self.ui.checkBox.isChecked():
            self.ui.content_eficiencia.setVisible(True)
            self.ui.frame_5.setVisible(True)
            self.ui.frame_3.setVisible(True)
            self.ui.frame_8.setVisible(True)
        else:
            self.ui.content_eficiencia.setVisible(False)
            self.ui.frame_5.setVisible(False)
            self.ui.frame_3.setVisible(False)
            self.ui.frame_8.setVisible(False)

    def _tipo_arranque(self, i):
        if i == 1:
            self.ui.content_tipo_4.setVisible(True)
            self.ui.label_3.setVisible(True)
        else:
            self.ui.content_tipo_4.setVisible(False)
            self.ui.label_3.setVisible(False)

        if i == 0:
            self.ui.frame_4.setVisible(True)
        else:
            self.ui.frame_4.setVisible(False)

    def get_values(self) -> dict:
        aux = {
            "Potencia": float(self.ui.potencia_entry.text()),
            "Unidad": self.ui.unidad_aa.currentText(),
            "Metodo_arranque": self.ui.tipo_arranque.currentText(),
            "Tipo": self.ui.tipo_norma.currentText(),
            "Avanzado": self.ui.checkBox.isChecked(),
            "Fases": int(self.ui.comboBox.currentText())
        }

        if aux["Tipo"] == "LRA":
            aux |= {"LRA": float(self.ui.lra_entry.text())}
        if aux["Avanzado"] and aux["Tipo"] == "NEMA":
            aux |= {
                "Letra": self.ui.letra_aire_combo.currentText()
            }
        if aux["Avanzado"]:
            aux |= {
                "Eficiencia": float(self.ui.eficiencia_real_aire.text()) / 100,
                "EER": float(self.ui.eer_air.text()),
                "FP": float(self.ui.fp_air.text()),
                "FP_A": float(self.ui.fp_arr_air.text())
            }

        return aux


if __name__ == '__main__':
    app = QApplication(sys.argv)
    data = DataLum(None)
    print(pickle.dumps(data))
    sys.exit(app.exec_())
