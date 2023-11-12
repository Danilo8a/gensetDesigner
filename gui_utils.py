import datetime
import traceback
from datetime import date

import winsound
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, Table, TableStyle, PageBreak, SimpleDocTemplate
from gui_elements import GUIBaseDialog, MotorCardListElement, NonLinealCardListElement
from FunctionPoints import FunctionPoints
from numpy import arange
import cmath
import json


_temp_curve = FunctionPoints(
    [30, 40, 45, 50, 55, 60, 70, 80],
    [1.07, 1, 0.965, 0.93, 0.9, 0.865, 0.79, 0.7]
)

_altitude_curve = FunctionPoints(
    [int(i) for i in arange(1000, 4500, 500)],
    [1, 0.96, 0.92, 0.88, 0.84, 0.8, 0.76]
)

_fp_power_factor_curve = FunctionPoints(
    [round(i, 2) for i in arange(0.1, 1, 0.1)],
    [1, 1, 1, 1, 0.97, 0.93, 0.9, 0.85, 0.83]
)


def secure_execution(function):
    def wrapper(*args, **kwargs):
        try:
            value = function(*args, **kwargs)
            return value
        except Exception as e:
            aux_dialog = GUIBaseDialog(None, GUIBaseDialog.SET_ICON_DIALOG_ERROR)
            aux_dialog.setDialogMessTitle("Ha ocurrido un problema al ejecutar la acción.")
            aux_dialog.setDialogMessInformation("A continuación, se adjunta la excepción generada. Presione 'ok' para "
                                                "enviar la información del problema al desarrollador.")
            txt = "Argumentos de la función:\n" \
                  "Args: "
            for arg in args:
                txt += str(type(arg)) + ", "
            txt += "\nKwargs: "
            for kwarg in kwargs:
                txt += str(type(kwarg))
            txt += "\nTraceback:\n" + "".join(traceback.format_tb(e.__traceback__))
            aux_dialog.set_plain_mess(txt)
            winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
            aux_dialog.exec()

    return wrapper


def time_execution(funcion):
    def wrapper(*args, **kwargs):
        init_time = datetime.datetime.now()
        funcion(*args, **kwargs)
        final_time = datetime.datetime.now()
        print(final_time -init_time)

    return wrapper


def derating_temperature_factor(temp):
    aux_out = 0
    if temp < 30:
        aux_out = 1
    else:
        aux_out = round(float(_temp_curve.eval(temp)), 2)
    return aux_out


def derating_altitude_factor(altitude):
    aux_out = 0
    if altitude < 1000:
        aux_out = 1
    else:
        aux_out = round(float(_altitude_curve.eval(altitude)), 2)
    return aux_out


def correction_factor_power(fp):
    if fp > 0.83:
        fp = 0.83
    elif fp < 0.1:
        fp = 0.2
    return round(float(_fp_power_factor_curve.eval(fp)), 2)


