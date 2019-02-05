# -*- coding: utf-8 -*-

from qgis.core import (QgsProject, QgsLegendModel, QgsLayerDefinition, QgsMapLayer, 
                       QgsLayerTree, QgsLayerTreeNode, QgsLayerTreeLayer)
from qgis.gui import (QgsLayerTreeView, QgsLayerTreeViewMenuProvider, QgsLayerTreeMapCanvasBridge,
                      QgsLayerTreeViewIndicator, QgsSearchQueryBuilder)
from qgis.PyQt.QtWidgets import QMenu, QAction, QFileDialog, QWidget, QPushButton, QVBoxLayout, QHBoxLayout
from qgis.PyQt.QtGui import QIcon, QBrush, QColor
from qgis.PyQt.QtCore import Qt, pyqtSignal, QSortFilterProxyModel
from moduls.QvAccions import QvAccions
from moduls.QvAtributs import QvAtributs
from moduls.QvApp import QvApp

# import images_rc
# import recursos

class QvBotoneraLlegenda(QWidget):

    clicatBoto = pyqtSignal(int)

    def __init__(self, llegenda, nom = 'Llegenda', vertical = True):
        super().__init__()
        self.llegenda = llegenda
        self.items = dict()
        self.botons = dict()
        self.setWindowTitle(nom)
        if vertical:
            self.setLayout(QVBoxLayout())
        else:
            self.setLayout(QHBoxLayout())
        self.funcioFiltre = None
        self.funcioBoto = None

    def afegirBoto(self, item):
        if self.llegenda.editable:
            self.llegenda.editarLlegenda(False)
        boto = QPushButton(item.nom())
        boto.setCheckable(True)
        boto.setChecked(item.esVisible())
        self.layout().addWidget(boto)
        i = self.layout().indexOf(boto)
        self.items[i] = item
        self.botons[i] = boto
        boto.clicked.connect(self.clickBoto)
        return boto

    def esborrarBotonera(self):
        layout = self.layout()
        for i in range(layout.count()):
            layout.removeItem(layout.itemAt(i))
        self.repaint()
        self.items = dict()
        self.botons = dict()

    def afegirBotonera(self, funcioFiltre = None, funcioBoto = None):
        # Filtro de usuario del itema a añadir a botonera
        if funcioFiltre is not None:
            self.funcioFiltre = funcioFiltre
        # Modificación de usuario del boton generado
        if funcioBoto is not None:
            self.funcioBoto = funcioBoto
        self.esborrarBotonera()
        for item in self.llegenda.items():
            if self.funcioFiltre is None or self.funcioFiltre(item):
                boto = self.afegirBoto(item)
                if self.funcioBoto is not None:
                    self.funcioBoto(boto)

    def actBotons(self):
        for i in range(len(self.botons)):
            self.botons[i].setChecked(self.items[i].esVisible())

    def clickBoto(self):
        boto = self.sender()
        i = self.layout().indexOf(boto)
        item = self.items[i]
        item.veure(not item.esVisible())
        self.actBotons()
        self.clicatBoto.emit(i)

