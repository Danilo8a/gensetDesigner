import sys
import os
import time
import winsound
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import QIcon

from GUIRegister import GUIRegister
from GUIXMLManager import GUIXMLManager
from skin_splash import *
from gui_elements import GUIBaseDialog
from gui_main import GUIMain


class GUILauncher(QtWidgets.QMainWindow):

    # Falta definir los parámetros del launcher
    def __init__(self, file_to_open=None):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowIcon(QIcon(r'./img/logo_4.png'))

        self.low_bar = self.ui.low_dir_bar
        self.high_bar = self.ui.high_dir_bar
        self.mess = self.ui.splash_infor_mess
        self.dialog = GUIBaseDialog(self, GUIBaseDialog.SET_ICON_DIALOG_ERROR)
        self.gui_main = None

        self.low_bar.setValue(0)
        self.low_bar.setMaximum(100)
        self.high_bar.setValue(0)
        self.high_bar.setMaximum(100)
        self.mess.setText("")

        if not os.path.exists("./config.xml"):
            self._error_mess("El archivo config.xml es indispensable para el funcionamiento de la aplicación y parece "
                             "que ha sido eliminado. Reinstale el programa para resolver el problema.")
            sys.exit()

        if not os.path.exists("./gensets.db.db"):
            self._error_mess("La base de datos del sistema no se encuentra disponible en el archivo raíz. Reinstale "
                             "el programa para corregir el error.")
            sys.exit()
        # Archivo xml con la configuración del sistema
        self.config_xml = GUIXMLManager("./config.xml")
        executions = int(self.config_xml.get_value_attrib_in_tag("user-data", "value", type_content="executions")[0])

        if executions == 0:
            pass

        executions += 1
        self.config_xml.insert_attrib_value('user-data', 'executions', 'value', str(executions))

        self.file_to_open = file_to_open

        self.thread = Launcher(self.config_xml)
        self.register_window = GUIRegister(self.config_xml)

        self.thread.signal_low_bar.connect(self._update_low_bar)
        self.thread.dialog_error.connect(self._error_mess)
        self.thread.signal_upper_bar.connect(self._update_up_bar)
        self.thread.message.connect(self._set_text)
        self.thread.launch_app_signal.connect(self._end_launcher)
        self.thread.launch_register.connect(self._register_window)
        self.register_window.registered_signal.connect(self._end_launcher)
        self.thread.start()

    def _register_window(self, xml: GUIXMLManager):
        self.setVisible(False)
        self.register_window.show()

    def _end_launcher(self):
        self.close()
        self.gui_main = GUIMain(self.config_xml, file_to_open=self.file_to_open)
        self.gui_main.show()
        return self.gui_main

    def _update_low_bar(self, i: int):
        if 0 <= i <= 100:
            self.low_bar.setValue(i)
        else:
            self.low_bar.setValue(0)

    def _update_up_bar(self, i: int):
        if 0 <= i <= 100:
            self.high_bar.setValue(i)
        else:
            self.high_bar.setValue(0)

    def _set_text(self, mess: str):
        self.mess.setText(mess)

    def _error_mess(self, mess: str):
        self.dialog.setDialogMessTitle("Error fatal al comprobar archivos raíz.")
        self.dialog.setDialogMessInformation(mess)
        winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
        self.dialog.exec()
        sys.exit()


def listed_files_in_dir(path):
    with open("res.txt", "w", encoding="utf-8") as f:
        if os.path.isdir(path):
            for f_name in os.listdir(path):
                f.write(f'<resource name="{f_name}"/>\n')


