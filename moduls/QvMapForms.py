# -*- coding: utf-8 -*-

from qgis.gui import QgsFileWidget
from qgis.PyQt.QtCore import Qt, QObject, pyqtSignal, pyqtSlot
from qgis.PyQt.QtGui import QColor, QValidator, QIcon, QDoubleValidator, QPixmap
from qgis.PyQt.QtWidgets import (QFileDialog, QWidget, QPushButton, QFormLayout, QVBoxLayout, QHBoxLayout,
                                 QComboBox, QLabel, QLineEdit, QSpinBox, QGroupBox, QGridLayout, QDialog,
                                 QMessageBox, QDialogButtonBox, QApplication)

from qgis.core import QgsApplication, QgsGraduatedSymbolRenderer, QgsExpressionContextUtils

from moduls.QvMapVars import *
from moduls.QvMapificacio import *

import os
import sqlite3

class QvFormBaseMapificacio(QDialog):
    def __init__(self, llegenda, amplada=None, parent=None, modal=True):
        super().__init__(parent, modal=modal)
        self.llegenda = llegenda
        if amplada is not None:
            self.setMinimumWidth(amplada)
            self.setMaximumWidth(amplada)
        self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint)

    def msgInfo(self, txt):
        QMessageBox.information(self, 'Informació', txt)

    def msgAvis(self, txt):
        QMessageBox.warning(self, 'Avís', txt)

    def msgError(self, txt):
        QMessageBox.critical(self, 'Error', txt)

    def pause(self):
        QApplication.instance().setOverrideCursor(Qt.WaitCursor)
        self.setDisabled(True)

    def play(self):
        self.setDisabled(False)
        QApplication.instance().restoreOverrideCursor()

    def comboColors(self, combo):
        for nom, col in MAP_COLORS.items():
            pixmap = QPixmap(80, 45)
            pixmap.fill(col)
            icon = QIcon(pixmap)
            combo.addItem(icon, nom)

    def valida(self):
        return True

    def mapifica(self):
        return ''

    @pyqtSlot()
    def accept(self):
        if self.valida():
            self.pause()
            msg = self.mapifica()
            if msg == '':
                self.play()
                super().accept()
            else:
                self.play()
                self.msgError(msg)

    @pyqtSlot()
    def cancel(self):
        self.close()

class QvVerifNumero(QValidator):

    def verifCharsNumero(self, string):
        for char in string:
            if char.isdigit() or char in ('.', ',', '-'):
                pass
            else:
                return False
        return True

    def validate(self, string, index):
        txt = string.strip()
        num, ok = MAP_LOCALE.toFloat(txt)
        if ok:
            state = QValidator.Acceptable
        elif self.verifCharsNumero(txt):
            state = QValidator.Intermediate
        else:
            state = QValidator.Invalid
        return (state, string, index)

class QvComboBoxEdited(QComboBox):
    def __init__(self, parent):
        super().__init__(parent)
        self.setEditable(True)
        self.setInsertPolicy(QComboBox.NoInsert)
        self.oldText = ''
        self.newText = ''
        self.editTextChanged.connect(self.copyText)
        self.activated.connect(self.copyItem)

    def setItems(self, items):
        self.addItems(items)
        self.setCurrentIndex(-1)
        self.setCurrentText('')

    @pyqtSlot(str)
    def copyText(self, txt):
        self.oldText = self.newText
        self.newText = txt

    @pyqtSlot(int)
    def copyItem(self, i):
        if i == -1:
            return
        txt = self.oldText
        self.item = self.currentText()
        lenItem = len(self.item)
        if txt.rstrip().upper().endswith(self.item.upper()):
            txt = txt.rstrip()
            txt = txt[0:len(txt)-lenItem] + self.item
        else:
            if txt != '' and txt[-1] != ' ':
                txt += ' '
            txt += self.item
        self.setCurrentText(txt)
        self.lineEdit().setSelection(len(txt) - lenItem, lenItem)