class QvItemLlegenda(object):

    def __init__(self, item, nivell):
        super().__init__()
        self.item = item
        self.nivell = nivell
        self.tipus = self.tipus()

    def nivell(self):
        return self.nivell()

    def tipus(self):
        clase = type(self.item).__name__
        if clase == 'QgsLayerTreeLayer':
            return 'layer'
        elif clase == 'QgsLayerTreeGroup':
            return 'group'
        elif clase == 'QgsLayerTreeModelLegendNode':
            return 'symb'
        else:
            return 'none'
    
    def capa(self):
        if self.tipus == 'layer':
            return self.item.layer()
        elif self.tipus == 'group':
            return None
        elif self.tipus == 'symb':
            return self.item.layerNode().layer()
        else:
            return None

    def nom(self):
        if self.tipus in ('layer', 'group'):
            return self.item.name()
        elif self.tipus == 'symb':
            return self.item.data(Qt.DisplayRole)
        else:
            return None

    def esMarcat(self):
        if self.tipus in ('layer', 'group'):
            return self.item.itemVisibilityChecked()
        elif self.tipus == 'symb':
            return self.item.data(Qt.CheckStateRole) != 0
        else:
            return None

    def marcar(self, on = True):
        if self.tipus in ('layer', 'group'):
            self.item.setItemVisibilityChecked(on)
        elif self.tipus == 'symb':
            if on:
                self.item.setData(Qt.Checked, Qt.CheckStateRole)
            else:
                self.item.setData(Qt.Unchecked, Qt.CheckStateRole)

    def esVisible(self):
        if self.tipus in ('layer', 'group'):
            return self.item.isVisible()
        elif self.tipus == 'symb':
            return self.esMarcat() and self.item.layerNode().isVisible()
        else:
            return None

    def veure(self, on = True, children = True):
        if self.tipus in ('layer', 'group'):
            if on:
                self.item.setItemVisibilityCheckedParentRecursive(True)
                if children:
                    self.item.setItemVisibilityCheckedRecursive(True)
            else:
                self.marcar(False)
        elif self.tipus == 'symb':
            self.marcar(on)
            if on:
                self.item.layerNode().setItemVisibilityCheckedParentRecursive(True)
                if children:
                    self.item.layerNode().setItemVisibilityCheckedRecursive(True)

class QvLlegendaModel(QgsLegendModel):
    def __init__(self, root):
        super().__init__(root)
        self.setScale(1.0)

    def setScale(self, scale):
        self.scale = scale

    def data(self, index, role):
        if index.isValid() and role == Qt.ForegroundRole:
            node = self.index2node(index)
            if node is not None and node.nodeType() == QgsLayerTreeNode.NodeLayer: # and node.isVisible():
                layer = node.layer()
                if layer is not None and layer.hasScaleBasedVisibility():
                    if layer.isInScaleRange(self.scale):
                        color = QColor('#000000')
                    else:
                        color = QColor('#c0c0c0')
                    return color
        return super().data(index, role)