# """ Es importante saber que este cálculo no toma en cuenta
#         el proceso de filtro
# cargas es igual """
def THD_Calculated(cargas, max_steps, xd, KVA_generator):

    THDV_total = {}
    THDV = {}
    cargas_steps = {}
    suma_kw = 0
    suma_kvar = 0

    # se crea el diccionario que contiene los armonicos por pasos
    for step in range(1, max_steps + 1):
        THDV_total[step] = {}
        for number in range(1, 26):
            THDV_total[step][number] = 0
    # se resorre la lista de cargas con el fin de obtener las xd por pasos
    """
        cargas_steps = {
            1: [kW, kVAR],
            ...
        }
    """

    for carga in cargas:
        paso = carga.get_step()
        kw = carga.get_apparent_power()["power_run"]
        kvar = carga.get_apparent_power()["reactive_run"]
        if paso not in cargas_steps: cargas_steps[paso] = [0, 0]
        cargas_steps[paso][0] += kw
        cargas_steps[paso][1] += kvar

    cargas_steps = dict(sorted(cargas_steps.items(), key=lambda x: x[0]))
    # ya con diccionario ordenado por pasos se suman las potencias  para ir acumulando
    """
        cargas_steps = {
            1: kVA -> (float),
            ...
        }
    """
    for key, values in cargas_steps.items():
        suma_kw += values[0]
        suma_kvar += values[1]
        cargas_steps[key] = abs(cmath.sqrt(suma_kw ** 2 + suma_kvar ** 2))
    """
        cargas_steps = {
            1: xd_new -> (float),
            ...
        }
    """
    print(cargas_steps)
    # se obtiene el diccionario con las reactancias nuevas por las potencias
    for reactancias in cargas_steps:
        cargas_steps[reactancias] = (cargas_steps[reactancias] / KVA_generator) * xd
    # se recorre nuevamente la lista de cargas para obtener su thdv
    # aqui se piden el valor de paso y pulso
    for carga in cargas:
        if isinstance(carga, NonLinealCardListElement):
            paso = carga.get_step()
            pulso = carga.get_values()["Pulsos"]

        elif isinstance(carga, MotorCardListElement):
            paso = carga.get_values()["Step"]
            pulso = carga.get_values()["VFD"]
        # se pregunta por pulso para saber que ármonicos afectan
        if pulso == 4:  # pregunto por pulso
            harmonics = (3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25)
        elif pulso == 6:
            harmonics = (5, 7, 11, 13, 17, 19, 23, 25)
        elif pulso == 12:
            harmonics = (11, 13, 23, 25)
        elif pulso == 24:
            harmonics = (23, 25)
        # se obtiene el total de los armonicos por cada paso
        for HDI in harmonics:
            THDV_total[paso][HDI] += ((1 / HDI) * HDI * cargas_steps[paso])
    # aqui se suma los cuadrados de cada armonico y se saca la raiz
    for THD in THDV_total:
        aux = 0
        for distortions in THDV_total[THD]:
            aux += (THDV_total[THD][distortions]) ** 2
        THDV[THD] = abs(cmath.sqrt(aux)) * 100


    return THDV


