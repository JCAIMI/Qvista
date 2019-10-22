# -*- coding: utf-8 -*-

from qgis.PyQt.QtGui import QColor

from qgis.core import QgsGraduatedSymbolRenderer

from qgis.PyQt.QtCore import QLocale

MAP_MAX_CATEGORIES = 10

MAP_ZONES = {
    # Nom: (Camps, Arxiu)
    "Districte": ("DISTRICTE", "Districtes.sqlite"),
    "Barri": ("BARRI", "Barris.sqlite")
    # "Codi postal": "CODI_POSTAL",
    # "Illa": "ILLA",
    # "Solar": "SOLAR",
    # "Àrea estadística bàsica": "AEB",
    # "Secció censal": "SECCIO_CENSAL",
    # "Sector policial operatiu": "SPO"
}

MAP_ZONES_COORD = MAP_ZONES.copy()
MAP_ZONES_COORD["Coordenada"] = (("ETRS89_COORD_X", "ETRS89_COORD_Y"), "")

MAP_AGREGACIO = {
    "Recompte": "COUNT({})",
    "Recompte diferents": "COUNT(DISTINCT {})",
    "Suma": "SUM({})",
    "Mitjana": "AVG({})"
}

MAP_DISTRIBUCIO = {
    "Total": "",
    "Per m2": "/ AREA"
    # "Per habitant": "/ POBLACIO"
}

MAP_COLORS = {
    "Blau": QColor(0, 128, 255),
    "Gris": QColor(128, 128, 128),
    "Groc" : QColor(255, 192, 0),
    "Taronja": QColor(255, 128, 0),
    "Verd" : QColor(32, 160, 32),
    "Vermell" : QColor(255, 32, 32)
}

MAP_METODES = {
    "Endreçat": QgsGraduatedSymbolRenderer.Pretty,
    "Intervals equivalents": QgsGraduatedSymbolRenderer.EqualInterval,
    "Quantils": QgsGraduatedSymbolRenderer.Quantile,
    "Divisions naturals (Jenks)": QgsGraduatedSymbolRenderer.Jenks,
    "Desviació estàndard": QgsGraduatedSymbolRenderer.StdDev
}

MAP_METODES_MODIF = MAP_METODES.copy()
MAP_METODES_MODIF["Personalitzat"] = QgsGraduatedSymbolRenderer.Custom

MAP_LOCALE = QLocale(QLocale.Catalan, QLocale.Spain)

if __name__ == "__main__":

    from qgis.core.contextmanagers import qgisapp

    gui = False

    with qgisapp(guienabled=gui) as app:

        for nom, col in MAP_COLORS.items():
            print(nom, col.name())