class QvLlegenda(QgsLayerTreeView):

    obertaTaulaAtributs = pyqtSignal()
    clicatMenuContexte = pyqtSignal(str)
    carregantProjecte = pyqtSignal()
    projecteCarregat = pyqtSignal(str)

    def __init__(self, canvas=None, atributs=None, canviCapaActiva=None, debug=False):
        super().__init__()
        self.debug = debug
        self.project = QgsProject.instance()
        self.root = self.project.layerTreeRoot()
        self.canvas = None
        self.bridge = None
        self.bridges = []
        self.atributs = atributs
        self.editable = True

        self.project.readProject.connect(self.nouProjecte)

        self.setWhatsThis(QvApp().carregaAjuda(self))

        # Asociar canvas y bridges
        self.mapBridge(canvas)

        # Evento de nueva capa seleccionada
        self.connectaCanviCapaActiva(canviCapaActiva)

        # Model
        self.model = QvLlegendaModel(self.root)
        self.model.setFlag(QgsLegendModel.ShowLegend, True)
        self.model.setFlag(QgsLegendModel.ShowLegendAsTree, True)
        self.editarLlegenda(True)

        self.setModel(self.model)
        if self.canvas is not None:
            self.canvas.scaleChanged.connect(self.connectaEscala)

        # Acciones disponibles
        self.accions = QvAccions()
        self.setAccions()
        # Lista de acciones que apareceran en el menú
        self.menuAccions = []
        self.setMenuProvider(QvMenuLlegenda(self))

        # self.setAcceptDrops(True)
        # self.setDropIndicatorShown(True)

        self.iconaFiltre = QgsLayerTreeViewIndicator()
        # self.iconaFiltre.setIcon(QIcon(':/Icones/ic_file_upload_black_48dp.png'))
        self.iconaFiltre.setIcon(QIcon('imatges/filter.png'))
        self.iconaFiltre.setToolTip('Filtre actiu')

        if self.atributs is not None:
            self.atributs.modificatFiltreCapa.connect(self.actIconaFiltre)

        self.projecteObert = False
        if self.canvas is not None:
            self.project.layerLoaded.connect(self.iniProjecte)
            self.canvas.renderComplete.connect(self.fiProjecte)

        if self.debug:
            self.printSignals()

    def iniProjecte(self, num, tot):
        # La carga de un proyecto se inicia con la capa #0
        if num == 0:
            self.projecteObert = False
            self.carregantProjecte.emit()
    
    def fiProjecte(self):
        # La carga de un proyecto acaba con su visualización en el canvas
        if not self.projecteObert:
            self.projecteObert = True
            self.projecteCarregat.emit(self.project.fileName())

    def printSignals(self):
        self.canvas.layersChanged.connect(lambda: print('Canvas layersChanged'))
        self.canvas.renderStarting.connect(lambda: print('Canvas renderStarting'))
        self.canvas.renderComplete.connect(lambda: print('Canvas renderComplete'))
        self.project.layerLoaded.connect(lambda num, tot: print("Project layerLoaded %d / %d" % (num, tot)))
        self.project.readProject.connect(lambda: print('Project readProject'))
        self.carregantProjecte.connect(lambda: print('*** Llegenda carregantProjecte'))
        self.projecteCarregat.connect(lambda f: print('*** Llegenda projecteCarregat ' + f))
        
    def editarLlegenda(self, on=True):
        self.editable = on
        self.model.setFlag(QgsLegendModel.AllowNodeReorder, on)
        self.model.setFlag(QgsLegendModel.AllowNodeRename, on)
        self.model.setFlag(QgsLegendModel.AllowLegendChangeState, on)
        self.model.setFlag(QgsLegendModel.AllowNodeChangeVisibility, on)
        self.model.setFlag(QgsLegendModel.DeferredLegendInvalidation, on)

    def connectaEscala(self, escala):
        # print('Cambio escala:', escala)
        self.model.setScale(escala)
        for capa in self.capes():
            if capa.hasScaleBasedVisibility():
                capa.nameChanged.emit()

    def actIconaFiltre(self, capa):
        if capa.type() != QgsMapLayer.VectorLayer:
            return
        node = self.root.findLayer(capa.id())
        if node is not None:
            if capa.subsetString() == '':
                self.removeIndicator(node, self.iconaFiltre)
            else:
                self.addIndicator(node, self.iconaFiltre)
            capa.nameChanged.emit()

    def nouProjecte(self):
        # Borrar tabs de atributos si existen
        if self.atributs is not None:
            self.atributs.deleteTabs()
        # Guardar escala inicial
        # if self.canvas is not None:
        #     escala = self.canvas.scale()
        # Capas: actualizar icono filtro y tratar capas raster
        for layer in self.capes():
            if layer.type() == QgsMapLayer.VectorLayer:
                self.actIconaFiltre(layer)
            if layer.type() == QgsMapLayer.RasterLayer and self.capaMarcada(layer):
                self.veureCapa(layer, False)
                self.veureCapa(layer, True)
        # Establecer escala inicial
        # print('Escala:', escala)
        # if self.canvas is not None:
        #     self.canvas.zoomScale(escala)

        # print('Capes Llegenda:')
        # for layer in leyenda.capes():
        #     print('-', layer.name(), ', Visible:', leyenda.capaVisible(layer),
        #                              ', Marcada:', leyenda.capaMarcada(layer),
        #                              ', Filtro escala:', layer.hasScaleBasedVisibility())
        #     if layer.type() == QgsMapLayer.VectorLayer:
        #         print(' ', 'Filtro datos:', layer.subsetString())
        #         leyenda.actIconaFiltre(layer)

    def connectaCanviCapaActiva(self, canviCapaActiva):
        if canviCapaActiva:
            self.currentLayerChanged.connect(canviCapaActiva)
    
    def mapBridge(self, canvas):
        """
        Enlaza el proyecto con un canvas. La primera vez se invoca con el canvas del
        mapa principal. El resto, con los temas.
        
        Arguments:
            canvas {QgsMapCanvas} -- Canvas donde se muestra el proyecto
                bridges
        """
        if canvas is None:
            return
        bridge = QgsLayerTreeMapCanvasBridge(self.root, canvas)
        if self.canvas is None: # Canvas principal
            self.canvas = canvas
            self.bridge = bridge
        else:
            self.bridges.append((canvas, bridge))

    def temes(self):
        return self.project.mapThemeCollection().mapThemes()

    def capaPerNom(self, nomCapa):
        """
        Devuelve el primer layer con el nombre especificado.
        
        Arguments:
            nomCapa {String} -- El nombre del layer que queremos recuperar.
        
        Returns:
            QgsMapLayer -- El layer que hemos pedido por nombre.
        
        """
        capes = self.project.mapLayersByName(nomCapa)
        if len(capes) > 0:
            return capes[0]
        else:
            return None

    def capes(self):
        """
        Devuelve la lista de capas de la leyenda.
        
        Returns:
            List de QgsMapLayers -- La lista de capas.

        """
        for capaId in self.project.mapLayers():
            yield self.project.mapLayer(capaId)

    def veureCapa(self, capa, visible = True, subCapas = True):
        """
        Hace visible o invisible una layer.

        Arguments:
            capa {QgsMapLayer} -- Layer al que queremos cambiar su visibilidad.
            visible {bool} -- True (visible) o False (invisible).
            subCapes {bool} -- True si queremos cambiar también la visibilidad de los hijos
        
        """
        node = self.root.findLayer(capa.id())
        if node is not None:
            if visible:
                node.setItemVisibilityCheckedParentRecursive(True)
                if subCapas:
                    node.setItemVisibilityCheckedRecursive(True)

            else:
                node.setItemVisibilityChecked(False)

    def capaVisible(self, capa):
        node = self.root.findLayer(capa.id())
        if node is not None:
            v = node.isVisible()
            if v and capa.hasScaleBasedVisibility() and self.canvas is not None:
                return capa.isInScaleRange(self.canvas.scale())
            return v
        return False

    def capaMarcada(self, capa):
        node = self.root.findLayer(capa.id())
        if node is not None:
            return node.itemVisibilityChecked()
        return False

    def setAccions(self):
        act = QAction()
        act.setText("Defineix grup")
        # act.setIcon(QIcon(':/Icones/ic_file_upload_black_48dp.png'))
        act.triggered.connect(self.defaultActions().addGroup)
        self.accions.afegirAccio('addGroup', act)

        act = QAction()
        act.setText("Afegeix capa")
        # act.setIcon(QIcon(':/Icones/ic_file_upload_black_48dp.png'))ic_beach_access_black_48dp
        act.triggered.connect(self.addLayersFromFile)
        self.accions.afegirAccio('addLayersFromFile', act)

        act = QAction()
        act.setText("Canvia nom")
        # act.setIcon(QIcon(':/Icones/ic_file_upload_black_48dp.png'))
        act.triggered.connect(self.defaultActions().renameGroupOrLayer) #, type = Qt.DirectConnection)
        self.accions.afegirAccio('renameGroupOrLayer', act)
        