class Launcher(QThread):
    signal_low_bar = QtCore.pyqtSignal(int)
    signal_upper_bar = QtCore.pyqtSignal(int)
    dialog_error = QtCore.pyqtSignal(str)
    message = QtCore.pyqtSignal(str)
    launch_app_signal = QtCore.pyqtSignal(bool)
    launch_register = QtCore.pyqtSignal(GUIXMLManager)

    len_img = 0
    len_plugins = 0
    len_projects = 0

    _list_roots = [
        "./img",
        "./config.xml"
    ]

    def __init__(self, xml: GUIXMLManager):
        super().__init__()
        self._xml = xml

    def run(self):
        # Comprueba el arbol de archivos
        if self._check_root_dir():
            return
        self._reset_gui_elements(25)

        # Comprueba que los recursos del sistema se encuentren y sean consistentes
        if not self._check_files(self._xml, "./img", "img", "name"):
            return
        self._reset_gui_elements(75)

        # Comprueba que los proyectos estén en los lugares indicados
        self._check_projects(self._xml, "projects", "name")
        self._reset_gui_elements(100)
        self.message.emit("Comprobación terminada!")

        if self._xml.get_root_attrib_value("user-data", "registered") == "false":
            self.launch_register.emit(self._xml)
            return
        else:
            self.launch_app_signal.emit(True)

    def _check_projects(self, file, tag, attr, type_content="resource"):

        in_file = file.get_value_attrib_in_tag(tag, attr, type_content=type_content)
        if len(in_file) > 0:
            step = int(100/len(in_file))
            to_emit = step
            for i in in_file:
                self.message.emit("Comprobando proyecto: " + i)
                to_emit += step
                self.signal_low_bar.emit(to_emit)
                time.sleep(0.1)
                if not os.path.isfile(i):
                    file.delete("projects", "resource", "name", i)
                    self.message.emit("Eliminando referencia al fichero: " + i)
                    time.sleep(0.1)

    def _check_files(self, file, path, tag, attr, type_content="resource"):

        if os.path.isdir(path):
            in_file = file.get_value_attrib_in_tag(tag, attr, type_content=type_content)
            in_dir = os.listdir(path)

            if len(in_file) > len(in_dir):
                self.dialog_error.emit(f"Faltan archivos en el directorio {path}. Reinstale el "
                                       "programa para corregir el error.")
                return False
            else:
                step = int(100/len(in_dir))
                for e_file in in_file:
                    self.message.emit("Comprobando el recurso: " + e_file)
                    if e_file in in_dir:
                        to_emit = (in_dir.index(e_file) + 1) * step
                        self.signal_low_bar.emit(to_emit)
                        time.sleep(0.1)
                    else:
                        self.dialog_error.emit(f"El archivo {e_file} no se encuentra en el directorio {path}. "
                                               f"Reinstale el programa para corregir el error.")
                        return False
            return in_dir

        elif not os.path.isdir(path):
            self.dialog_error.emit(f"El directorio {path} es incorrecto o ha sido corrompido. Reinstale el "
                                   "programa para corregir el error.")
            return False

    def _reset_gui_elements(self, emit_up_bar=None):

        self.signal_low_bar.emit(0)
        if emit_up_bar is not None:
            self.signal_upper_bar.emit(emit_up_bar)
        else:
            self.signal_upper_bar.emit(0)
        self.message.emit("")
        time.sleep(0.1)

    def _check_root_dir(self):
        step = int(100 / len(self._list_roots))

        for c_value in self._list_roots:

            self.message.emit("Comprobando el recurso: " + c_value)
            to_emit = (self._list_roots.index(c_value) + 1) * step

            if os.path.isdir(c_value) or os.path.isfile(c_value):
                self.signal_low_bar.emit(to_emit)
                time.sleep(0.3)
            else:
                self.dialog_error.emit(f"Error fatal comprobando el recurso: {c_value}. Reinstale el "
                                       "programa para corregir el error.")
                return True


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    aux_file = None
    if len(sys.argv) > 1 and os.path.exists(str(sys.argv[1])):
        aux_file = str(sys.argv[1])
    main = GUILauncher(file_to_open=aux_file)
    main.show()
    sys.exit(app.exec_())