def Crear_Reporte(data_dict, voltage_dip, distortion_Harmonic, genset_loaded,kva_rp_valor,carga, kva_rp, arranques, volt, nombre, usuario, dict_ord, maquina):

    # Datos de las tablas en diccionarios
    descripcion_proyecto = {
        "Fila 1": ["Nombre del proyecto:", data_dict["name"]],
        "Fila 2": ["Descripción:", data_dict["Descripcion"]],
        "Fila 3": ["Contacto: ", data_dict["Contacto"]]
    }

    tabla2 = {
        "Fila 1": ["Voltaje:", str(data_dict["voltaje"]), "Combustible:", str(data_dict["combustible"])],
        "Fila 2": ["Fases:", str(data_dict["fases"]), "Ciclo de trabajo:", str(data_dict["ciclo_trabajo"])],
        "Fila 3": ["Frecuencia:", str(data_dict["frecuencia"]), "ISO 8528:", str(data_dict["ISO_8528"])],
        "Fila 4": ["Altitud:", str(data_dict["altura"]), "Max Ambiente Temp:", str(data_dict["temperatura"])],

    }

    tabla3 = {
        "Fila 1": [" Limite Volt-Dip %:", str(data_dict["voltaje_dip"]), "Volt-Dip %:", str(voltage_dip)],
        "Fila 2": ["Limite THD %:", str(data_dict["THD"]), "THD %:", str(distortion_Harmonic)],
        "Fila 3": ["Max Genset carga:", "90 %", "Carga del Genset %", str(genset_loaded)],
        "Fila 4": ["Min Genset carga:", "25 %", "carga en regimem permanente:", str(kva_rp_valor)]
    }

    tabla4 ={
        "Fila 5": ["Modelo:", str(maquina[7]), "Fabricante:", str(maquina[6])],
        "fila 6": ["Potencia:", str(maquina[5]) + "kVA", "ID base de dato:", str(maquina[0])]

    }

    # Crear el documento PDF
    doc = SimpleDocTemplate(nombre, pagesize=letter)

    # Contenido del reporte
    contenido = []
    fecha_actual = date.today().strftime("%d/%m/%Y")
    estilo_centro = getSampleStyleSheet()["Normal"]
    estilo_centro.alignment = 1  # 0: Izquierda, 1: Centro, 2: Derecha

    # Agregar imagen como encabezado
    Encabezado = Paragraph(f"- <img src='./img/logo_1.png' width='90%' height='80'></img>", estilo_centro)

    page_width, page_height = letter

    tabla1_data = [
        [Paragraph("Información del proyecto", getSampleStyleSheet()["Title"])],
        [Paragraph(descripcion_proyecto["Fila 1"][0], getSampleStyleSheet()["Normal"]),
         Paragraph(descripcion_proyecto["Fila 1"][1], getSampleStyleSheet()["Normal"])],
        [Paragraph(descripcion_proyecto["Fila 2"][0], getSampleStyleSheet()["Normal"]),
         Paragraph(descripcion_proyecto["Fila 2"][1], getSampleStyleSheet()["Normal"])],
        [Paragraph(descripcion_proyecto["Fila 3"][0], getSampleStyleSheet()["Normal"]),
         Paragraph(descripcion_proyecto["Fila 3"][1], getSampleStyleSheet()["Normal"])],

    ]
    tabla1 = Table(tabla1_data, colWidths=[2 * inch, 5 * inch])
    tabla1.setStyle(TableStyle([
        ('SPAN', (0, 0), (-1, 0)),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.lightblue),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Alinear verticalmente al centro
        ('WORDWRAP', (0, 0), (-1, -1))  # Ajustar el texto dentro de las celdas
    ]))

    # Tabla 2
    tabla2_data = [
        [Paragraph("Requerimientos del sistema", getSampleStyleSheet()["Title"])],
        [Paragraph(tabla2["Fila 1"][0], getSampleStyleSheet()["Normal"]),
         Paragraph(tabla2["Fila 1"][1], getSampleStyleSheet()["Normal"]),
         Paragraph(tabla2["Fila 1"][2], getSampleStyleSheet()["Normal"]),
         Paragraph(tabla2["Fila 1"][3], getSampleStyleSheet()["Normal"])
         ],
        [Paragraph(tabla2["Fila 2"][0], getSampleStyleSheet()["Normal"]),
         Paragraph(tabla2["Fila 2"][1], getSampleStyleSheet()["Normal"]),
         Paragraph(tabla2["Fila 2"][2], getSampleStyleSheet()["Normal"]),
         Paragraph(tabla2["Fila 2"][3], getSampleStyleSheet()["Normal"])
         ],
        [Paragraph(tabla2["Fila 3"][0], getSampleStyleSheet()["Normal"]),
         Paragraph(tabla2["Fila 3"][1], getSampleStyleSheet()["Normal"]),
         Paragraph(tabla2["Fila 3"][2], getSampleStyleSheet()["Normal"]),
         Paragraph(tabla2["Fila 3"][3], getSampleStyleSheet()["Normal"])
         ],
        [Paragraph(tabla2["Fila 4"][0], getSampleStyleSheet()["Normal"]),
         Paragraph(tabla2["Fila 4"][1], getSampleStyleSheet()["Normal"]),
         Paragraph(tabla2["Fila 4"][2], getSampleStyleSheet()["Normal"]),
         Paragraph(tabla2["Fila 4"][3], getSampleStyleSheet()["Normal"]),
         ]
    ]
    tabla2 = Table(tabla2_data, colWidths=[2 * inch, 1.5 * inch, 2 * inch, 1.5 * inch])
    tabla2.setStyle(TableStyle([
        ('SPAN', (0, 0), (-1, 0)),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 0), (1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.lightblue),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Alinear verticalmente al centro
        ('WORDWRAP', (0, 0), (-1, -1))  # Ajustar el texto dentro de las celdas
        #('SPAN', (0, 5), (-1, 5)),
        #('BACKGROUND', (0, 5), (-1, 5), colors.lightgrey)
    ]))
    tabla4_data = [
        [Paragraph("Generador seleccionado ", getSampleStyleSheet()["Title"])],
        [Paragraph(tabla4["Fila 5"][0], getSampleStyleSheet()["Normal"]),
         Paragraph(tabla4["Fila 5"][1], getSampleStyleSheet()["Normal"]),
         Paragraph(tabla4["Fila 5"][2], getSampleStyleSheet()["Normal"]),
         Paragraph(tabla4["Fila 5"][3], getSampleStyleSheet()["Normal"])
         ],
        [Paragraph(tabla4["fila 6"][0], getSampleStyleSheet()["Normal"]),
         Paragraph(tabla4["fila 6"][1], getSampleStyleSheet()["Normal"]),
         Paragraph(tabla4["fila 6"][2], getSampleStyleSheet()["Normal"]),
         Paragraph(tabla4["fila 6"][3], getSampleStyleSheet()["Normal"])
         ]
    ]
    tabla4 = Table(tabla4_data, colWidths=[2 * inch, 1.5 * inch, 2 * inch, 1.5 * inch])

    tabla4.setStyle(TableStyle([
        ('SPAN', (0, 0), (-1, 0)),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 0), (1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.lightblue),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Alinear verticalmente al centro
        ('WORDWRAP', (0, 0), (-1, -1))  # Ajustar el texto dentro de las celdas
        ]))

    # Tabla 3
    tabla3_data = [
        [Paragraph("Resumen de análisis de carga", getSampleStyleSheet()["Title"])],
        [Paragraph(tabla3["Fila 1"][0], getSampleStyleSheet()["Normal"]),
         Paragraph(tabla3["Fila 1"][1], getSampleStyleSheet()["Normal"]),
         Paragraph(tabla3["Fila 1"][2], getSampleStyleSheet()["Normal"]),
         Paragraph(tabla3["Fila 1"][3], getSampleStyleSheet()["Normal"])
         ],
        [Paragraph(tabla3["Fila 2"][0], getSampleStyleSheet()["Normal"]),
         Paragraph(tabla3["Fila 2"][1], getSampleStyleSheet()["Normal"]),
         Paragraph(tabla3["Fila 2"][2], getSampleStyleSheet()["Normal"]),
         Paragraph(tabla3["Fila 2"][3], getSampleStyleSheet()["Normal"])
         ],
        [Paragraph(tabla3["Fila 3"][0], getSampleStyleSheet()["Normal"]),
         Paragraph(tabla3["Fila 3"][1], getSampleStyleSheet()["Normal"]),
         Paragraph(tabla3["Fila 3"][2], getSampleStyleSheet()["Normal"]),
         Paragraph(tabla3["Fila 3"][3], getSampleStyleSheet()["Normal"])
         ]
    ]
    tabla3 = Table(tabla3_data, colWidths=[2 * inch, 1.5 * inch, 2 * inch, 1.5 * inch])
    tabla3.setStyle(TableStyle([
        ('SPAN', (0, 0), (-1, 0)),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.lightblue),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Alinear verticalmente al centro
        ('WORDWRAP', (0, 0), (-1, -1)),  # Ajustar el texto dentro de las celdas
        ('ROWHEIGHT', (0, 1), (-1, -1), 15),  # Ajustar la altura de todas las filas a 30 puntos
    ]))
    # Agregar espacio entre las tablas
    separador_color = colors.HexColor("#9dbfe7")  # Color azul en formato hexadecimal
    separador_data = [[""]]
    separador = Table(separador_data, colWidths=[7 * inch])
    separador.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), separador_color),
        ('LINEBELOW', (0, 0), (-1, -1), 1, colors.white),
    ]))

    espacio_entre_tablas = Paragraph("<br/><br/>", getSampleStyleSheet()["Normal"])

    # Agregar tablas al contenido
    contenido.append(Encabezado)
    contenido.append(separador)
    contenido.append(espacio_entre_tablas)
    contenido.append(tabla1)
    contenido.append(espacio_entre_tablas)
    contenido.append(tabla2)
    contenido.append(espacio_entre_tablas)
    contenido.append(tabla4)
    contenido.append(espacio_entre_tablas)
    contenido.append(tabla3)
    contenido.append(espacio_entre_tablas)
    contenido.append(separador)

    # Estilo para el contenido centrado

    # Agregar pie de página
    pie_pagina = Paragraph(f"- <img src='./img/logo.png' width='70%' height='60'></img>  ", estilo_centro)
    contenido.append(separador)
    contenido.append(pie_pagina)
    contenido.append(Paragraph(f"Reporte realizado por:  {usuario}", estilo_centro))
    fecha = Paragraph(f"{fecha_actual}", estilo_centro)
    contenido.append(fecha)
    contenido.append(PageBreak())

    # Tabla1 pagina 2
    # Datos de las tablas en diccionarios
    Tabla1_2 = {
        "Fila 2": ["Paso", "Descripcion", "Tipo de Arranque", "Marcha", "Arranque", "Volt Dip%"],
        "Fila 3": ["", "kW", "kVA "]}
    tabla_page_data = [
        [Paragraph("Perfiles de cargas", getSampleStyleSheet()["Title"])],
        [Paragraph(Tabla1_2["Fila 2"][0], getSampleStyleSheet()["Normal"]),
         Paragraph(Tabla1_2["Fila 2"][1], getSampleStyleSheet()["Normal"]),
         Paragraph(Tabla1_2["Fila 2"][2], getSampleStyleSheet()["Normal"]),
         Paragraph(Tabla1_2["Fila 2"][3], getSampleStyleSheet()["Normal"]),
         Paragraph(Tabla1_2["Fila 2"][3], getSampleStyleSheet()["Normal"]),
         Paragraph(Tabla1_2["Fila 2"][4], getSampleStyleSheet()["Normal"]),
         Paragraph(Tabla1_2["Fila 2"][4], getSampleStyleSheet()["Normal"]),
         Paragraph(Tabla1_2["Fila 2"][5], getSampleStyleSheet()["Normal"])
         ],
        [Paragraph(Tabla1_2["Fila 3"][0], getSampleStyleSheet()["Normal"]),
         Paragraph(Tabla1_2["Fila 3"][0], getSampleStyleSheet()["Normal"]),
         Paragraph(Tabla1_2["Fila 3"][0], getSampleStyleSheet()["Normal"]),
         Paragraph(Tabla1_2["Fila 3"][1], getSampleStyleSheet()["Normal"]),
         Paragraph(Tabla1_2["Fila 3"][2], getSampleStyleSheet()["Normal"]),
         Paragraph(Tabla1_2["Fila 3"][1], getSampleStyleSheet()["Normal"]),
         Paragraph(Tabla1_2["Fila 3"][2], getSampleStyleSheet()["Normal"]),
         Paragraph(Tabla1_2["Fila 3"][0], getSampleStyleSheet()["Normal"])]
    ]
    tabla_page2 = Table(tabla_page_data,
                        colWidths=[0.5 * inch, 3 * inch, 0.9 * inch, 0.7 * inch, 0.7 * inch, 0.7 * inch, 0.7 * inch,
                                   0.7 * inch])
    tabla_page2.setStyle(TableStyle([
        ('SPAN', (0, 0), (7, 0)),
        ('SPAN', (3, 1), (4, 1)),
        ('SPAN', (5, 1), (6, 1)),
        ('SPAN', (0, 1), (0, 2)),
        ('SPAN', (1, 1), (1, 2)),
        ('SPAN', (2, 1), (2, 2)),
        ('SPAN', (7, 1), (7, 2)),
        ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, -1), 16),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Alinear verticalmente al centro
        ('WORDWRAP', (0, 0), (-1, -1)),  # Ajustar el texto dentro de las celdas
        ('ROWHEIGHT', (0, 1), (-1, -1), 15),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.white)

    ]))
    contenido.append(tabla_page2)
    generar_tabla_cargas(carga, kva_rp, contenido, arranques, volt, dict_ord)
    # Construir el documento PDF
    doc.build(contenido)