# 
# TODO:
# Sincronizar señales para que la segunda espere al final de la primera
# 
        # if self.atributs is not None:
        #   act.triggered.connect(lambda: self.atributs.tabTaula(self.currentLayer()))

        act = QAction()
        act.setText("Esborra capa o grup")
        # act.setIcon(QIcon(':/Icones/ic_file_upload_black_48dp.png'))
        if self.atributs is not None:
            act.triggered.connect(lambda: self.atributs.tancarTaula(self.currentLayer())) #, type = Qt.DirectConnection)
        act.triggered.connect(self.defaultActions().removeGroupOrLayer)
        self.accions.afegirAccio('removeGroupOrLayer', act)

        act = QAction()
        act.setText("Enquadra capa")
        # act.setIcon(QIcon(':/Icones/ic_file_upload_black_48dp.png'))
        act.triggered.connect(self.showLayerMap)
        self.accions.afegirAccio('showLayerMap', act)

        act = QAction()
        act.setText("Mostra contador elements")
        # act.setIcon(QIcon(':/Icones/ic_file_upload_black_48dp.png'))
        act.triggered.connect(self.defaultActions().showFeatureCount)
        # act.setCheckable(True)
        # act.setChecked(False)
        self.accions.afegirAccio('showFeatureCount', act)

        act = QAction()
        act.setText("Mostra taula dades")
        # act.setIcon(QIcon(':/Icones/ic_file_upload_black_48dp.png'))
        act.triggered.connect(self.showFeatureTable)
        self.accions.afegirAccio('showFeatureTable', act)

        act = QAction()
        act.setText("Filtra elements")
        # act.setIcon(QIcon(':/Icones/ic_file_upload_black_48dp.png'))
        act.triggered.connect(self.filterElements)
        self.accions.afegirAccio('filterElements', act)

        act = QAction()
        act.setText("Esborra filtre")
        # act.setIcon(QIcon(':/Icones/ic_file_upload_black_48dp.png'))
        act.triggered.connect(self.removeFilter)
        self.accions.afegirAccio('removeFilter', act)

    def calcTipusMenu(self):
        # Tipos: none, group, layer, symb
        tipo = 'none'
        idx = self.currentIndex()
        if idx.isValid():
            node = self.currentNode()
            if node is None:
                tipo = 'symb'
            else:
                tipoNodo = node.nodeType()
                if tipoNodo == QgsLayerTreeNode.NodeGroup:
                    tipo = 'group'
                elif tipoNodo == QgsLayerTreeNode.NodeLayer:
                    tipo = 'layer'
        return tipo

    def setMenuAccions(self):
        # Menú dinámico según tipo de elemento sobre el que se clicó
        self.menuAccions = []
        tipo = self.calcTipusMenu()
        if tipo == 'layer':
            capa = self.currentLayer()
            if capa is not None and capa.type() == QgsMapLayer.VectorLayer:
                if self.atributs is not None:
                    self.menuAccions += ['showFeatureTable', 'filterElements' ]
                self.menuAccions += ['showFeatureCount']
            if capa is not None and self.canvas is not None:
                self.menuAccions += ['showLayerMap']
            if self.editable:
                self.menuAccions += ['separator',
                                     'addGroup', 'renameGroupOrLayer', 'removeGroupOrLayer']
        elif tipo == 'group':
            if self.editable:
                self.menuAccions += ['addGroup', 'renameGroupOrLayer', 'removeGroupOrLayer']
        elif tipo == 'none':
            if self.editable:
                self.menuAccions += ['addGroup']
        else: # 'symb'
            pass
        return tipo

    # def removeGroupOrLayer(self):
    #     if self.atributs is not None:
    #         self.atributs.tancarTaula(self.currentLayer())
    #     self.defaultActions().removeGroupOrLayer()

    def addLayersFromFile(self):
        dlgLayers = QFileDialog()
        # dlgLayers.setDirectoryUrl()
        nfile, _ = dlgLayers.getOpenFileName(None, "Afegir Capes Qgis", ".", "Capes Qgis (*.qlr)")
        if nfile != '':
            QgsLayerDefinition.loadLayerDefinition(nfile, self.project, self.root)
    
    def showLayerMap(self):
        if self.canvas is not None:
            layer = self.currentLayer()
            if layer is not None:
                self.veureCapa(layer)
                extent = layer.extent()
                self.canvas.setExtent(extent)
                self.canvas.refresh()

    def showFeatureTable(self):
        if self.atributs is not None:
            layer = self.currentLayer()
            if layer is not None and layer.type() == QgsMapLayer.VectorLayer:
                self.atributs.obrirTaula(layer)
                self.atributs.show()
                self.obertaTaulaAtributs.emit()

    def filterElements(self):
        layer = self.currentLayer()
        if layer is not None and self.atributs is not None:
            self.atributs.filtrarCapa(layer, True)
            # self.actIconaFiltre(layer)
            # try:
            #     dlgFiltre = QgsSearchQueryBuilder(layer)
            #     dlgFiltre.setSearchString(layer.subsetString())
            #     dlgFiltre.exec_()
            #     layer.setSubsetString(dlgFiltre.searchString())
            #     self.actIconaFiltre(layer)
            # except Exception as e:
            #     print(str(e))

    def removeFilter(self):
        layer = self.currentLayer()
        if layer is not None and self.atributs is not None:
            self.atributs.filtrarCapa(layer, False)
            # self.actIconaFiltre(layer)
        # if layer is not None:
        #     layer.setSubsetString('')
        #     self.actIconaFiltre(layer)

    def nodes(self):
        def recurse(parent):
            for child in parent.children():
                yield child
                yield from recurse(child)
        num = self.model.rowCount()
        for row in range(num):
            index = self.model.index(row, 0)
            node = self.model.index2node(index)
            yield node
            yield from recurse(node)

    def nodePerNom(self, nom, filtre = 'none'):
        if filtre == 'group':
            tipus = QgsLayerTreeNode.NodeGroup
        elif filtre == 'layer':
            tipus = QgsLayerTreeNode.NodeLayer
        else:
            tipus = None
        for node in self.nodes():
            if (tipus is None or tipus == node.nodeType()) and node.name() == nom:
                return node
        return None

    def items(self):
        def recurse(item, level):
            yield QvItemLlegenda(item, level)
            if QgsLayerTree.isLayer(item):
                for cat in self.model.layerOriginalLegendNodes(item):
                    if cat.data(Qt.CheckStateRole) is not None:
                        yield QvItemLlegenda(cat, level + 1)
            for child in item.children():
                yield from recurse(child, level + 1)
        num = self.model.rowCount()
        for row in range(num):
            index = self.model.index(row, 0)
            item = self.model.index2node(index)
            yield from recurse(item, 0)

