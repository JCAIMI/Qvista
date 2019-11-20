# -*- coding: utf-8 -*-

from qgis.PyQt.QtGui import QColor
from qgis.core import QgsGraduatedSymbolRenderer
from qgis.PyQt.QtCore import QLocale
from collections import OrderedDict

from configuracioQvista import *

MAP_ID = "qV_mapificacio"
MAP_MAX_CATEGORIES = 10
MAP_ALPHA_INI = 4
MAP_ALPHA_FIN = 28
MAP_ZONES_DB = "Zones.gpkg"

MAP_ZONES = OrderedDict({
    # Nom: (Camps, Taula)
    "Districte": ("DISTRICTE", "districtes"),
    "Barri": ("BARRI", "barris"),
    "Codi postal": ("CODI_POSTAL", ""),
    "Illa": ("ILLA", "illes"),
    "Solar": ("SOLAR", ""),
    "Àrea estadística bàsica": ("AEB", "aeb"),
    "Secció censal": ("DISTRICTE || SECCIO_CENSAL AS SECCIO_CENSAL", "seccions_censals"),
    "Sector policial operatiu": ("SPO", "")
})

MAP_ZONES_COORD = OrderedDict({
    "Coordenada": (("ETRS89_COORD_X", "ETRS89_COORD_Y"), ""),
    **MAP_ZONES
})

MAP_AGREGACIO = OrderedDict({
    "Recompte": "COUNT({})",
    "Recompte diferents": "COUNT(DISTINCT {})",
    "Suma": "SUM({})",
    "Mitjana": "AVG({})"
})

MAP_DISTRIBUCIO = OrderedDict({
    "Total": "",
    "Per m2": "AREA",
    "Per habitant": "POBLACIO"
})

MAP_COLORS = OrderedDict({
    "Blau": QColor(0, 128, 255),
    "Gris": QColor(128, 128, 128),
    "Groc" : QColor(255, 192, 0),
    "Porpra" : QColor(156, 41, 161),
    "Taronja": QColor(255, 128, 0),
    "Verd" : QColor(32, 160, 32),
    "Vermell" : QColor(255, 32, 32)
})

MAP_METODES = OrderedDict({
    "Endreçat": QgsGraduatedSymbolRenderer.Pretty,
    "Intervals equivalents": QgsGraduatedSymbolRenderer.EqualInterval,
    "Quantils": QgsGraduatedSymbolRenderer.Quantile,
    "Divisions naturals (Jenks)": QgsGraduatedSymbolRenderer.Jenks
    # "Desviació estàndard": QgsGraduatedSymbolRenderer.StdDev
})

MAP_METODES_MODIF = OrderedDict({
    **MAP_METODES,
    "Personalitzat": QgsGraduatedSymbolRenderer.Custom
})

MAP_LOCALE = QLocale(QLocale.Catalan, QLocale.Spain)

if __name__ == "__main__":

    from qgis.core.contextmanagers import qgisapp

    gui = False

    with qgisapp(guienabled=gui) as app:

        print('MAP_COLORS:')
        for nom, col in MAP_COLORS.items():
            print(nom, col.name())
        print('---')
        print('MAP_ZONES_COORD:')
        for nom in MAP_ZONES_COORD.keys():
            print(nom)
        print('---')
        print('MAP_METODES_MODIF:')
        for nom in MAP_METODES_MODIF.keys():
            print(nom)
