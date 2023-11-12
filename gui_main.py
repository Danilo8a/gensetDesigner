import cmath
import datetime
import json
import math
import pickle
import sqlite3
import sys
import subprocess
from PyQt5.QtGui import QPixmap, QIcon

import gui_utils
from PIL import Image
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem
from gui_elements import ResistanceCardListElement, LinearLoadCardListElement, MotorCardListElement, \
    LumCardListElement, \
    AirCardListElement, AbstractCardListElement, GUITemporalMessage, GUILoadView, GUIDataSizing, GUIBaseDialog, \
    NonLinealCardListElement, GUIInputDBData, GUIProjectItem
from skin_lacca import *
import numpy as np
import matplotlib.patches as mpatches
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from syng import AbstractGen, CylindricalGen, SalientGen
from GUIXMLManager import GUIXMLManager
import os

plt.rcParams.update({'font.size': 7})


def _partial_run_power_v(dict, n):
    acum_p = 0
    acum_q = 0
    for i in range(1, n):
        acum_p += dict[i]['power_run']
        acum_q += dict[i]['reactive_run']
    return acum_p, acum_q


def _partial_run_power(dictionary, n):
    acum_s = 0
    for i in range(1, n):
        acum_s += math.sqrt(dictionary[i]['power_run'] ** 2 + dictionary[i]['reactive_run'] ** 2)
    return acum_s


# Esto genera un diccionario con los módulos de las potencias aparentes de arranque
def step_kvart(diccionario):
    resultados = {}
    for step, valores in diccionario.items():
        power_star = valores.get('power_star', 0)
        reactive_star = valores.get('reactive_star', 0)
        resultado = abs(cmath.sqrt(power_star ** 2 + reactive_star ** 2))
        resultados[step] = resultado
    return resultados


# Esto genera un diccionario con los módulos de las potencias aparentes de regimen permanente
def step_kvarp(diccionario):
    resultados = {}
    for step, valores in diccionario.items():
        power_run = valores.get('power_run', 0)
        reactive_run = valores.get('reactive_run', 0)
        resultado = abs(cmath.sqrt(power_run ** 2 + reactive_run ** 2))
        resultados[step] = resultado
    return resultados


# Esta función calcula la potencia de arranque de cada paso. Da como resultado un diccionario
def get_arranques(diccionario):
    valores = {}
    suma = 0
    for i in range(1, len(step_kvart(diccionario)) + 1):
        if i == 1:
            valores[i] = step_kvart(diccionario)[i]
        else:
            suma += step_kvarp(diccionario).get(i - 1)

            valores[i] = suma + step_kvart(diccionario)[i]
    return valores


def get_max_start(diccionario):
    start_for_output = 0
    aux_step = 0
    for key, value in diccionario.items():
        if diccionario[key]['arranque_paso'] > start_for_output:
            start_for_output = diccionario[key]['arranque_paso']
            aux_step = key
    return start_for_output, aux_step


