# coding:utf-8

from importaciones import *

from qgis.PyQt.QtGui import QStandardItemModel, QStandardItem
from qgis.core import QgsRectangle

from PyQt5.QtWebKitWidgets import QWebView , QWebPage
from PyQt5.QtWebKit import QWebSettings
projecteInicial='../dades/projectes/BCN11_nord.qgs'

class BotoQvBrowser(QtWidgets.QPushButton):
    def __init__(self):
        QtWidgets.QPushButton.__init__(self)
        self.setMinimumHeight(30)
        self.setMaximumHeight(30)
        self.setMinimumWidth(100)
        self.setMaximumWidth(100)

class QvBrowser(QtWidgets.QWidget):

    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self)
        self.parent = parent
        self.browser = QWebView()
        self.browser.setContentsMargins(0,0,0,0)
        self.browser.setUrl(QUrl("http://www.qt.io"))
        self.browser.resize(512, 375)
        self.browser.show()
        self.setContentsMargins(0,0,0,0)

        self.layoutBrowser = QVBoxLayout(self)
        self.layoutBrowser.setContentsMargins(0,0,0,0)
        self.layoutBrowser.setSpacing(0)

        self.botoneraQvBrowser = QtWidgets.QFrame()
        self.botoneraQvBrowser.setContentsMargins(0,0,0,0)
        self.botoneraQvBrowser.setMinimumHeight(30)
        self.botoneraQvBrowser.setMaximumHeight(30)

        self.layoutBotonera = QHBoxLayout(self.botoneraQvBrowser)
        self.layoutBotonera.setContentsMargins(0,0,0,0)
        self.layoutBotonera.setAlignment( Qt.AlignRight )
        self.botoneraQvBrowser.setLayout(self.layoutBotonera)

        self.botoneraQvBrowser.show()
        self.botoTancar = BotoQvBrowser()
        self.botoTancar.setText('SORTIR')
        self.botoTancar.clicked.connect(self.tancar)
        self.botoTancar.show()

        self.botoOSM = BotoQvBrowser()
        self.botoOSM.setText('OpenStreet Maps')
        self.botoOSM.clicked.connect(self.openStreetMaps)
        self.botoOSM.show()

        self.botoGoogleMaps = BotoQvBrowser()
        self.botoGoogleMaps.setText('Google Maps')
        self.botoGoogleMaps.clicked.connect(self.openGoogleMaps)
        self.botoGoogleMaps.show()

        self.botoStreetView = BotoQvBrowser()
        self.botoStreetView.setText('Street view')
        self.botoStreetView.clicked.connect(self.openStreetView)
        self.botoStreetView.show()


        self.layoutBotonera.addWidget(self.botoOSM)
        self.layoutBotonera.addWidget(self.botoGoogleMaps)
        self.layoutBotonera.addWidget(self.botoStreetView)
        self.layoutBotonera.addWidget(self.botoTancar)
        self.layoutBrowser.addWidget(self.botoneraQvBrowser)
        self.layoutBrowser.addWidget(self.browser)
        self.setLayout(self.layoutBrowser)
        # https://www.openstreetmap.org/#map=17/41.38740/2.17272
    
    def openGoogleMaps(self):
        self.browser.setUrl(QUrl(self.parent.urlGoogleMaps))
    def openStreetMaps(self):
        self.browser.setUrl(QUrl(self.parent.urlStreetMaps))
    def openStreetView(self):
        self.browser.setUrl(QUrl(self.parent.urlStreetView))


    
    def tancar(self):
        print('sortir')
        self.hide()

class QvStreetView(QtWidgets.QWidget,QgsMapTool):
    """Una classe del tipus QWidget 
    """
    
    def __init__(self, canvas):
        """Inicialització de la clase:
            Arguments:
                canvas {QgsVectorLayer} -- El canvas sobre el que es clicka   
        """
        # We inherit our parent's properties and methods.
        QtWidgets.QWidget.__init__(self)
        QgsMapTool.__init__(self, canvas)
        self.moureBoto = False

        self.canvas = canvas

        canvas.setMapTool(self)
        self.boto = QtWidgets.QPushButton(self.canvas)
        self.icon=QIcon('littleMan.png')
        self.boto.setIcon(self.icon)
        self.boto.clicked.connect(self.segueixBoto)

        self.setupUI()
        # self.canvas.xyCoordinates.connect(self.mocMouse)
    def segueixBoto(self):
        self.rp.moureBoto = True
    def setupUI(self):
        self.layoutH = QtWidgets.QHBoxLayout(self)
        self.layoutH.setContentsMargins(0,0,0,0)
        self.layoutH.setSpacing(0)
        self.setLayout(self.layoutH)


        self.qbrowser = QvBrowser(self)
        self.qbrowser.hide()

        self.layoutH.addWidget(self.qbrowser)
        self.layoutH.addWidget(self.canvas)

            
    def canvasMoveEvent(self, event):
        self.dockX = event.pos().x()
        self.dockY = event.pos().y()
        if self.moureBoto:
            self.boto.move(event.x()-30,event.y()-30)

    def canvasReleaseEvent(self, event):
        
        self.point = self.toMapCoordinates(event.pos())
        xMon = self.point.x()
        yMon = self.point.y()

        self.transformacio = QgsCoordinateTransform(QgsCoordinateReferenceSystem("EPSG:25831"), 
                             QgsCoordinateReferenceSystem("EPSG:4326"), 
                             QgsProject.instance())
                             
        self.puntTransformat=self.transformacio.transform(self.point) 

        self.pucMoure = False
        # streetView = 'https://www.google.com/maps/@{},{},3a,75y,0h,75t'.format(self.puntTransformat.y(),puntTransformat.x())
        # streetView = 'https://www.google.com/maps/@{},{},2a/data=!3m1!1e3'.format(puntTransformat.y(),puntTransformat.x())
        self.urlStreetView = "https://maps.google.com/maps?layer=c&cbll={},{}".format(self.puntTransformat.y(), self.puntTransformat.x())
        self.urlGoogleMaps = 'https://www.google.com/maps/@{},{},2a/data=!3m1!1e3'.format(self.puntTransformat.y(), self.puntTransformat.x())
        self.urlStreetMaps = "https://www.openstreetmap.org/#map=17/{}/{}".format(self.puntTransformat.y(), self.puntTransformat.x())

        self.qbrowser.browser.setUrl(QUrl(self.urlStreetView))
        self.qbrowser.show()
        self.boto.move(0,0)
        self.moureBoto = False
if __name__ == "__main__":
    with qgisapp():
        canvas=QgsMapCanvas()
        canvas.setContentsMargins(0,0,0,0)
        project=QgsProject().instance()
        root=project.layerTreeRoot()
        bridge=QgsLayerTreeMapCanvasBridge(root,canvas)
        bridge.setCanvasLayers()

        # llegim un projecte de demo

        project.read(projecteInicial)
        
        qvSv = QvStreetView(canvas)
        # qvSv.setContentsMargins(0,0,0,0)
        qvSv.show()

        canvas.show()

