import sys
import time
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPixmap, QIcon

from GUIXMLManager import GUIXMLManager
from gui_elements import GUITemporalMessage
from skin_register import Ui_MainWindow


class GUIRegister(QtWidgets.QMainWindow):

    registered_signal = QtCore.pyqtSignal(bool)

    def __init__(self, xml: GUIXMLManager):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._xml = xml
        self._registered = False
        self.ui.button_acept.clicked.connect(self._continuar)
        self.ui.label.setText("")
        pixmap = QPixmap("img/logo_1.png")
        self.ui.label.setPixmap(pixmap)
        self.ui.label.setMinimumSize(QtCore.QSize(237, 65))
        self.ui.label.setMaximumSize(QtCore.QSize(237, 65))
        self.ui.label.setScaledContents(True)
        self.setWindowIcon(QIcon(r'./img/logo_4.png'))

    def _continuar(self):
        name = self.ui.name_edit.text()
        apellido = self.ui.apellido_edit.text()
        institucion = self.ui.institucion_edit.text()
        correo = self.ui.correo_edit.text()
        pais = self.ui.pais_edit.text()
        profesion = self.ui.profesion_edit.text()
        if len(name) == 0 or len(apellido) == 0 or len(institucion) == 0 or len(correo) == 0\
                or len(pais) == 0 or len(profesion) == 0:
            GUITemporalMessage(self, "Error al rellenar el formulario.", "Uno o más campos se encuentran vacíos.", 11,
                               position=GUITemporalMessage.POSITION_TC)
        else:
            self._xml.insert_attrib_value('user-data', 'first-name', 'value', name)
            self._xml.insert_attrib_value('user-data', 'last-name', 'value', apellido)
            self._xml.insert_attrib_value('user-data', 'institution', 'value', institucion)
            self._xml.insert_attrib_value('user-data', 'profession', 'value', profesion)
            self._xml.insert_attrib_value('user-data', 'email', 'value', correo)
            self._xml.insert_attrib_value('user-data', 'country', 'value', pais)
            self._xml.container_tag_change_attrib('user-data', 'registered', 'true')
            time.sleep(1)
            self.close()
            self.registered_signal.emit(True)

    def moveEvent(self, event):
        for temp in self.findChildren(GUITemporalMessage):
            temp.move(temp.x_init + self.pos().x(), temp.y_init + self.pos().y())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    my_register = GUIRegister(None)
    my_register.show()
    sys.exit(app.exec_())