class GUIMain(QtWidgets.QMainWindow):
    size = QtCore.pyqtSignal(tuple)

    def __init__(self, xml: GUIXMLManager, file_to_open=None):
        QtWidgets.QMainWindow.__init__(self)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.thread = None
        self.showMaximized()
        self.setWindowIcon(QIcon(r'./img/logo_4.png'))
        self.setWindowTitle("GenSet Designer - Designing energy")

        self._xml = xml
        self._user_name = xml.get_value_attrib_in_tag("user-data", "value", type_content="first-name")[0]
        self._last_name = xml.get_value_attrib_in_tag("user-data", "value", type_content="last-name")[0]
        self._user_institution = xml.get_value_attrib_in_tag("user-data", "value", type_content="institution")[0]
        self._last_curve_generated = xml.get_root_attrib_value("last-curve", "url")
        self.ui.ultima_curva_label.mousePressEvent = self._load_last_curve

        # Comprobación para la última máquina exportada
        self.ui.ultima_curva_label.setScaledContents(True)
        self._last_curve_act()

        self.ui.name_user.setText(self._user_name + " " + self._last_name)
        self.ui.institute_user.setText(self._user_institution)
        self.closeEvent = self.on_close

        # Acción de los botones principales
        self.ui.grafica.clicked.connect(self._go_curve)
        self.ui.polo_liso.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.datos_liso))
        self.ui.polo_saliente.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.datos_saliente))
        self.ui.regresar_select.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.home_2))
        self.ui.home.clicked.connect(self._go_home)
        self.ui.especificar.clicked.connect(lambda: self.sizing_window.show())
        self.ui.saliente_anterior_3.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.graficar_2))
        self.ui.liso_anterior.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.graficar_2))
        self.ui.anterior_graph.clicked.connect(self._anterior_graph)
        self.ui.exportar_graph.clicked.connect(self._screen_shot)
        self.ui.e_r_1_but.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.datos_liso))
        self.ui.toolButton_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.datos_saliente))
        self.ui.toolButton_3.clicked.connect(lambda: self.sizing_window.show())
        self.ui.anterior_select_loads.clicked.connect(self._previous_loads)
        self.ui.base.clicked.connect(self._go_db)
        self.ui.anterior_db.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.home_2))
        self.ui.pushButton.clicked.connect(self._report)
        self.ui.resultados_atras.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.dim_select_page))
        self.ui.toolButton_4.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.bd_visualizar))
        self.ui.guardar_proyecto_dim.clicked.connect(self._save_project)
        self.ui.toolButton.clicked.connect(lambda: subprocess.Popen('cmd /c start manual.pdf'))

        self.liso_pu = False
        self.saliente_pu = False
        self.ui.saliente_pu_check_3.toggled.connect(self.onClicked)
        self.ui.liso_pu_check.toggled.connect(self.onClicked)
        self.ui.saliente_graficar_3.clicked.connect(self._graficar_saliente)
        self.ui.liso_graficar.clicked.connect(self._graficar_lisos)

        # Área para dibujar
        self.w_canvas = self.ui.graph_container
        self.c_layout = self.ui.graph_layout_graph
        self.data_graph_layout = self.ui.graph_data_layout
        self.static_graph = None

        # Inicializa la interfaz en la pagina principal
        self.ui.stackedWidget.setCurrentWidget(self.ui.home_2)
        # Quita el cambio de voltaje para valores en PU
        self.ui.sal_v_nom_pu.setVisible(False)
        self.ui.liso_v_nom_pu.setVisible(False)

        self._update_projects()

        # Acción de los botones para agregar las cargas
        self.ui.list_motor.clicked.connect(self._add_motor)
        self.ui.lis_lum.clicked.connect(self._add_lum)
        self.ui.list_resistance.clicked.connect(self._add_resistance)
        self.ui.list_static_load.clicked.connect(self._add_lineal_load)
        self.ui.list_air_conditioning.clicked.connect(self._add_air)
        self.ui.list_non_linear_load.clicked.connect(self._add_non_lineal_load)
        self.ui.siguiente_select_loads.clicked.connect(self._siguiente_carga)

        # Cuadro de espera
        self._wait_panel = GUILoadView(self)
        self.size.connect(self._wait_panel.update_location)

        # Ventana para los datos del dimensionamiento
        self.sizing_window = GUIDataSizing(parent=self)
        self.sizing_window.data_for_emit.connect(self._data_for_sizing_is_here)

        self.my_data_for_dim = dict()

        # Rellenando la base de datos de la app
        self._actualizar()
        self.B = None
        self._last_fila = 0
        self.ui.eliminar_db.clicked.connect(self._eliminar)
        self.ui.agregar_db.clicked.connect(self._agregar)
        self.aux_gui_db = GUIInputDBData(self)
        self.aux_gui_db.end_signal.connect(self._actualizar)

        # variables para el reporte
        self.dict_desc = {}
        self.dict_kva_rp = {}
        self.dict_arranques = {}
        self.dict_vd = []
        self.maxvd = 0
        self.maxthd = 0
        self.porc_carga = 0
        self.kva_total_rp = 0
        self.kw_rp = {}
        self.kw_rt = {}
        self.my_machine = []

        # Detalles para las pantallas de la gráfica
        self.ui.label_11.setWordWrap(True)
        self.ui.label_11.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.ui.polo_liso.enterEvent = self._liso_enter
        self.ui.polo_liso.leaveEvent = self._liso_saliente_leave
        self.ui.polo_saliente.enterEvent = self._saliente_enter
        self.ui.polo_saliente.leaveEvent = self._liso_saliente_leave
        # Detalle para los datos de polos salientes
        self.ui.detalles_dalientes_texto.setWordWrap(True)
        self.ui.sal_l_1.enterEvent = self._potencia_text_saliente
        self.ui.sal_l_1.leaveEvent = self._leave_saliente

        self.ui.sal_l_2.enterEvent = self._factor_potencia_saliente
        self.ui.sal_l_2.leaveEvent = self._leave_saliente

        self.ui.sal_l_3.enterEvent = self._tension_campo_saliente
        self.ui.sal_l_3.leaveEvent = self._leave_saliente

        self.ui.sal_l_4.enterEvent = self._porcentaje_estabilidad_saliente
        self.ui.sal_l_4.leaveEvent = self._leave_saliente

        self.ui.sal_r_1.enterEvent = self._voltaje_nominal_saliente
        self.ui.sal_r_1.leaveEvent = self._leave_saliente

        self.ui.sal_r_2.enterEvent = self._reactancia_directa_saliente
        self.ui.sal_r_2.leaveEvent = self._leave_saliente

        self.ui.sal_r_3.enterEvent = self._reactancia_cuadratura_saliente
        self.ui.sal_r_3.leaveEvent = self._leave_saliente

        self.ui.sal_r_4.enterEvent = self._potencia_potriz_maxima_saliente
        self.ui.sal_r_4.leaveEvent = self._leave_saliente

        self.ui.sal_r_5.enterEvent = self._porcentaje_seguridad_saliente
        self.ui.sal_r_5.leaveEvent = self._leave_saliente

        # Detalles para los datos de polos lisos
        self.ui.detalles_liso_label.setWordWrap(True)
        self.ui.left_1.enterEvent = self._potencia_liso
        self.ui.left_1.leaveEvent = self._leave_liso

        self.ui.left_2.enterEvent = self._factor_potencia_liso
        self.ui.left_2.leaveEvent = self._leave_liso

        self.ui.left_3.enterEvent = self._tension_campo_liso
        self.ui.left_3.leaveEvent = self._leave_liso

        self.ui.left_4.enterEvent = self._porcentaje_estabilidad_liso
        self.ui.left_4.leaveEvent = self._leave_liso

        self.ui.right_1.enterEvent = self._voltaje_nominal_liso
        self.ui.right_1.leaveEvent = self._leave_liso

        self.ui.right_2.enterEvent = self._reactancia_sincrona_liso
        self.ui.right_2.leaveEvent = self._leave_liso

        self.ui.right_3.enterEvent = self._potencia_potriz_maxima_liso
        self.ui.right_3.leaveEvent = self._leave_liso

        self.ui.right_4.enterEvent = self._porcentaje_seguridad_liso
        self.ui.right_4.leaveEvent = self._leave_liso

        if file_to_open is not None:
            self._file_path = file_to_open
            self._open_project(file_to_open)

    def on_close(self, event):
        aux_dialog = GUIBaseDialog(None, GUIBaseDialog.SET_ICON_DIALOG_INFORMATION)
        aux_dialog.setDialogMessTitle("¿Está seguro que desea salir?")
        aux_dialog.setDialogMessInformation(
            "Si presiona ok, la aplicación se cerrará."
        )
        if aux_dialog.exec():
            event.accept()
        else:
            event.ignore()

    def _liso_enter(self, event):
        self.ui.label_11.setText("Una máquina síncrona de polos lisos es un tipo "
                                 "de máquina eléctrica rotativa de corriente "
                                 "alterna cuya velocidad de rotación está "
                                 "sincronizada con la frecuencia de la corriente "
                                 "alterna que la alimenta. El rotor de la "
                                 "máquina tiene un conjunto de polos magnéticos "
                                 "que son uniformes en forma y tamaño. El "
                                 "estator tiene un devanado trifásico que genera "
                                 "un campo magnético giratorio. Cuando el rotor "
                                 "y el estator están en sincronismo, "
                                 "las corrientes inducidas en el estator "
                                 "producen un par que hace girar el rotor a la "
                                 "misma velocidad.")

    def _liso_saliente_leave(self, event):
        self.ui.label_11.setText("")

    def _saliente_enter(self, event):
        self.ui.label_11.setText("Una máquina síncrona de polos salientes es "
                                 "un tipo de máquina síncrona en la que el "
                                 "rotor tiene una serie de salientes o "
                                 "protuberancias que sobresalen del cuerpo "
                                 "principal. Estas salientes tienen un "
                                 "efecto en el flujo magnético del rotor, "
                                 "que se distribuye de manera más uniforme "
                                 "en el entrehierro.")

    # Detalles para los datos de polos salientes
    def _potencia_text_saliente(self, event):
        self.ui.detalles_dalientes_texto.setText("Producto de la tensión eléctrica eficaz aplicada por la corriente "
                                                 "eléctrica eficaz que circula por un generador eléctrico. También se "
                                                 "considera como la suma vectorial de la Potencia Activa más la "
                                                 "Potencia Reactiva. En p.u. su valor es 1.")

    def _factor_potencia_saliente(self, event):
        self.ui.detalles_dalientes_texto.setText("Relación que existe entre el vector corriente y el vector tensión "
                                                 "que representan la potencia activa y potencia reactiva, "
                                                 "respectivamente. Este se representa mediante el coseno del ángulo "
                                                 "φ, que es el ángulo entre las formas de onda de la tensión y la "
                                                 "corriente.")

    def _tension_campo_saliente(self, event):
        self.ui.detalles_dalientes_texto.setText("Máxima tensión inducida en el devanado estatórico del generador "
                                                 "síncrono, debido a la máxima corriente de campo que circula por el "
                                                 "devanado rotórico.")

    def _porcentaje_estabilidad_saliente(self, event):
        self.ui.detalles_dalientes_texto.setText("Valor porcentual que permite mantener un ángulo de potencia menor a "
                                                 "90° para evitar inestabilidades en el funcionamiento del generador.")

    def _voltaje_nominal_saliente(self, event):
        self.ui.detalles_dalientes_texto.setText("Es el voltaje que el generador está diseñado para generar a plena "
                                                 "carga y a la frecuencia nominal. En p.u. su valor es 1")

    def _reactancia_directa_saliente(self, event):
        self.ui.detalles_dalientes_texto.setText("Es la medida de oposición que ofrece una máquina síncrona al flujo "
                                                 "magnético del eje directo. El eje directo es la dirección por la "
                                                 "que se orienta el flujo producido por el devanado de campo.")

    def _reactancia_cuadratura_saliente(self, event):
        self.ui.detalles_dalientes_texto.setText("Es la medida de oposición que ofrece una máquina síncrona al flujo "
                                                 "magnético del eje de cuadratura. El eje de cuadratura es el eje "
                                                 "perpendicular al campo magnético del rotor y se encuentra "
                                                 "distribuido en un área más grande que el flujo magnético en el "
                                                 "eje directo.")

    def _potencia_potriz_maxima_saliente(self, event):
        self.ui.detalles_dalientes_texto.setText("Es la máxima potencia que puede proporcionar el primo motor del "
                                                 "grupo electrógeno al momento de hacer girar el rotor de la máquina "
                                                 "síncrona.")

    def _porcentaje_seguridad_saliente(self, event):
        self.ui.detalles_dalientes_texto.setText("Valor porcentual que permite mantener a la corriente de excitación "
                                                 "por encima de la mínima corriente de excitación para que la máquina "
                                                 "funcione de forma segura y estable.")

    # Detalles para los datos de polos salientes
    def _potencia_liso(self, event):
        self.ui.detalles_liso_label.setText(
                "Producto de la tensión eléctrica eficaz aplicada por la corriente "
                "eléctrica eficaz que circula por un generador eléctrico. También se "
                "considera como la suma vectorial de la Potencia Activa más la "
                "Potencia Reactiva. En p.u. su valor es 1.")

    def _factor_potencia_liso(self, event):
        self.ui.detalles_liso_label.setText(
                "Relación que existe entre el vector corriente y el vector tensión "
                "que representan la potencia activa y potencia reactiva, "
                "respectivamente. Este se representa mediante el coseno del ángulo "
                "φ, que es el ángulo entre las formas de onda de la tensión y la "
                "corriente.")

    def _tension_campo_liso(self, event):
        self.ui.detalles_liso_label.setText("Máxima tensión inducida en el devanado estatórico del generador "
                                                     "síncrono, debido a la máxima corriente de campo que circula por el "
                                                     "devanado rotórico.")

    def _porcentaje_estabilidad_liso(self, event):
        self.ui.detalles_liso_label.setText(
                "Valor porcentual que permite mantener un ángulo de potencia menor a "
                "90° para evitar inestabilidades en el funcionamiento del generador.")

    def _voltaje_nominal_liso(self, event):
        self.ui.detalles_liso_label.setText(
                "Es el voltaje que el generador está diseñado para generar a plena "
                "carga y a la frecuencia nominal. En p.u. su valor es 1")

    def _reactancia_sincrona_liso(self, event):
        self.ui.detalles_liso_label.setText(
                "Es la medida de oposición que ofrece una máquina síncrona al flujo "
                "magnético producido por el devanado de campo.")

    def _potencia_potriz_maxima_liso(self, event):
        self.ui.detalles_liso_label.setText("Es la máxima potencia que puede proporcionar el primo motor del "
                                                     "grupo electrógeno al momento de hacer girar el rotor de la máquina "
                                                     "síncrona.")

    def _porcentaje_seguridad_liso(self, event):
        self.ui.detalles_liso_label.setText(
                "Valor porcentual que permite mantener a la corriente de excitación "
                "por encima de la mínima corriente de excitación para que la máquina "
                "funcione de forma segura y estable.")

    def _leave_liso(self, event):
        self.ui.detalles_liso_label.setText("")

    def _leave_saliente(self, event):
        self.ui.detalles_dalientes_texto.setText("")

    def _go_home(self):
        if self._check_for_exit():
            self.ui.stackedWidget.setCurrentWidget(self.ui.home_2)

    def _go_curve(self):
        if self._check_for_exit():
            self.ui.stackedWidget.setCurrentWidget(self.ui.graficar_2)

    def _go_db(self):
        if self._check_for_exit():
            self.ui.stackedWidget.setCurrentWidget(self.ui.bd_visualizar)

    def _check_for_exit(self):
        aux_dialog = GUIBaseDialog(None, GUIBaseDialog.SET_ICON_DIALOG_INFORMATION)
        # Condición para salir de la ventana del perfil de carga
        if self.ui.stackedWidget.currentWidget() is self.ui.dim_select_page and len(
                self.ui.list_selected.findChildren(AbstractCardListElement)) > 0:
            aux_dialog.setDialogMessTitle("¿Está seguro que desea descartar los cambios?")
            aux_dialog.setDialogMessInformation(
                "Si presiona aceptar, todos los cambios realizados en el proyecto se perderán."
            )
            if aux_dialog.exec():
                self._clear_select_loads_page()
                return True
            else:
                return False
        # Condición para salir de la página de resultados
        elif self.ui.stackedWidget.currentWidget() is self.ui.resultados_dim:
            aux_dialog.setDialogMessTitle("¿Está seguro que desea salir?")
            aux_dialog.setDialogMessInformation(
                "Si presiona aceptar, saldrá de la visualización de resultados. Asegúrese de guardar el proyecto."
            )
            if aux_dialog.exec():
                self._clear_select_loads_page()
                return True
            else:
                return False
        elif self.ui.stackedWidget.currentWidget() is self.ui.visualizar:
            aux_dialog.setDialogMessTitle("¿Está seguro que desea salir?")
            aux_dialog.setDialogMessInformation(
                "Asegúrese de exportar el gráfico antes de salir de la visualización de la carta de operación."
            )
            if aux_dialog.exec():
                return True
            else:
                return False
        else:
            return True

    def _clear_select_loads_page(self):
        for child in self.ui.list_selected.findChildren(AbstractCardListElement):
            child.deleteLater()
        self.ui.nombre_proyecto.setText("")
        self.ui.voltaje_proyecto.setText("")
        self.ui.fases_proyecto.setText("")
        self.ui.frecuencia_proyecto.setText("")
        self.ui.altura_proyecto.setText("")
        self.ui.temperatura_proyecto.setText("")
        self.ui.tiempo_servicio_proyecto.setText("")
        self.ui.reserva_proyecto.setText("")
        self.ui.voltaje_dip_proyecto.setText("")
        self.ui.combustibl_proyecto.setText("")
        self.ui.ciclo_proyecto.setText("")
        self.ui.iso_proyecto.setText("")

    def _previous_loads(self):
        if self._check_for_exit():
            self.ui.stackedWidget.setCurrentWidget(self.ui.home_2)

    @gui_utils.secure_execution
    def _update_projects(self):
        # Elimina todos los proyectos en la lista
        for child in self.ui.container_proyectos_elements.findChildren(GUIProjectItem):
            child.deleteLater()

        # Obtiene la lista con los proyectos apuntados en el xml
        list_projects = self._xml.get_list_elements_in_container("projects", "project")
        # Ordena la lista según la fecha y hora
        list_projects.sort(key=lambda element: datetime.datetime.strptime(element.attrib["fecha"], "%Y-%m-%d %H:%M:%S"))

        # Comprueba si los archivos existen, sino, los elimina de la lista
        for project in list_projects:
            if not os.path.exists(project.attrib["path"]):
                list_projects.pop(list_projects.index(project))
                self._xml.delete_element_in_container("projects", "project", project.attrib)
        # Agrega los proyectos a la lista
        for project in list_projects:
            aux_item = GUIProjectItem(
                self.ui.container_proyectos_elements,
                project.attrib["name"],
                project.attrib["path"],
                project.attrib["fecha"]
            )
            aux_item.delete_signal.connect(self._delete_this_pi)
            aux_item.open_me_signal.connect(self._open_this_pi)
            self.ui.container_projects_layout.addWidget(aux_item)

    @gui_utils.secure_execution
    def _delete_this_pi(self, input_dict: dict):
        self._xml.delete_element_in_container("projects", "project", {
            "name": input_dict["to_delete"].name,
            "path": input_dict["to_delete"].path,
            "fecha": input_dict["to_delete"].fecha
        })
        self._update_projects()

    @gui_utils.secure_execution
    def _open_this_pi(self, input_dict: dict):
        self._open_project(input_dict["to_open"].path)

    @gui_utils.secure_execution
    def _save_project(self, *args, **kwargs):
        # Crea una instancia del cuadro de diálogo de selección de archivo
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        dialog.setNameFilter("GSD (*.gsd)")

        # Abre el cuadro de diálogo y espera a que el usuario seleccione un archivo y un directorio
        if dialog.exec_() == QFileDialog.Accepted:
            ruta_seleccionada = dialog.selectedFiles()[0]
            gui_utils.package_project(self.my_data_for_dim,
                                      self.ui.list_selected.findChildren(AbstractCardListElement),
                                      ruta_seleccionada)
            # Guarda la ruta del proyecto en el archivo de persistencia
            # Primero, comprueba que el proyecto: nombre + ruta, se encuentre en el archivo config
            list_projects = self._xml.get_list_elements_in_container("projects", "project")
            if len(list_projects) == 0:
                self._xml.add_element_in_container(
                    "projects",
                    "project",
                    {
                        "name": self.my_data_for_dim["name"],
                        "path": ruta_seleccionada,
                        "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                )
            elif len(list(filter(lambda elem: elem.attrib["path"] == ruta_seleccionada, list_projects))) > 0:
                attrs = list(filter(lambda elem: elem.attrib["path"] == ruta_seleccionada, list_projects))[0]
                self._xml.replace_attrib_value("projects",
                                               "project",
                                               attrs,
                                               {
                                                   "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                               }
                                               )
            else:
                self._xml.add_element_in_container(
                    "projects",
                    "project",
                    {
                        "name": self.my_data_for_dim["name"],
                        "path": ruta_seleccionada,
                        "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                )

            self._update_projects()
        del dialog

    @gui_utils.secure_execution
    def _open_project(self, route):
        data = json.loads(open(route, "r").read())

        data_dim = data["data_project"]
        self._data_for_sizing_is_here(data_dim)

        for load in data["serializate_list"]:
            if load["type"] == "ResistanceCardListElement":
                self._add_resistance(init_data=load["data"])
            if load["type"] == "LumCardListElement":
                self._add_lum(init_data=load["data"])
            if load["type"] == "MotorCardListElement":
                self._add_motor(init_data=load["data"])
            if load["type"] == "NonLinealCardListElement":
                self._add_non_lineal_load(init_data=load["data"])
            if load["type"] == "LinearLoadCardListElement":
                self._add_lineal_load(init_data=load["data"])
            if load["type"] == "AirCardListElement":
                self._add_air(init_data=load["data"])

    @gui_utils.secure_execution
    def _report(self, *args, **kwargs):
        # Crea una instancia del cuadro de diálogo de selección de archivo
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        dialog.setNameFilter("PDF (*.pdf)")
        # Abre el cuadro de diálogo y espera a que el usuario seleccione un archivo y un directorio
        if dialog.exec_() == QFileDialog.Accepted:
            # Obtiene la ruta del archivo seleccionado por el usuario
            ruta_seleccionada = dialog.selectedFiles()[0]
            gui_utils.Crear_Reporte(
                self.my_data_for_dim,
                self.maxvd,
                self.maxthd,
                self.porc_carga,
                self.kva_total_rp,
                self.dict_desc,
                self.dict_kva_rp,
                self.dict_arranques,
                self.dict_vd,
                ruta_seleccionada,
                self._user_name,
                self.kw_rp,
                self.my_machine
            )

    # Función para rellenar la tabla con los datos de la bd
    def _actualizar(self):
        # Conectar a la base de datos
        conn = sqlite3.connect('gensets.db.db')
        cursor = conn.cursor()

        # Ejecutar una consulta SQL para obtener los datos de la tabla
        cursor.execute("SELECT * FROM machine")

        # Obtener los datos de la consulta
        datos = cursor.fetchall()

        # Establecer las dimensiones de la tabla
        self.ui.tabla_db.setRowCount(len(datos))
        self.ui.tabla_db.setColumnCount(len(datos[0]) - 1)
        column_headers = [description[0] for description in cursor.description]
        self.ui.tabla_db.setHorizontalHeaderLabels(column_headers)

        # Llenar la tabla con los datos
        for i, fila in enumerate(datos):
            for j, columna in enumerate(fila):
                celda = QtWidgets.QTableWidgetItem(str(columna))
                self.ui.tabla_db.setItem(i, j, celda)

        # Bloquear todas las celdas
        self.ui.tabla_db.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        # Activar edición en celda de la columna "id"
        self.ui.tabla_db.cellClicked.connect(self._click_celda)

    # Elimina la fila seleccionada
    @gui_utils.secure_execution
    def _eliminar(self, *args, **kwargs):
        if self.B is not None:
            # Agregar código para la función del botón "ELIMINAR" aquí
            aux_dialog = GUIBaseDialog(None, GUIBaseDialog.SET_ICON_DIALOG_INFORMATION)
            aux_dialog.setDialogMessTitle("Eliminar generador de la base de datos.")
            aux_dialog.setDialogMessInformation(
                "¿Está seguro que desea eliminar la máquina seleccionada de la base de datos?"
            )
            if aux_dialog.exec():
                aux_dialog.setDialogMessInformation(
                    "Al pulsar 'Ok', la máquina seleccionada será eliminada. ¿Desea eliminar la máquina seleccionada?"
                )
                if aux_dialog.exec():
                    conn = sqlite3.connect('gensets.db.db')
                    conn.execute(f"DELETE FROM machine WHERE id = {self.B}")
                    conn.commit()
                    self._actualizar()
                    self.B = None

    def _agregar(self):
        self.aux_gui_db.exec()

    # Obitiene el ID de la fila y la pinta completa
    @gui_utils.secure_execution
    def _click_celda(self, fila, columna):
        celda = self.ui.tabla_db.item(fila, 0)
        self.B = int(celda.text())
        for i in range(0, self.ui.tabla_db.columnCount()):
            if self.ui.tabla_db.item(self._last_fila, i):
                self.ui.tabla_db.item(self._last_fila, i).setBackground(QtGui.QColor(248, 248, 248))
            self.ui.tabla_db.item(fila, i).setBackground(QtGui.QColor(11, 209, 252))
        self._last_fila = fila

    # Método para manejar el llamado a dimensionar una máquina
    def _data_for_sizing_is_here(self, data: dict):
        self.sizing_window.close()
        self.ui.stackedWidget.setCurrentWidget(self.ui.dim_select_page)
        self.my_data_for_dim = data

        self.ui.nombre_proyecto.setText(data["name"])
        self.ui.voltaje_proyecto.setText(str(data["voltaje"]))
        self.ui.fases_proyecto.setText(str(data["fases"]))
        self.ui.frecuencia_proyecto.setText(str(data["frecuencia"]))
        self.ui.altura_proyecto.setText(str(data["altura"]))
        self.ui.temperatura_proyecto.setText(str(data["temperatura"]))
        self.ui.tiempo_servicio_proyecto.setText(str(data["tiempo_servicio"]))
        self.ui.reserva_proyecto.setText(str(data["reserva"]))
        self.ui.voltaje_dip_proyecto.setText(str(data["voltaje_dip"]))
        self.ui.combustibl_proyecto.setText(data["combustible"])
        self.ui.ciclo_proyecto.setText(data["ciclo_trabajo"])
        self.ui.iso_proyecto.setText(data["ISO_8528"])

        for elem in self.ui.list_selected.findChildren(AbstractCardListElement):
            elem.deleteLater()

    @gui_utils.secure_execution
    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        for temp in self.findChildren(GUITemporalMessage):
            if temp.isVisible():
                title = temp.get_title()
                mess = temp.get_mess()
                icon = temp.get_icon_type()
                pos = temp.get_position()

                temp.close()
                GUITemporalMessage(self, title, mess, icon, pos)

    @gui_utils.secure_execution
    def _last_curve_act(self, *args, **kwargs):
        if self._last_curve_generated == "":
            self.ui.ultima_curva_2.setVisible(False)
            self.ui.frame_14.setVisible(True)
        elif os.path.exists(self._last_curve_generated):
            pixmap = QPixmap(self._last_curve_generated)
            name = os.path.basename(self._last_curve_generated)
            self.ui.label_3.setText("Última curva generada: " + name)
            self.ui.ultima_curva_label.setPixmap(pixmap)
            self.ui.ultima_curva_2.setVisible(True)
            self.ui.frame_14.setVisible(False)
        else:
            self._xml.container_tag_change_attrib("last-curve", "url", "")
            self._last_curve_generated = ""
            self.ui.ultima_curva_2.setVisible(False)
            self.ui.frame_14.setVisible(True)

    def _add_air(self, init_data=None):
        a_card = AirCardListElement(self.ui.list_selected, float(self.my_data_for_dim["voltaje"]),
                                    initial_values=init_data, fases=self.my_data_for_dim["fases"])
        a_card.set_icon(url="./img/copo-de-nieve.png")
        a_card.set_card_title("Aire acondicionado")
        self.ui.list_selected_layout.addWidget(a_card)

    def _add_lineal_load(self, init_data=None):
        a_card = LinearLoadCardListElement(self.ui.list_selected, initial_values=init_data, fases=self.my_data_for_dim["fases"])
        a_card.set_icon(url="./img/lineal.png")
        a_card.set_card_title("Carga lineal")
        self.ui.list_selected_layout.addWidget(a_card)

    def _add_motor(self, init_data=None):
        a_card = MotorCardListElement(self.ui.list_selected, initial_values=init_data, fases=self.my_data_for_dim["fases"])
        a_card.set_icon(url="./img/motor-electrico.png")
        a_card.set_card_title("Motor electrico")
        self.ui.list_selected_layout.addWidget(a_card)

    def _add_lum(self, init_data=None):
        a_card = LumCardListElement(self.ui.list_selected, initial_values=init_data)
        a_card.set_icon(url="./img/bombilla.png")
        a_card.set_card_title("Luminaria")
        self.ui.list_selected_layout.addWidget(a_card)

    def _add_resistance(self, init_data=None):
        a_card = ResistanceCardListElement(self.ui.list_selected, initial_values=init_data, fases=self.my_data_for_dim["fases"])
        a_card.set_icon(url="./img/resistencia (1).png")
        a_card.set_card_title("Resistencia")
        self.ui.list_selected_layout.addWidget(a_card)

    def _add_non_lineal_load(self, init_data=None):
        a_card = NonLinealCardListElement(self.ui.list_selected, initial_values=init_data)
        a_card.set_icon(url="./img/non_linear.png")
        a_card.set_card_title("No lineal")
        self.ui.list_selected_layout.addWidget(a_card)

    def _anterior_graph(self):
        if isinstance(self.static_graph.get_gen(), CylindricalGen):
            self.ui.stackedWidget.setCurrentWidget(self.ui.datos_liso)
        elif isinstance(self.static_graph.get_gen(), SalientGen):
            self.ui.stackedWidget.setCurrentWidget(self.ui.datos_saliente)

    def _siguiente_carga(self):
        diccionarios_ordenados = {}
        thdv_loads = []
        diccionario_descriptions = {}
        kva_rp_dict = {}
        if len(self.ui.list_selected.findChildren(AbstractCardListElement)) > 0:
            for elem in self.ui.list_selected.findChildren(AbstractCardListElement):
                if not elem.data_panel.is_checked():
                    GUITemporalMessage(self, "Error al ingresar los datos de las cargas.", "Una o más cargas no son "
                                                                                           "correctas. Rellena los campos"
                                                                                           " requeridos.", 11,
                                       position=5)
                    return None
                else:
                    aux_descriptions = elem.get_description()
                    # Acá se guardan las cargas no lineals y los motores con variador de frecuencia
                    if isinstance(elem, NonLinealCardListElement) or (
                            isinstance(elem, MotorCardListElement) and elem.get_values()[
                        "Metodo_arranque"] == "Variador de frecuencia"):
                        thdv_loads.append(elem)

                    # Acá se suman las potencias de las cargas que se encuentran en cada paso respectivo
                    # Se crean las claves para una lista que guarde a las cargas del paso respectivo
                    # En power_#### se guarda la potencia activa de rp y de rt
                    # En reactive_### se guarda la potencia reactiva de rp y de rt
                    # En arranque_paso se guardará la potencia de recepción de ese paso
                    aux_power = elem.get_apparent_power()
                    paso = aux_power['step']
                    if paso not in diccionarios_ordenados:
                        diccionarios_ordenados[paso] = {
                            'load_list': [],
                            'power_star': 0,
                            'power_run': 0,
                            'reactive_star': 0,
                            'reactive_run': 0,
                            'arranque_paso': 0,
                            'voltage_dip_step': 0,
                            'fp_step': 0
                        }
                    diccionarios_ordenados[paso]['load_list'].append(elem)
                    for clave in ['power_star', 'power_run', 'reactive_star', 'reactive_run']:
                        diccionarios_ordenados[paso][clave] += aux_power[clave]

                    if paso not in diccionario_descriptions:
                        diccionario_descriptions[paso] = []
                    diccionario_descriptions[paso].append(aux_descriptions)
                    diccionario_descriptions = dict(sorted(diccionario_descriptions.items(), key=lambda x: x[0]))
                    self.dict_desc = diccionario_descriptions

            for step in range(1, max(diccionarios_ordenados.keys()) + 1):
                diccionarios_ordenados.setdefault(step,
                                                  {
                                                      'power_star': 0,
                                                      'power_run': 0,
                                                      'reactive_star': 0,
                                                      'reactive_run': 0
                                                  })
            diccionarios_ordenados = dict(sorted(diccionarios_ordenados.items(), key=lambda x: x[0]))
            kva_rp_dict = step_kvarp(diccionarios_ordenados)
            self.dict_kva_rp = kva_rp_dict
            self.kw_rp = diccionarios_ordenados

            # En este ciclo se obtiene la potencia aparente de puesta en marcha de cada paso
            # La potencia de puesta en marca es igual a la suma la potencia en rp de las estapas 1 a n-1
            # más la potencia de arranque en la etapa n
            for key, values in diccionarios_ordenados.items():
                # Obtiene la potencia activa y reactiva en el paso actual
                active = diccionarios_ordenados[key]['power_star']
                reactive = diccionarios_ordenados[key]['reactive_star']
                p = diccionarios_ordenados[key]['power_run']
                q = diccionarios_ordenados[key]['reactive_run']
                # Si la clave es 1, no hay cargas ya conectadas y solo calcula el módulo de la potencia
                # aparente de arranque en el paso 1
                if key == 1:
                    diccionarios_ordenados[1]['arranque_paso'] = math.sqrt(active ** 2 + reactive ** 2)
                    diccionarios_ordenados[key]['p_arr'] = active
                    diccionarios_ordenados[key]['p_marcha'] = diccionarios_ordenados[key]['power_run']
                    diccionarios_ordenados[key]['kva_marcha'] = math.sqrt(p ** 2 + q ** 2)
                # Para el resto de pasos, se debe calcular la potencia aparente en rp del resto de pasos -> [1, n)
                # El resultado de esto se suma con la potencia aparente de arranque de la etapa n
                else:
                    p_run, q_run = _partial_run_power_v(diccionarios_ordenados, key)
                    diccionarios_ordenados[key]['arranque_paso'] = math.sqrt(
                        (active + p_run) ** 2 + (reactive + q_run) ** 2)
                    diccionarios_ordenados[key]['p_arr'] = active + p_run
                    diccionarios_ordenados[key]['p_marcha'] = p_run + diccionarios_ordenados[key]['power_run']
                    diccionarios_ordenados[key]['kva_marcha'] = math.sqrt((p + p_run) ** 2 + (q + q_run) ** 2)
                diccionarios_ordenados[key]['fp_step'] = active / diccionarios_ordenados[key]['arranque_paso']

            arranque_dict = {}
            for key, values in diccionarios_ordenados.items():
                arranque_dict[key] = diccionarios_ordenados[key]['arranque_paso']

            self.dict_arranques = arranque_dict

            voltaje = self.my_data_for_dim["voltaje"]
            frecuencia = self.my_data_for_dim["frecuencia"]
            reserva = 1 + self.my_data_for_dim["reserva"] / 100
            derating = reserva / (gui_utils.derating_temperature_factor(self.my_data_for_dim["temperatura"]) *
                                  gui_utils.derating_altitude_factor(self.my_data_for_dim["altura"]))
            rp_total = _partial_run_power(diccionarios_ordenados, len(diccionarios_ordenados) + 1) * derating
            rt_max, step_max = get_max_start(diccionarios_ordenados)

            valores = self.consultar(
                voltaje,
                frecuencia,
                rp_total,
                rt_max
            )
            if len(valores) == 0:
                aux_dialog = GUIBaseDialog(None, GUIBaseDialog.SET_ICON_DIALOG_INFORMATION)
                aux_dialog.setDialogMessTitle("No se ha encontrado un generador.")
                aux_dialog.setDialogMessInformation(
                    f"La potencia de la carga comprendida entre {round(1.05 * rp_total, 2)} y {round(2 * rp_total, 2)} (25% - 90%), no "
                    f"puede ser alimentada por ninguno de los generadores que se encuentran en la base de datos."
                )
                aux_dialog.exec()
            else:

                # Inicia la comprobación para más de un paso
                definir = {"id": 0, "volt": 0, "machine": None, "step_vd": 0, "xd": 0, "kva_machine": 0}

                nuevo = []  # lista para almacenar los vd
                id_aux = 0  # Guarda el id de la máquina seleccionada
                # Inicia el ciclo con los generadores
                for result in valores:
                    nuevo = []
                    # Parámetros para el cálculo del THD
                    id = result[0]
                    xd = result[1]
                    xd_prima = result[2]
                    xq = result[3]
                    kva_machine = result[5]
                    curves = pickle.loads(result[4])  # Acá se obtiene la lista de las curvas
                    imprimir = pickle.loads(curves[int(voltaje)])  # Acá se obtiene la curva para el voltaje del
                    # sistema desbinarizado

                    # Acá se calcula el VD para la potencia de puesta en marcha de cada paso en la curva de la máquina actual
                    for key, value in diccionarios_ordenados.items():
                        fp_factor = gui_utils.correction_factor_power(diccionarios_ordenados[key]['fp_step'])
                        resultado = round(abs(imprimir.eval(diccionarios_ordenados[key]['arranque_paso']) * fp_factor),
                                          4)
                        nuevo.append(resultado)

                    # Verifica que el máximo VD no supere el VD G1, G2 o G3
                    if max(nuevo) < self.my_data_for_dim["voltaje_dip"]:
                        # Esta condición es para cuando se obtiene la primera máquina que cumple
                        if (definir["volt"] == 0 and definir["id"] == 0) or (definir["volt"] > max(nuevo)):
                            id_final = result[0]
                            definir["volt"] = max(nuevo)
                            definir["step_vd"] = nuevo.index(definir["volt"]) + 1
                            definir["id"] = id_final
                            definir["machine"] = result
                            definir["xd"] = xd
                            definir["kva_machine"] = kva_machine
                            definir["list_vd"] = nuevo

                    # Esta condición verifica que se ha llegado a la última máquina 
                    if result == valores[-1]:
                        # Comprueba si el id y el VD guardado en
                        # definir es cero respectivamente. En tal caso, no se encontró ninguna máquina que cumpliera con los
                        # requerimientos de respuesta transitoria.
                        if definir["id"] == 0 and definir["volt"] == 0:
                            aux_dialog = GUIBaseDialog(None, GUIBaseDialog.SET_ICON_DIALOG_INFORMATION)
                            aux_dialog.setDialogMessTitle("No se ha encontrado un generador.")
                            aux_dialog.setDialogMessInformation(
                                f"La caída de tensión provocada por la carga en todos los generadores "
                                f"calificados "
                                f"de la base de datos sobrepasa el valor límite especificado por el régimen de "
                                f"servicio {self.my_data_for_dim['ISO_8528']}."
                            )
                            aux_dialog.exec()
                        # En caso contrario, si hay una máquina que cumplió con los requerimientos den rt y en rp.
                        else:
                            # Cálculo del THD
                            if len(thdv_loads) != 0:
                                thd = gui_utils.THD_Calculated(thdv_loads, len(diccionarios_ordenados), definir["xd"],
                                                               definir["kva_machine"])
                                if thd[max(thd, key=thd.get)] > self.my_data_for_dim["THD"]:
                                    self.ui.label_32.setStyleSheet("QLabel{color: red;}")
                                else:
                                    self.ui.label_32.setStyleSheet("QLabel{color: green;}")
                                self.ui.label_32.setText(str(round(thd[max(thd, key=thd.get)], 2)) + "%")
                                self.maxthd = str(round(thd[len(diccionarios_ordenados)], 2)) + "%"
                            else:
                                self.maxthd = "NA"
                                self.ui.label_32.setText("NA")
                            self.maxvd = definir['volt']

                            self.porc_carga = str(round((rp_total / derating) / definir["machine"][5] * 100, 3)) + "%"
                            self.kva_total_rp = str(round(rp_total / derating, 2)) + " kVA"
                            print(
                                f"la maquina con la id elegida es : {definir['id']} tiene un Voltage dip de : {definir['volt']} ")
                            self.my_machine = definir["machine"]
                            # Datos del proyecto
                            self.ui.nombre_proyecto_dim.setText(self.my_data_for_dim["name"])
                            self.ui.voltaje_dim.setText(str(self.my_data_for_dim["voltaje"]) + " V")
                            self.ui.fases_dim.setText(str(self.my_data_for_dim["fases"]))
                            self.ui.frecuencia_dim.setText(str(self.my_data_for_dim["frecuencia"]) + " Hz")
                            self.ui.altura_dim.setText(str(int(self.my_data_for_dim["altura"])) + " m")
                            self.ui.temperautra_dim.setText(str(int(self.my_data_for_dim["temperatura"])) + " °C")
                            self.ui.tiempo_dim.setText(str(int(self.my_data_for_dim["tiempo_servicio"])) + " h")
                            self.ui.reserva_dim.setText(str(int(self.my_data_for_dim["reserva"])) + " %")
                            self.ui.iso_dim.setText(self.my_data_for_dim["ISO_8528"])
                            self.ui.combustible_dim.setText(self.my_data_for_dim["combustible"])
                            self.ui.ciclo_dim.setText(self.my_data_for_dim["ciclo_trabajo"])
                            self.ui.thd_dim.setText(str(int(self.my_data_for_dim["THD"])) + " %")

                            # Datos del sistema
                            self.ui.potencia_rp_dim.setText(str(round(rp_total / derating, 2)) + " kVA")
                            self.ui.pasos_dim.setText(str(len(diccionarios_ordenados)))
                            self.ui.max_p_arr_dim.setText(str(round(rt_max, 2)) + " kVA")
                            self.ui.step_dim.setText(str(step_max))
                            # Datos del generador
                            self.ui.fabricante_dim.setText(definir["machine"][6])
                            self.ui.potencia_dim.setText(str(round(definir["machine"][5], 2)) + " kVA")
                            self.ui.voltaje_dip_dim.setText(str(round(definir["volt"], 2)) + " %")
                            self.ui.step_vd_dim.setText(str(round(definir["step_vd"], 2)))
                            self.ui.modelo_dim.setText(definir["machine"][7])
                            self.ui.cargabilidad_dim.setText(
                                str(round((rp_total / derating) / definir["machine"][5] * 100, 3)) + "%")
                            self.ui.reserva_dim_2.setText(
                                str(round((definir["machine"][5] - rp_total / derating) / definir["machine"][5] * 100,
                                          3)) + "%")

                            conn = sqlite3.connect('gensets.db.db')
                            c = conn.cursor()
                            c.execute(
                                "SELECT id, manufacturer, alternator_model, power_kva, xq, xd, xd_prima FROM machine WHERE id >= ? and id <= ?",
                                (definir['id'], definir['id'] + 5)
                            )
                            aux_res_dim = c.fetchall()
                            conn.close()

                            # Llenando la tabla con los generadores
                            self.ui.tabla_gensets.setRowCount(len(aux_res_dim))
                            for machine in aux_res_dim:
                                row = aux_res_dim.index(machine)
                                for data in machine:
                                    col = machine.index(data)
                                    item = QTableWidgetItem(str(data))
                                    if machine == aux_res_dim[0]:
                                        item.setBackground(QtGui.QColor(0, 204, 0))
                                    self.ui.tabla_gensets.setItem(row, col, item)

                            self.ui.stackedWidget.setCurrentWidget(self.ui.resultados_dim)
                self.dict_vd = definir["list_vd"]

    # Funciones hechas por Jimmy para el diccionario.
    @gui_utils.secure_execution
    def consultar(self, voltage, frecuencia, kVA, hola):
        # nos conectamos a la base de datos y hacemos la consulta
        conn = sqlite3.connect('gensets.db.db')
        c = conn.cursor()
        c.execute(
            "SELECT id, xd, xd_prima, xq, curve, power_kva, manufacturer, alternator_model FROM machine WHERE frequency = ? AND voltage LIKE ? AND "
            "power_kva BETWEEN ? AND ? AND (?/power_kva) <= ? ORDER BY (power_kva) DESC LIMIT 10",
            (frecuencia, f'%{voltage}%', 1.11 * kVA, 4 * kVA, hola, 2))
        results = c.fetchall()
        conn.close()
        return results

    @gui_utils.secure_execution
    def _update_status_bar(self, l_pos):
        q = l_pos[0]
        p = l_pos[1]
        s = np.sqrt(q ** 2 + p ** 2)
        self.static_graph.fig.suptitle(
            f"Punto de operación: P={np.round(l_pos[1], 3)}PU Q={np.round(l_pos[0], 3)}PU Fp={np.round(np.abs(p) / s, 3)} δ={l_pos[2]}° Ef={l_pos[3]}")

    @gui_utils.secure_execution
    def _screen_shot(self, *args, **kwargs):
        # Crea una instancia del cuadro de diálogo de selección de archivo
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        dialog.setNameFilter("JPEG (*.jpg)")

        # Abre el cuadro de diálogo y espera a que el usuario seleccione un archivo y un directorio
        if dialog.exec_() == QFileDialog.Accepted:
            # Obtiene la ruta del archivo seleccionado por el usuario
            ruta_seleccionada = dialog.selectedFiles()[0]
            self._xml.container_tag_change_attrib("last-curve", "url", ruta_seleccionada)
            self._last_curve_generated = ruta_seleccionada
            # Toma la captura de pantalla y guarda la imagen en la ruta seleccionada
            screen = QtWidgets.QApplication.primaryScreen()
            screenshot = screen.grabWindow(self.ui.graph_container.winId())
            screenshot.save(ruta_seleccionada, 'jpg')
            self._last_curve_act()
            gen = self.static_graph.get_gen()
            if isinstance(gen, CylindricalGen):
                aux_attr = {
                    "pa": str(gen.get_electric_parameters()["S: "]),
                    "fp": str(gen.get_electric_parameters()["Fp: "]),
                    "tmc": str(gen.get_electric_parameters()["Ef: "]),
                    "pe": str(gen.get_electric_parameters()["Seg. prac. "]),
                    "vpu": "True",
                    "vn": str(gen.get_electric_parameters()["V: "]),
                    "rs": str(gen.get_electric_parameters()["Xs: "]),
                    "pm": str(gen.get_electric_parameters()["P: "]),
                    "ps": str(gen.get_electric_parameters()["Seg. min.: "])
                }
                self._xml.container_tag_change_attrib("last-curve", "type", "cylindrical")
                self._xml.replace_one_attrib_value("last-curve", "cylindrical", aux_attr)
            else:
                aux_attr = {
                    "pa": str(gen.get_electric_parameters()["S: "]),
                    "fp": str(gen.get_electric_parameters()["Fp: "]),
                    "tmc": str(gen.get_electric_parameters()["Ef: "]),
                    "pe": str(gen.get_electric_parameters()["Seg. prac. "]),
                    "vpu": "True",
                    "vn": str(gen.get_electric_parameters()["V: "]),
                    "rd": str(gen.get_electric_parameters()["Xd: "]),
                    "rs": str(gen.get_electric_parameters()["Xq: "]),
                    "pm": str(gen.get_electric_parameters()["P: "]),
                    "ps": str(gen.get_electric_parameters()["Seg. min.: "])
                }
                self._xml.container_tag_change_attrib("last-curve", "type", "salient")
                self._xml.replace_one_attrib_value("last-curve", "salient", aux_attr)

    @gui_utils.secure_execution
    def _load_last_curve(self, event):
        type = self._xml.get_root_attrib_value("last-curve", "type")
        if type == "cylindrical":
            attr = self._xml.get_list_elements_in_container("last-curve", "cylindrical")[0].attrib
            self.c_layout.removeWidget(self.static_graph)
            self.static_graph = MyMplCanvas(parent=self.w_canvas)
            self.static_graph.mess_to_emit.connect(self._update_status_bar)
            self.c_layout.addWidget(self.static_graph)
            self._wait_panel.show()
            data_plate = {
                "sn": float(attr["pa"]),
                "vn": float(attr["vn"]),
                "fp": float(attr["fp"]),
                "xs": float(attr["rs"]),
                "p_motriz": float(attr["pm"]),
                "seg_min": float(attr["ps"]),
                "seg_prac": float(attr["pe"]),
                "ef": float(attr["tmc"]),
                "per_units": bool(attr["vpu"])
            }
            self.static_graph.set_gen(CylindricalGen(**data_plate),
                                      parent_layout_data=self.ui.graph_data_layout,
                                      parent_frame_data=self.ui.graph_container_data)
            self.thread = DeepThread(self.static_graph)
            self.thread.mess_graph_signal.connect(self._wait_panel.update_message)
            self.thread.im_end.connect(self._plot_finished)
            self.thread.im_end.connect(lambda: self._wait_panel.hide())
            self.thread.start()
        else:
            attr = self._xml.get_list_elements_in_container("last-curve", "salient")[0].attrib
            self.c_layout.removeWidget(self.static_graph)
            self.static_graph = MyMplCanvas(parent=self.w_canvas)
            self.static_graph.mess_to_emit.connect(self._update_status_bar)
            self.c_layout.addWidget(self.static_graph)
            self._wait_panel.show()

            data_plate = {
                "sn": float(attr["pa"]),
                "vn": float(attr["vn"]),
                "fp": float(attr["fp"]),
                "xd": float(attr["rd"]),
                "xq": float(attr["rq"]),
                "p_motriz": float(attr["pm"]),
                "seg_min": float(attr["ps"]),
                "seg_prac": float(attr["pe"]),
                "ef": float(attr["tmc"]),
                "per_units": bool(attr["vpu"])
            }
            self.static_graph.set_gen(SalientGen(**data_plate),
                                      parent_layout_data=self.ui.graph_data_layout,
                                      parent_frame_data=self.ui.graph_container_data)
            self.thread = DeepThread(self.static_graph)
            self.thread.mess_graph_signal.connect(self._wait_panel.update_message)
            self.thread.im_end.connect(self._plot_finished)
            self.thread.im_end.connect(lambda: self._wait_panel.hide())
            self.thread.start()

    def _actualizate_loading_mess(self, mess: str):
        self.ui.mensaje_progreso.setText(mess)

    def _plot_finished(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.visualizar)

    def _set_generator_from_thread(self, gen):
        self.static_graph.set_gen(gen,
                                  parent_layout_data=self.ui.graph_data_layout,
                                  parent_frame_data=self.ui.graph_container_data)

    @gui_utils.secure_execution
    def moveEvent(self, event):
        for temp in self.findChildren(GUITemporalMessage):
            temp.move(temp.x_init + self.pos().x(), temp.y_init + self.pos().y())

    # Función para el manejo de valores en PU de una máquina de polos salientes
    def onClicked(self):
        if not self.ui.saliente_pu_check_3.isChecked():
            self.saliente_pu = False
            self.ui.voltaje_nominal_sal_3.setVisible(True)
            self.ui.sal_v_nom_pu.setVisible(False)
            self.ui.sal_p_aparente_3.setEnabled(True)
            self.ui.sal_p_aparente_3.setText("")
            self.ui.sal_r_q_label_3.setText("Reactancia cuadratura**(Ω)")
            self.ui.sal_v_n_label_3.setText("Voltaje nominal**(V)")
            self.ui.sal_r_d_label_3.setText("Reactancia directa**(Ω)")
            self.ui.sal_p_m_label_3.setText("Potencia motriz máxima(W)")
            self.ui.sal_p_aparente_label_3.setText("Potencia aparente**(V)")
        elif self.ui.saliente_pu_check_3.isChecked():
            self.saliente_pu = True
            self.ui.voltaje_nominal_sal_3.setVisible(False)
            self.ui.sal_v_nom_pu.setVisible(True)
            self.ui.sal_p_aparente_3.setText("1")
            self.ui.sal_p_aparente_3.setEnabled(False)
            self.ui.sal_v_nom_pu.setEnabled(False)
            self.ui.sal_v_nom_pu.setText("1")
            self.ui.sal_r_q_label_3.setText("Reactancia cuadratura**(p.u.)")
            self.ui.sal_v_n_label_3.setText("Voltaje nominal**(p.u.)")
            self.ui.sal_r_d_label_3.setText("Reactancia directa**(p.u.)")
            self.ui.sal_p_m_label_3.setText("Potencia motriz máxima(p.u.)")
            self.ui.sal_p_aparente_label_3.setText("Potencia aparente**(p.u.)")

        if not self.ui.liso_pu_check.isChecked():
            self.liso_pu = False
            self.ui.voltaje_nominal.setVisible(True)
            self.ui.liso_v_nom_pu.setVisible(False)
            self.ui.liso_p_aparente.setEnabled(True)
            self.ui.liso_p_aparente.setText("")
            self.ui.liso_p_aparente_label.setText("Potencia aparente**(VA)")
            self.ui.liso_v_n_label.setText("Voltaje nominal**(V)")
            self.ui.liso_r_s_label.setText("Reactancia sincrónica**(Ω)")
            self.ui.liso_p_m_label.setText("Potencia motriz máxima(W)")
        elif self.ui.liso_pu_check.isChecked():
            self.liso_pu = True
            self.ui.voltaje_nominal.setVisible(False)
            self.ui.liso_v_nom_pu.setVisible(True)
            self.ui.liso_v_nom_pu.setText("1")
            self.ui.liso_v_nom_pu.setEnabled(False)
            self.ui.liso_p_aparente.setEnabled(False)
            self.ui.liso_p_aparente.setText("1")
            self.ui.liso_p_aparente_label.setText("Potencia aparente**(p.u.)")
            self.ui.liso_v_n_label.setText("Voltaje nominal**(p.u.)")
            self.ui.liso_r_s_label.setText("Reactancia sincrónica**(p.u.)")
            self.ui.liso_p_m_label.setText("Potencia motriz máxima(p.u.)")

    # Funcion para graficar curva de polos salientes
    @gui_utils.secure_execution
    def _graficar_saliente(self, *args, **kwargs):
        r_d = self.ui.sal_r_d_3.text()  # Reactancia de eje directo
        r_q = self.ui.sal_r_q_3.text()  # Reactancia de eje de cuadratura
        p = self.ui.sal_p_m_3.text()  # Potencia motriz
        p_s = self.ui.sal_p_aparente_3.text()  # Potencia aparente
        f_p = self.ui.sal_f_p_3.text()  # Factor de potencia
        t_c_max = self.ui.sal_t_m_c_3.text()  # Tension máxima de campo
        e_p = int(self.ui.sal_porcentaje_practica.currentText())  # Porcentaje de estabilidad práctica
        v_n = int(self.ui.voltaje_nominal_sal_3.currentText()) if not self.saliente_pu else self.ui.sal_v_nom_pu.text()
        p_seg = int(self.ui.sal_porcentaje_seg_3.currentText())

        try:
            if len(r_q) == 0 or len(r_d) == 0 or len(p_s) == 0 or len(f_p) == 0:
                GUITemporalMessage(self, "Error al ingresar los datos", "Uno o más campos están vacíos.", 11,
                                   position=1)
                return
            v_n = float(v_n)
            r_d = float(r_d)
            r_q = float(r_q)
            p = 0.0 if len(p) == 0 or p == '0' else float(p)
            p_seg = p_seg / 100.0
            p_s = float(p_s)
            f_p = float(f_p)
            t_c_max = None if len(t_c_max) == 0 or t_c_max == '0' or t_c_max == '0.0' else float(t_c_max)
            e_p = e_p / 100.0
        except ValueError:
            GUITemporalMessage(self, "Error al ingresar los datos", "Solo puedes ingresar dígitos en los campos.", 11,
                               position=1)
            return

        # Convierte a todos los valores a números positivos
        r_d = abs(r_d)
        r_q = abs(r_q)
        p = abs(p)
        p_s = abs(p_s)
        f_p = abs(f_p)
        t_c_max = abs(t_c_max) if t_c_max is not None else None
        v_n = abs(v_n)

        # Actualiza los valores en los campos luego de aplicar valor absoluto
        self.ui.sal_r_d_3.setText(str(r_d))
        self.ui.sal_r_q_3.setText(str(r_q))
        self.ui.sal_p_m_3.setText(str(p))
        self.ui.sal_p_aparente_3.setText(str(p_s))
        self.ui.sal_f_p_3.setText(str(f_p))
        if self.saliente_pu:
            self.ui.sal_v_nom_pu.setText(str(v_n))
        if t_c_max is not None:
            self.ui.sal_t_m_c_3.setText(str(t_c_max))

        # Comprueba que el Factor de potencia sea correcto
        if f_p >= 1 or f_p <= 0:
            GUITemporalMessage(self, "Error al ingresar los datos",
                               "Ingrese un factor de potencia válido para la máquina.", 11,
                               position=1)
        # Comprueba que, si la p_motriz es distinta de cero y que no sea mayor que la potencia aparente
        elif p != 0 and p_s < p:
            GUITemporalMessage(self, "Error al ingresar los datos",
                               "La potencia motriz y aparente ingresadas no son correctas.", 11,
                               position=1)
        elif r_d == 0:
            GUITemporalMessage(self, "Error al ingresar los datos",
                               "La reactancia de eje directo debe ser un número mayor a cero.", 11,
                               position=1)
        elif r_q == 0:
            GUITemporalMessage(self, "Error al ingresar los datos",
                               "La reactancia de cuadratura debe ser un número mayor a cero.", 11,
                               position=1)
        elif p_s == 0:
            GUITemporalMessage(self, "Error al ingresar los datos",
                               "La potencia aparente debe ser un número mayor a cero.", 11,
                               position=1)
        elif r_q > r_d:
            GUITemporalMessage(self, "Error al ingresar los datos",
                               "La reactancia de cuadratura no puede ser mayor que la de eje directo.", 11,
                               position=1)
        else:
            self.c_layout.removeWidget(self.static_graph)
            self.static_graph = MyMplCanvas(parent=self.w_canvas)
            self.static_graph.mess_to_emit.connect(self._update_status_bar)
            self.c_layout.addWidget(self.static_graph)
            # self.ui.stackedWidget.setCurrentWidget(self.ui.espera)
            self._wait_panel.show()

            data_plate = {
                "sn": p_s,
                "vn": v_n,
                "fp": f_p,
                "xd": r_d,
                "xq": r_q,
                "p_motriz": p,
                "seg_min": p_seg,
                "seg_prac": e_p,
                "ef": t_c_max,
                "per_units": self.liso_pu
            }
            self.static_graph.set_gen(SalientGen(**data_plate),
                                      parent_layout_data=self.ui.graph_data_layout,
                                      parent_frame_data=self.ui.graph_container_data)
            self.thread = DeepThread(self.static_graph)
            self.thread.mess_graph_signal.connect(self._wait_panel.update_message)
            self.thread.im_end.connect(self._plot_finished)
            self.thread.im_end.connect(lambda: self._wait_panel.hide())
            self.thread.start()

    # Función para graficar curva de polos lisos
    @gui_utils.secure_execution
    def _graficar_lisos(self, *args, **kwargs):
        r = self.ui.liso_r_s.text()
        p = self.ui.liso_p_m.text()
        p_s = self.ui.liso_p_aparente.text()
        f_p = self.ui.liso_f_p.text()
        t_c_max = self.ui.liso_t_m_c.text()
        e_p = int(self.ui.liso_estabilidad_practica.currentText())
        v_n = int(self.ui.voltaje_nominal.currentText()) if not self.liso_pu else self.ui.liso_v_nom_pu.text()
        p_seg = int(self.ui.liso_porcentaje_seg.currentText())

        try:
            # Comprueba que los campos no estén vacíos
            if len(r) == 0 or len(p_s) == 0 or len(f_p) == 0:
                GUITemporalMessage(self, "Error al ingresar los datos", "Uno o más campos están vacíos.", 11,
                                   position=1)
                return
            v_n = float(v_n)
            r = float(r)
            p = 0.0 if len(p) == 0 or p == '0' else float(p)
            p_seg = p_seg / 100.0
            p_s = float(p_s)
            f_p = float(f_p)
            t_c_max = None if len(t_c_max) == 0 or t_c_max == '0' or t_c_max == '0.0' else float(t_c_max)
            e_p = e_p / 100.0
        except ValueError:
            GUITemporalMessage(self, "Error al ingresar los datos", "Solo puedes ingresar dígitos en los campos.", 11,
                               position=1)
            return

        # Convierte a todos los valores a números positivos
        r = abs(r)
        p = abs(p)
        p_s = abs(p_s)
        f_p = abs(f_p)
        t_c_max = abs(t_c_max) if t_c_max is not None else None
        v_n = abs(v_n)

        # Actualiza los valores en los campos luego de aplicar valor absoluto
        self.ui.liso_r_s.setText(str(r))
        self.ui.liso_p_m.setText(str(p))
        self.ui.liso_p_aparente.setText(str(p_s))
        self.ui.liso_f_p.setText(str(f_p))
        if self.liso_pu:
            self.ui.liso_v_nom_pu.setText(str(v_n))
        if t_c_max is not None:
            self.ui.liso_t_m_c.setText(str(t_c_max))

        # Comprueba que el Factor de potencia sea correcto
        if f_p >= 1 or f_p <= 0:
            GUITemporalMessage(self, "Error al ingresar los datos",
                               "Ingrese un factor de potencia válido para la máquina.", 11, position=1)
        # Comprueba que, si la p_motriz es distinta de cero, no sea menor que la potencia aparente
        elif p != 0 and p_s < p:
            GUITemporalMessage(self, "Error al ingresar los datos",
                               "La potencia motriz y aparente ingresadas no son correctas.", 11, position=1)
        elif r == 0:
            GUITemporalMessage(self, "Error al ingresar los datos",
                               "La reactancia síncrona debe ser un número mayor a cero.", 11, position=1)
        elif p_s == 0:
            GUITemporalMessage(self, "Error al ingresar los datos",
                               "La potencia aparente debe ser un número mayor a cero.", 11, position=1)
        else:
            self.c_layout.removeWidget(self.static_graph)
            self.static_graph = MyMplCanvas(parent=self.w_canvas)
            self.static_graph.mess_to_emit.connect(self._update_status_bar)
            self.c_layout.addWidget(self.static_graph)
            # self.ui.stackedWidget.setCurrentWidget(self.ui.espera)
            self._wait_panel.show()
            data_plate = {
                "sn": p_s,
                "vn": v_n,
                "fp": f_p,
                "xs": r,
                "p_motriz": p,
                "seg_min": p_seg,
                "seg_prac": e_p,
                "ef": t_c_max,
                "per_units": self.liso_pu
            }
            self.static_graph.set_gen(CylindricalGen(**data_plate),
                                      parent_layout_data=self.ui.graph_data_layout,
                                      parent_frame_data=self.ui.graph_container_data)
            self.thread = DeepThread(self.static_graph)
            self.thread.mess_graph_signal.connect(self._wait_panel.update_message)
            self.thread.im_end.connect(self._plot_finished)
            self.thread.im_end.connect(lambda: self._wait_panel.hide())
            self.thread.start()


class MyMplCanvas(FigureCanvas):
    mess_to_emit = QtCore.pyqtSignal(list)
    _generator = None

    def __init__(self, parent=None, width=40, height=10, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.circle = mpatches.Circle((100, 100), radius=0.015, color='red', alpha=0.7)
        self.axes = self.figure.subplots()
        self.axes.set_xlabel('Per Unit (p.u.)')
        self.axes.set_ylabel('Per Unit (p.u.)')
        self.axes.grid(True)
        self.axes.set_aspect('auto', adjustable='datalim')
        self.axes.add_artist(self.circle)
        self.mpl_connect('button_press_event', self.onClick)
        self.img = Image.open(r'./img/logo.png')
        self.fig.figimage(self.img, xo=0, yo=0, alpha=0.5)

    def _draw_polar_axes(self, factor_y=1 / 2):
        minor_x = round(self._generator.get_width()[0], ndigits=1)
        major_x = round(self._generator.get_width()[1], ndigits=1)
        _x_ticks = np.around(np.linspace(minor_x, major_x, int((major_x - minor_x) * 10) + 1), 1)
        self.axes.set_xticks(list(_x_ticks))
        _y_ticks = np.around(
            np.linspace(0, factor_y * (major_x - minor_x), int(factor_y * (major_x - minor_x) * 10) + 1), 1)
        self.axes.set_yticks(list(_y_ticks))
        self.axes.set_xlim([minor_x - 0.02, major_x + 0.02])
        self.axes.set_ylim([0, factor_y * (major_x - minor_x) + 0.02])

        angle_range = np.arange(-0.9, 1.0, 0.2)
        _x = [minor_x - 1, major_x + 1]

        # Rótulos para las líneas del factor de potencia
        self.axes.text(-0.03, factor_y * (major_x - minor_x) - 0.04, "1.0", bbox={'facecolor': 'white', 'pad': 2})
        for beta in angle_range:
            beta = np.arccos(float(beta))
            self.axes.plot(_x, _x / np.tan(beta), alpha=1, color='k', linewidth=0.6)
            if np.tan(beta) < 0:
                if minor_x / np.tan(beta) < factor_y * (major_x - minor_x):
                    self.axes.text(minor_x + 0.02, minor_x / np.tan(beta), abs(round(np.cos(beta), 2)),
                                   bbox={'facecolor': 'white', 'pad': 2})
                else:
                    self.axes.text(np.tan(beta) * factor_y * (major_x - minor_x), factor_y * (major_x - minor_x) - 0.04,
                                   abs(round(np.cos(beta), 2)), bbox={'facecolor': 'white', 'pad': 2})
            else:
                if major_x / np.tan(beta) < factor_y * (major_x - minor_x):
                    self.axes.text(major_x - 0.1, major_x / np.tan(beta), abs(round(np.cos(beta), 2)),
                                   bbox={'facecolor': 'white', 'pad': 2})
                else:
                    self.axes.text(np.tan(beta) * factor_y * (major_x - minor_x), factor_y * (major_x - minor_x) - 0.04,
                                   abs(round(np.cos(beta), 2)), bbox={'facecolor': 'white', 'pad': 2})

        self.axes.axvline(x=0, color='k', linewidth=0.7)

        # Círcunferencias notables
        for i in np.arange(0.2, 2.2, 0.1):
            self.axes.add_artist(plt.Circle((0, 0), i, fill=False, linewidth=0.7, linestyle='--'))

    @gui_utils.secure_execution
    def onClick(self, event):
        if event.xdata is not None and event.ydata is not None:
            _delta = self._generator.get_load_angle(event.xdata, event.ydata)
            _delta = round(math.degrees(_delta), 3)
            _e_f = self._generator.get_induced_voltage(event.xdata, event.ydata)
            _e_f = round(_e_f, 3)
            self.mess_to_emit.emit([event.xdata, event.ydata, _delta, _e_f])
            self.circle.center = event.xdata, event.ydata
            self.figure.canvas.draw()

    # Clase para graficar la curva
    @gui_utils.secure_execution
    def plot_curve(self, *args, **kwargs):
        self._draw_polar_axes()
        self._plot_function()

    # Asigna un generador al gráfico
    @gui_utils.secure_execution
    def set_gen(self, gen: AbstractGen, parent_layout_data=None, parent_frame_data=None):
        self._generator = gen
        # Quitando labels de la máquina anterior
        while parent_layout_data.count():
            child = parent_layout_data.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Colocando los labels para la nueva máquina
        if parent_layout_data is not None and parent_frame_data is not None:
            if not isinstance(parent_layout_data, QtWidgets.QHBoxLayout) and not isinstance(parent_frame_data,
                                                                                            QtWidgets.QFrame):
                raise AttributeError("The parameters named 'parent_layout_data' and 'parent_frame_data' must be "
                                     "instances of 'QtWidgets.QHBoxLayout' and 'QtWidgets.QFrame', respectively.")
            parent_layout_data.addItem(
                QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))

            param_label = QtWidgets.QLabel(parent_frame_data)
            font = QtGui.QFont()
            font.setPointSize(9)
            font.setBold(True)
            font.setWeight(80)
            param_label.setFont(font)
            font.setFamily("MS Shell Dlg 2")
            param_label.setAlignment(QtCore.Qt.AlignLeft)
            param_label.setText("Datos de placa: ")
            param_label.setAlignment(QtCore.Qt.AlignVCenter)
            parent_layout_data.addWidget(param_label)
            parent_layout_data.addItem(
                QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
            for name, param in gen.get_electric_parameters().items():
                param_label = QtWidgets.QLabel(parent_frame_data)
                font = QtGui.QFont()
                font.setPointSize(9)
                font.setFamily("MS Shell Dlg 2")
                param_label.setFont(font)
                param_label.setAlignment(QtCore.Qt.AlignVCenter)
                if name == "Seg. min.: " or name == "Seg. prac. ":
                    param_label.setText(name + str(round(param, 2) * 100) + "%")
                else:
                    param_label.setText(name + str(round(param, 2)) + "pu")
                parent_layout_data.addWidget(param_label)
                parent_layout_data.addItem(
                    QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))

    @gui_utils.secure_execution
    def _plot_function(self, *args, **kwargs):
        for key, value in self._generator.get_math_model().items():
            self.axes.plot(value[1], value[0].eval_an_array(value[1]), linewidth=1.6, color='k')

    def get_gen(self):
        return self._generator


class DeepThread(QThread):
    mess_graph_signal = QtCore.pyqtSignal(str)
    im_end = QtCore.pyqtSignal(bool)

    def __init__(self, canvas: MyMplCanvas):
        super().__init__()
        self._my_canvas = canvas

    def run(self) -> None:
        # Dibujando los ejes y las curvas
        self.mess_graph_signal.emit("Generando canvas para el renderizado de la gráfica.")
        self._my_canvas.plot_curve()

        # Obtención de la región de operación
        # self.mess_graph_signal.emit("Intersecando límites de la máquina.")
        # intersect = RegionManager.intersect_functions(
        #    self._my_canvas.get_gen().get_only_functions() + [Function(0.001)])
        # self.mess_graph_signal.emit("Obteniendo el contorno que minimiza la potencia.")
        # contour = RegionManager.get_minor_contour(intersect, self._my_canvas.get_gen().get_only_functions())
        # self.mess_graph_signal.emit("Recorriendo los puntos del contorno de mínima potencia.")
        # ordered = RegionManager.run_contour(contour, sentido=-1)
        # if ordered is not None:
        #    self.mess_graph_signal.emit("Pintando la región de operación del generador.")
        #    poly = mpatches.Polygon(RegionManager.make_polygon(ordered, sentido=-1), alpha=0.5)
        #    self._my_canvas.axes.add_patch(poly)

        # Señal de finalización
        self.im_end.emit(True)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main = GUIMain()
    main.show()
    sys.exit(app.exec_())