def generar_tabla_cargas(carga, kva_rp, contenido, kva_rt, volt, dict_ord):
    aux = 0
    for carga_data in carga.keys():

        for j in carga[carga_data]:

            if isinstance(j["kW_start"], float): j["kW_start"] = round(j["kW_start"],2)
            if isinstance(j["kVA_start"], float): j["kVA_start"] = round(j["kVA_start"], 2)

            loads_data = [
                [Paragraph(str(j["step"]), getSampleStyleSheet()["Normal"]),
                 Paragraph(str(j["Description"]), getSampleStyleSheet()["Normal"]),
                 Paragraph(str(j['starting type']), getSampleStyleSheet()["Normal"]),
                 Paragraph(str(round(j["kW"], 2)), getSampleStyleSheet()["Normal"]),
                 Paragraph(str(round(j["kVA"],2)), getSampleStyleSheet()["Normal"]),
                 Paragraph(str(j['kW_start']), getSampleStyleSheet()["Normal"]),
                 Paragraph(str(j['kVA_start']), getSampleStyleSheet()["Normal"]),
                 Paragraph(str(j["Volt_dip"]), getSampleStyleSheet()["Normal"])]
            ]

            tabla_cargas = Table(loads_data,
                                 colWidths=[0.5 * inch, 3 * inch, 0.9 * inch, 0.7 * inch, 0.7 * inch, 0.7 * inch,
                                            0.7 * inch, 0.7 * inch])

            tabla_cargas.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.white),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Times-Roman'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.lightblue),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('WORDWRAP', (0, 0), (-1, -1)),
                ('ROWHEIGHT', (0, 1), (-1, -1), 15)
            ]))

            contenido.append(tabla_cargas)

        totales_data = [
            [Paragraph(str(carga_data), getSampleStyleSheet()["Normal"]),
             Paragraph(("Total"), getSampleStyleSheet()["Normal"]),
             Paragraph(("---"), getSampleStyleSheet()["Normal"]),
             Paragraph(str(round(dict_ord[carga_data]['power_run'], 2)), getSampleStyleSheet()["Normal"]),
             Paragraph(str(round(
                 abs(cmath.sqrt((dict_ord[carga_data]['power_run']) ** 2 + (dict_ord[carga_data]['reactive_run']) ** 2)), 2)), getSampleStyleSheet()["Normal"]),
             Paragraph(str(round(dict_ord[carga_data]['power_star'], 2)), getSampleStyleSheet()["Normal"]),
             Paragraph(str(round(abs(cmath.sqrt((dict_ord[carga_data]['power_star']) ** 2 + (dict_ord[carga_data]['reactive_star']) ** 2)), 2)), getSampleStyleSheet()["Normal"]),
             Paragraph(("---"), getSampleStyleSheet()["Normal"])]]
        totales = Table(totales_data,
                        colWidths=[0.5 * inch, 3 * inch, 0.9 * inch, 0.7 * inch, 0.7 * inch, 0.7 * inch, 0.7 * inch,
                                   0.7 * inch])
        totales.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.white),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Times-Roman'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.lightblue),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('WORDWRAP', (0, 0), (-1, -1)),
            ('ROWHEIGHT', (0, 1), (-1, -1), 15)
        ]))
        contenido.append(totales)
        acumulate_data = [
            [Paragraph(str(carga_data), getSampleStyleSheet()["Normal"]),
             Paragraph(("Total acumulado"), getSampleStyleSheet()["Normal"]),
             Paragraph(("---"), getSampleStyleSheet()["Normal"]),
             Paragraph(str(round(dict_ord[carga_data]['p_marcha'], 2)), getSampleStyleSheet()["Normal"]),
             Paragraph(str(round(dict_ord[carga_data]['kva_marcha'], 2)), getSampleStyleSheet()["Normal"]),
             Paragraph(str(round(dict_ord[carga_data]['p_arr'], 2)), getSampleStyleSheet()["Normal"]),
             Paragraph(str(round(kva_rt[carga_data], 2)), getSampleStyleSheet()["Normal"]),
             Paragraph(str(round(volt[carga_data - 1], 2)), getSampleStyleSheet()["Normal"])]]
        acumulate = Table(acumulate_data,
                          colWidths=[0.5 * inch, 3 * inch, 0.9 * inch, 0.7 * inch, 0.7 * inch, 0.7 * inch, 0.7 * inch,
                                     0.7 * inch])
        acumulate.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Times-Roman'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.lightblue),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('WORDWRAP', (0, 0), (-1, -1)),
            ('ROWHEIGHT', (0, 1), (-1, -1), 15)
        ]))
        contenido.append(acumulate)


def package_project(data_dict: dict, loads_list: list, name: str):
    aux_package = []
    for i in loads_list:
        aux_package.append(i.get_data_for_package())

    aux_for_dump = {
        "data_project": data_dict,
        "serializate_list": aux_package
    }

    with open(name, "w") as f:
        json.dump(aux_for_dump, f)


if __name__ == '__main__':
    print(derating_temperature_factor(40))
    print(derating_altitude_factor(1200))