class QvFormNovaMapificacio(QvFormBaseMapificacio):
    def __init__(self, llegenda, amplada=450, mapificacio=None):
        super().__init__(llegenda, amplada)

        self.fCSV = mapificacio

        self.setWindowTitle('Afegir capa de mapificació')

        self.layout = QVBoxLayout()
        self.layout.setSpacing(14)
        self.setLayout(self.layout)

        if self.fCSV is None:
            self.arxiu = QgsFileWidget()
            self.arxiu.setStorageMode(QgsFileWidget.GetFile)
            self.arxiu.setDialogTitle('Selecciona fitxer de dades…')
            self.arxiu.setDefaultRoot(RUTA_LOCAL)
            self.arxiu.setFilter('Arxius CSV (*.csv)')
            self.arxiu.setSelectedFilter('Arxius CSV (*.csv)')
            self.arxiu.lineEdit().setReadOnly(True)
            self.arxiu.fileChanged.connect(self.arxiuSeleccionat)

        self.zona = QComboBox(self)
        self.zona.setEditable(False)
        self.zona.addItem('Selecciona zona…')
        self.zona.currentIndexChanged.connect(self.canviaZona)

        self.capa = QLineEdit(self)
        self.capa.setMaxLength(40)

        self.tipus = QComboBox(self)
        self.tipus.setEditable(False)
        self.tipus.addItem('Selecciona tipus…')
        self.tipus.addItems(MAP_AGREGACIO.keys())

        self.distribucio = QComboBox(self)
        self.distribucio.setEditable(False)
        self.distribucio.addItem(next(iter(MAP_DISTRIBUCIO.keys())))

        self.calcul = QvComboBoxEdited(self)

        self.filtre = QvComboBoxEdited(self)

        self.color = QComboBox(self)
        self.color.setEditable(False)
        self.comboColors(self.color)

        self.metode = QComboBox(self)
        self.metode.setEditable(False)
        self.metode.addItems(MAP_METODES.keys())

        self.intervals = QSpinBox(self)
        self.intervals.setMinimum(2)
        self.intervals.setMaximum(MAP_MAX_CATEGORIES)
        self.intervals.setSingleStep(1)
        self.intervals.setValue(4)
        self.intervals.setSuffix("  (depèn del mètode)")
        # self.intervals.valueChanged.connect(self.deselectValue)

        self.buttons = QDialogButtonBox()
        self.buttons.addButton(QDialogButtonBox.Ok)
        self.buttons.accepted.connect(self.accept)
        self.buttons.addButton(QDialogButtonBox.Cancel)
        self.buttons.rejected.connect(self.cancel)

        self.gZona = QGroupBox('Definició zona')
        self.lZona = QFormLayout()
        self.lZona.setSpacing(14)
        self.gZona.setLayout(self.lZona)

        if self.fCSV is None:
            self.lZona.addRow('Arxiu dades:', self.arxiu)
        self.lZona.addRow('Zona:', self.zona)
        self.lZona.addRow('Nom capa:', self.capa)

        self.gDades = QGroupBox('Dades agregació')
        self.lDades = QFormLayout()
        self.lDades.setSpacing(14)
        self.gDades.setLayout(self.lDades)

        self.lDades.addRow('Tipus agregació:', self.tipus)
        self.lDades.addRow('Camp o fòrmula càlcul:', self.calcul)
        self.lDades.addRow('Filtre:', self.filtre) 
        self.lDades.addRow('Distribució:', self.distribucio)

        self.gSimb = QGroupBox('Simbologia mapificació')
        self.lSimb = QFormLayout()
        self.lSimb.setSpacing(14)
        self.gSimb.setLayout(self.lSimb)

        self.lSimb.addRow('Color mapa:', self.color)
        self.lSimb.addRow('Mètode classificació:', self.metode)
        self.lSimb.addRow('Nombre intervals:', self.intervals)

        self.layout.addWidget(self.gZona)
        self.layout.addWidget(self.gDades)
        self.layout.addWidget(self.gSimb)
        self.layout.addWidget(self.buttons)

        self.adjustSize()

        self.nouArxiu()

    def campsDB(self, nom):
        res = []
        if nom != '':
            fich = RUTA_DADES + nom
            if os.path.isfile(fich):
                conn = sqlite3.connect('file:' + fich + '?mode=ro', uri=True)
                conn.row_factory = sqlite3.Row
                c = conn.cursor()
                c.execute('select * from ' + nom.split('.')[0])
                row = c.fetchone()
                # res = [i[0].upper() for i in c.description]
                res = [i.upper() for i in row.keys()]
                conn.close()
        return res

    def soloPrimerItem(self, combo):
        combo.setCurrentIndex(0)
        ultimo = combo.count() - 1
        for n in range(ultimo, 0, -1):
            combo.removeItem(n)

    @pyqtSlot()
    def canviaZona(self):
        self.distribucio.setCurrentIndex(0)
        self.soloPrimerItem(self.distribucio)
        if self.zona.currentIndex() > 0:
            z = self.zona.currentText()
            campsZona = self.campsDB(MAP_ZONES[z][1])
            # Carga combo con distribuciones si el campo correspondiente está en la BBDD
            for dist, campo in MAP_DISTRIBUCIO.items():
                if campo != '' and campo in campsZona:
                    self.distribucio.addItem(dist)

    def borrarZonas(self):
        self.tipus.setCurrentIndex(0)
        self.soloPrimerItem(self.zona)
        self.calcul.clear()
        self.filtre.clear()

    def nouArxiu(self):
        if self.fCSV is None:
            return
        # Carga combo con zonas si el campo correspondiente está en el fichero CSV
        num = 0
        for zona, val in MAP_ZONES.items():
            if val[1] != '' and self.fCSV.prefixe + val[0] in self.fCSV.camps:
                self.zona.addItem(zona)
                num = num + 1
        if num == 0:
            self.msgInfo("El fitxer " + nom + " no té cap camp de zona")
            if hasattr(self, 'arxiu'):
                self.arxiu.lineEdit().clear()
                self.arxiu.setFocus()
            return
        if num == 1:
            self.zona.setCurrentIndex(1)
            self.capa.setFocus()
        else:
            self.zona.setFocus()
        self.calcul.setItems(self.fCSV.camps)
        self.filtre.setItems(self.fCSV.camps)

    @pyqtSlot(str)
    def arxiuSeleccionat(self, nom):
        if nom == '':
            return
        self.borrarZonas()
        self.fCSV = QvMapificacio(nom, numMostra=0)
        self.nouArxiu()

    def valida(self):
        ok = False
        if hasattr(self, 'arxiu') and self.arxiu.filePath() == '':
            self.msgInfo("S'ha de seleccionar un arxiu de dades")
            self.arxiu.setFocus()
        elif self.zona.currentIndex() <= 0:
            self.msgInfo("S'ha de seleccionar una zona")
            self.zona.setFocus()
        elif self.capa.text().strip() == '':
            self.msgInfo("S'ha de introduir un nom de capa")
            self.capa.setFocus()
        elif self.tipus.currentIndex() <= 0:
            self.msgInfo("S'ha de seleccionar un tipus d'agregació")
            self.tipus.setFocus()
        elif self.calcul.currentText().strip() == '' and self.tipus.currentText() != 'Recompte':
            self.msgInfo("S'ha de introduir un cálcul per fer l'agregació")
            self.calcul.setFocus()
        else:
            ok = True
        return ok

    def mapifica(self):
        if self.fCSV is None:
            return "No hi ha cap fitxer seleccionat"
        ok = self.fCSV.agregacio(self.llegenda, self.capa.text().strip(), self.zona.currentText(), self.tipus.currentText(),
                                 campAgregat=self.calcul.currentText().strip(), filtre=self.filtre.currentText().strip(),
                                 tipusDistribucio=self.distribucio.currentText(), modeCategories=self.metode.currentText(),
                                 numCategories=self.intervals.value(), colorBase=self.color.currentText())
        if ok:
            return ''
        else: 
            return self.fCSV.msgError