class QvMenuLlegenda(QgsLayerTreeViewMenuProvider):

    def __init__(self, llegenda):
        QgsLayerTreeViewMenuProvider.__init__(self)
        self.llegenda = llegenda

    def createContextMenu(self):
        tipo = self.llegenda.setMenuAccions()
        self.llegenda.clicatMenuContexte.emit(tipo)
        return self.llegenda.accions.menuAccions(self.llegenda.menuAccions)

if __name__ == "__main__":

    from qgis.core.contextmanagers import qgisapp
    from qgis.gui import QgsMapCanvas
    from qgis.PyQt.QtWidgets import QMessageBox

    with qgisapp(sysexit=False) as app:

        QvApp().carregaIdioma(app, 'ca')
        # QvApp().logInici()

        def printCapaActiva():
            cLayer = leyenda.currentLayer()
            if cLayer:
                print('Capa activa:', leyenda.currentLayer().name())
            else:
                print('Capa activa: None')

        canv = QgsMapCanvas()

        atrib = QvAtributs(canv)

        leyenda = QvLlegenda(canv, atrib, printCapaActiva, debug=True)

        leyenda.project.read('../dades/projectes/bcn11.qgs')
        # leyenda.project.read('../dades/projectes/Prototip GUIA OracleSpatial_WMS.qgz')

    # Al cargar un proyecto o capa:
    # - Ver si tiene filtro de datos para actualizar el icono del embudo
    # - Para las capas raster, ver si funciona el chech/uncheck de la capa para la visualización
    # - Ver si se produce un cambio de escala y restaurarlo
    # Evento: QgsProject -> legendLayersAdded(lista de capas)

        canv.setWindowTitle('Canvas')
        canv.show()

        leyenda.setWindowTitle('Llegenda')
        leyenda.show()

        #
        # Funciones de capes:
        # capes(), capaPerNom(), veureCapa(), capaVisible(), capaMarcada(), currentLayer(), setCurrentLayer()
        #
        #
        # Funciones de nodes:
        # nodes(), nodePerNom(), node.isVisible(), node.itemVisibilityChecked()
        #

        # leyenda.veureCapa(leyenda.capaPerNom('BCN_Barri_ETRS89_SHP'), True)
        # leyenda.veureCapa(leyenda.capaPerNom('BCN_Districte_ETRS89_SHP'), False)
        # leyenda.veureCapa(leyenda.capaPerNom('BCN_Illes_ETRS89_SHP'), True)

        # leyenda.setCurrentLayer(leyenda.capaPerNom('BCN_Barri_ETRS89_SHP'))

        # Acciones personalizadas para menú contextual de la leyenda:
        #
        # - Definición de la acción y del metodo asociado
        # - Se añade la acción a la lista de acciones disponibles (llegenda.accions)
        # - Se redefine la lista de acciones que apareceran en el menú (llegenda.menuAccions)
        #   mediante la señal clicatMenuContexte según el tipo de nodo clicado
        #   (Tipos: none, group, layer, symb)

        # Generación de botoneras de leyenda
        def filtroBotonera(item):
            return item.tipus in ('layer','group')

        def filtroRangos(item):
            return item.tipus in ('symb')

        def modifBoton(boton):
            boton.setFlat(True)

        def botonCapa(i):
            if leyenda.capaVisible(leyenda.capaPerNom('BCN_Districte_ETRS89_SHP')):
                testSimbologia()
            else:
                if rangos is not None:
                    rangos.close()

        botonera = None
        rangos = None

        # Acciones de usuario
        def testCapas():
            global botonera
            botonera = QvBotoneraLlegenda(leyenda, 'Botonera')
            botonera.afegirBotonera(filtroBotonera, modifBoton)
            botonera.clicatBoto.connect(botonCapa)
            botonera.show()
            if leyenda.capaVisible(llegenda.capaPerNom('BCN_Districte_ETRS89_SHP')):
                testSimbologia()

        def testSimbologia():
            global rangos
            rangos = QvBotoneraLlegenda(leyenda, 'Rangos', False)
            rangos.afegirBotonera(filtroRangos, modifBoton)
            rangos.show()

        def test():
            QvApp().logRegistre('Menú Test')

            print('Items Llegenda:')
            for item in leyenda.items():
                capa = item.capa()
                if capa is None:
                    nomCapa = '-'
                else:
                    nomCapa = capa.name()
                print('  ' * item.nivell, '-',
                      'Tipo:', item.tipus,
                     'Nivel:', item.nivell,
                     ' Capa:', nomCapa,
                    'Nombre:', item.nom(), 
                   'Visible:', item.esVisible(),
                   'Marcado:', item.esMarcat())

        def salutacions():
            QMessageBox().information(None, 'qVista', 'Salutacions ' + QvApp().usuari)

        def editable():
            leyenda.editarLlegenda(not leyenda.editable)
            if leyenda.editable:
                if rangos is not None:
                    rangos.close()
                if botonera is not None:
                     botonera.close()
        
        # Acciones de usuario para el menú
        act = QAction()
        act.setText("Editable")
        act.triggered.connect(editable)
        leyenda.accions.afegirAccio('editable', act)

        act = QAction()
        act.setText("Test")
        act.triggered.connect(test)
        leyenda.accions.afegirAccio('test', act)

        act = QAction()
        act.setText("Test Botonera")
        act.triggered.connect(testCapas)
        leyenda.accions.afegirAccio('testCapas', act)

        act = QAction()
        act.setText("Test Simbologia")
        act.triggered.connect(testSimbologia)
        leyenda.accions.afegirAccio('testSimbologia', act)

        # Adaptación del menú
        def menuContexte(tipo):
            if tipo == 'none':
                leyenda.menuAccions.append('addLayersFromFile')
                leyenda.menuAccions.append('separator')
                leyenda.menuAccions.append('test')
                leyenda.menuAccions.append('testCapas')
                # leyenda.menuAccions.append('testSimbologia')
                leyenda.menuAccions.append('editable')

        # Conexión de la señal con la función menuContexte para personalizar el menú
        leyenda.clicatMenuContexte.connect(menuContexte)

        app.aboutToQuit.connect(QvApp().logFi)
    
    #######
        
        # QgsLayerTreeNode --> nameChanged()

        # from qgis.gui import QgsCategorizedSymbolRendererWidget
        # from qgis.core import QgsStyle

        # layer = llegenda.currentLayer()
        # renderer = layer.renderer()
        # cats = QgsCategorizedSymbolRendererWidget(layer, QgsStyle.defaultStyle(), renderer)
        # cats.show()
        # cats.applyChanges()