class QvFormSimbMapificacio(QvFormBaseMapificacio):
    def __init__(self, llegenda, capa, amplada=450):
        super().__init__(llegenda, amplada)
        self.capa = capa
        if not self.iniParams():
            return

        self.setWindowTitle('Modificar mapificació')

        self.layout = QVBoxLayout()
        self.layout.setSpacing(14)
        self.setLayout(self.layout)

        self.color = QComboBox(self)
        self.color.setEditable(False)
        self.comboColors(self.color)

        self.metode = QComboBox(self)
        self.metode.setEditable(False)
        self.metode.addItems(MAP_METODES_MODIF.keys())
        self.metode.setCurrentIndex(-1)
        self.metode.currentIndexChanged.connect(self.canviaMetode)

        self.nomIntervals = QLabel('Nombre intervals:', self)
        self.intervals = QSpinBox(self)
        self.intervals.setMinimum(2)
        self.intervals.setMaximum(max(MAP_MAX_CATEGORIES, self.numCategories))
        self.intervals.setSingleStep(1)
        self.intervals.setValue(4)
        self.intervals.setSuffix("  (depèn del mètode)")
        # self.intervals.valueChanged.connect(self.deselectValue)

        self.buttons = QDialogButtonBox()
        self.buttons.addButton(QDialogButtonBox.Ok)
        self.buttons.accepted.connect(self.accept)
        self.buttons.addButton(QDialogButtonBox.Cancel)
        self.buttons.rejected.connect(self.cancel)

        self.gSimb = QGroupBox('Simbologia mapificació')
        self.lSimb = QFormLayout()
        self.lSimb.setSpacing(14)
        # self.gSimb.setMinimumWidth(400)
        self.gSimb.setLayout(self.lSimb)

        self.lSimb.addRow('Color mapa:', self.color)
        self.lSimb.addRow('Mètode classificació:', self.metode)
        self.lSimb.addRow(self.nomIntervals, self.intervals)

        self.wInterval = []
        for w in self.iniIntervals():
            self.wInterval.append(w)
        self.gInter = self.grupIntervals()

        self.layout.addWidget(self.gSimb)
        self.layout.addWidget(self.gInter)
        self.layout.addWidget(self.buttons)

        self.valorsInicials()

    def iniParams(self):
        map = QgsExpressionContextUtils.layerScope(self.capa).variable(MAP_ID)
        if map != 'True':
            return False
        ok, (self.campCalculat, self.numDecimals, self.colorBase, self.numCategories, \
            self.modeCategories, self.rangsCategories) = self.llegenda.mapRenderer.paramsRender(self.capa)
        self.custom = (self.modeCategories == 'Personalitzat')
        if not ok:
            self.msgInfo("No s'han pogut recuperar els paràmetres de mapificació")
        return True

    def valorsInicials(self):        
        self.color.setCurrentIndex(self.color.findText(self.colorBase))
        self.intervals.setValue(self.numCategories)
        self.metode.setCurrentIndex(self.metode.findText(self.modeCategories))

    def valorsFinals(self):
        self.colorBase = self.color.currentText()
        self.modeCategories = self.metode.currentText()
        self.numCategories = self.intervals.value()
        if self.custom:
            self.rangs = []
            for fila in self.wInterval:
                self.rangs.append((fila[0].text(), fila[2].text()))

    def txtRang(self, num):
        if type(num) == str:
            return num
        return MAP_LOCALE.toString(num, 'f', self.numDecimals)

    def iniFilaInterval(self, iniValor, finValor):
        maxSizeB = 27
        # validator = QDoubleValidator(self)
        # validator.setLocale(MAP_LOCALE)
        # validator.setNotation(QDoubleValidator.StandardNotation)
        # validator.setDecimals(5)
        validator = QvVerifNumero(self)
        ini = QLineEdit(self)
        ini.setText(self.txtRang(iniValor))
        ini.setValidator(validator)
        sep = QLabel('-', self)
        fin = QLineEdit(self)
        fin.setText(self.txtRang(finValor))
        fin.setValidator(validator)
        fin.editingFinished.connect(self.nouTall)
        add = QPushButton('+', self)
        add.setMaximumSize(maxSizeB, maxSizeB)
        add.setToolTip('Afegeix nou interval')
        add.clicked.connect(self.afegirFila)
        add.setFocusPolicy(Qt.NoFocus)
        rem = QPushButton('-', self)
        rem.setMaximumSize(maxSizeB, maxSizeB)
        rem.setToolTip('Esborra interval')
        rem.clicked.connect(self.eliminarFila)
        rem.setFocusPolicy(Qt.NoFocus)
        return [ini, sep, fin, add, rem]

    def iniIntervals(self):
        for cat in self.rangsCategories:
            yield self.iniFilaInterval(cat.lowerValue(), cat.upperValue())

    def grupIntervals(self):
        group = QGroupBox('Definició intervals')
        # group.setMinimumWidth(400)
        layout = QGridLayout()
        layout.setSpacing(10)
        # layout.setColumnMinimumWidth(4, 40)
        numFilas = len(self.wInterval)
        for fila, widgets in enumerate(self.wInterval):
            for col, w in enumerate(widgets):
                # Primera fila: solo +
                if fila == 0 and col > 3:
                    w.setVisible(False)
                # # Ultima fila: no hay + ni -
                elif fila > 0 and fila == (numFilas - 1) and col > 2:
                    w.setVisible(False)
                else:
                    w.setVisible(True)
                # Valor inicial deshabilitado (menos 1a fila)
                if col == 0 and fila != 0:
                    w.setDisabled(True)
                w.setProperty('Fila', fila)
                layout.addWidget(w, fila, col)
        group.setLayout(layout)
        return group

    def actGrupIntervals(self):
        self.intervals.setValue(len(self.wInterval))

        self.setUpdatesEnabled(False)
        self.buttons.setVisible(False)
        self.gInter.setVisible(False)

        self.layout.removeWidget(self.buttons)
        self.layout.removeWidget(self.gInter)

        self.gInter.deleteLater()
        self.gInter = self.grupIntervals()

        self.layout.addWidget(self.gInter)
        self.layout.addWidget(self.buttons)

        self.gInter.setVisible(True)
        self.buttons.setVisible(True)

        self.adjustSize()
        self.setUpdatesEnabled(True)

    @pyqtSlot()
    def afegirFila(self):
        masFilas = (len(self.wInterval) < MAP_MAX_CATEGORIES)
        if masFilas:
            f = self.sender().property('Fila') + 1
            ini = self.wInterval[f][0]
            val = ini.text()
            ini.setText('')
            w = self.iniFilaInterval(val, '')
            self.wInterval.insert(f, w)
            self.actGrupIntervals()
            self.wInterval[f][2].setFocus()
        else:
            self.msgInfo("S'ha arribat al màxim d'intervals possibles")

    @pyqtSlot()
    def eliminarFila(self):
        f = self.sender().property('Fila')
        ini = self.wInterval[f][0]
        val = ini.text()
        del self.wInterval[f]
        ini = self.wInterval[f][0]
        ini.setText(val)
        self.actGrupIntervals()

    @pyqtSlot()
    def nouTall(self):
        w = self.sender()
        if w.isModified():
            f = w.property('Fila') + 1
            if f < len(self.wInterval):
                ini = self.wInterval[f][0]
                ini.setText(w.text())
            w.setModified(False)

    @pyqtSlot()
    def canviaMetode(self):
        self.custom = (self.metode.currentText() == 'Personalitzat')
        if self.custom:
            self.intervals.setValue(len(self.wInterval))
        self.intervals.setEnabled(not self.custom)
        self.gInter.setVisible(self.custom)
        self.adjustSize()
        # print('GSIMB -> Ancho:', self.gSimb.size().width(), '- Alto:', self.gSimb.size().height())
        # print('FORM -> Ancho:', self.size().width(), '- Alto:', self.size().height())

    def leSelectFocus(self, wLineEdit):
        lon = len(wLineEdit.text())
        if lon > 0:
            wLineEdit.setSelection(0, lon)
        wLineEdit.setFocus()

    def validaNum(self, wLineEdit):
        val = wLineEdit.validator()
        if val is None:
            return True
        res = val.validate(wLineEdit.text(), 0)
        if res[0] == QValidator.Acceptable:
            return True
        else:
            self.msgInfo("Cal introduir un nombre enter o amb decimals.\n"
                "Es farà servir la coma (,) per separar els decimals.\n"
                "I pels milers, opcionalment, el punt (.)")
            self.leSelectFocus(wLineEdit)
            return False

    def validaInterval(self, wLineEdit1, wLineEdit2):
        num1, _ = MAP_LOCALE.toFloat(wLineEdit1.text())
        num2, _ = MAP_LOCALE.toFloat(wLineEdit2.text())
        if num2 > num1:
            return True
        else:
            self.msgInfo("El segon nombre de l'interval ha de ser major que el primer")
            self.leSelectFocus(wLineEdit2)
            return False

    def validaFila(self, fila):
        wLineEdit1 = fila[0]
        wLineEdit2 = fila[2]
        if not self.validaNum(wLineEdit1):
            return False
        if not self.validaNum(wLineEdit2):
            return False
        if not self.validaInterval(wLineEdit1, wLineEdit2):
            return False
        return True

    def valida(self):
        if self.custom:
            for fila in self.wInterval:
                if not self.validaFila(fila):
                    return False
        return True

    def mapifica(self):
        self.valorsFinals()
        try:
            if self.custom:
                self.renderer = self.llegenda.mapRenderer.customRender(self.capa, self.campCalculat,
                    MAP_COLORS[self.colorBase], self.rangs)
            else:
                self.renderer = self.llegenda.mapRenderer.calcRender(self.capa, self.campCalculat, self.numDecimals,
                    MAP_COLORS[self.colorBase], self.numCategories, MAP_METODES_MODIF[self.modeCategories])            
            if self.renderer is None:
                return "No s'ha pogut elaborar el mapa"
            err = self.llegenda.saveStyleToGeoPackage(self.capa, MAP_ID)
            if err != '':
                return "Hi ha hagut problemes al desar la simbologia\n({})".format(err)
            # self.llegenda.modificacioProjecte('mapModified')
            return ''
        except Exception as e:
            return "No s'ha pogut modificar em mapa\n({})".format(str(e))

