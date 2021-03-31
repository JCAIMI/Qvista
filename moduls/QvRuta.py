#imports
import xml.etree.ElementTree as ET
import requests
from moduls.QvImports import *
from qgis.core import QgsPointXY
from qgis.gui import QgsMapCanvas, QgsRubberBand


def pintarRuta(trams,canvas):
    for tram in trams:
        points = []
        polylines = []
        polyline = QgsRubberBand(canvas, False)
        polylines.append(polyline)
        for point in tram.getCoords():
            points.append(QgsPoint(point))

        polyline.setToGeometry(QgsGeometry.fromPolyline(points), None)
        if (tram.getCirculable() == False):
            polyline.setColor(QColor(255, 0, 0))
        else:
            polyline.setColor(QColor(0, 0, 255))

        polyline.setWidth(3)

        for linia in polylines:
            linia.show()

        return polylines

class Gir():
    descripcio = ""
    coord = QgsPointXY() #Coordenada()

    def __init__(self,inp_coord,descr):
        """
        Pre: inp_coord és una coordenada inicialitzada
        Post: s'inicialitza la variable coord
        """
        self.coord = inp_coord
        self.descripcio = descr

    def getCoord(self):
        return self.coord

    def getDescription(self):
        return self.descripcio

class Tram():
    circulable = False #boolean
    coords = []

    def __init__(self,circulable,coords):
        """
        Pre: coords és una array de coordenades
        Post: s'inicialitza la variable coord
        """
        self.circulable = circulable
        self.coords = coords

    def getCoords(self):
        return self.coords

    def getCirculable(self):
        return self.circulable

class Ruta():
    ruta_calculada = False

    coordInici = QgsPointXY()
    coordInici_descripcio = ""
    coordFinal = QgsPointXY()
    coordFinal_descripcio = ""

    girsRuta = [] #array de Gir
    tramsRuta = [] #array de Tram
    distanciaRuta = 0
    duradaRuta = 0

    coord_Final_descripcio = ""

    def __init__(self, coordA, coordB):
        """ 
        Pre: coordA i coordB són instàncies de la classe QgsPointXY
        Post: s'inicialitzen les variables coordInici i coordFinal
        """
        #comprovacions coordenades?

        self.coordInici = coordA
        self.coordFinal = coordB

        self.tramsRuta.clear()
        self.girsRuta.clear()

    def calculaRuta(self):
        """ 
        Pre: coordInici i coordFi han estat establerts i són a Barcelona.
        Post: es defineixen la resta d'atributs de la classe
        comprovar que missatgeResultat sigui OK
        """
        def readLocalXML(filename):
            with open(filename, 'r') as file:
                data = file.read().replace('\n', '')
            return data

        def readRemoteXML(URL):
            """
                Cal especificar que s'accepta només xml com a resposta. Per defecte torna JSON.
            """
            headers = {
                "Accept": "application/xml",
            }
            var = requests.get(URL,headers=headers).text
            return var 

        def parseXML(content):
            root = ET.fromstring(content)

            ns = {'nsruta': 'http://schemas.datacontract.org/2004/07/RutesSrv.Controllers', 'd2p1': 'http://schemas.microsoft.com/2003/10/Serialization/Arrays'}

            if (int(root.find("nsruta:codiResultat",ns).text) != 0):
                print("XML parse error")

            self.coordInici_descripcio = root.find("nsruta:sortida",ns).find("nsruta:descripcio",ns).text
            self.coordFinal_descripcio = root.find("nsruta:arribada",ns).find("nsruta:descripcio",ns).text

            self.distanciaRuta = int(root.find("nsruta:distancia",ns).text)
            self.duradaRuta = int(root.find("nsruta:durada",ns).text)

            for index,gir in enumerate(root.find("nsruta:girs",ns).findall("nsruta:Gir",ns)):
                temp_coord = QgsPointXY(float(gir.find("nsruta:coord",ns).find("nsruta:x",ns).text), float(gir.find("nsruta:coord",ns).find("nsruta:y",ns).text))
                descr = root.find("nsruta:descripcio",ns).findall("d2p1:string",ns)[index+1].text
                self.girsRuta.append(Gir(temp_coord,descr.split(" - ")[1]))

            for tram in root.find("nsruta:trams",ns).findall("nsruta:Tram",ns):
                coords = []
                circulable = False

                str_circulable = tram.find("nsruta:circulable",ns).text

                if (str_circulable == "true"):
                    circulable = True
                
                for tramcoord in tram.find("nsruta:coords",ns).findall("nsruta:Coord",ns):
                    temp_coord = QgsPointXY(float(tramcoord.find("nsruta:x",ns).text), float(tramcoord.find("nsruta:y",ns).text))
                    coords.append(temp_coord)

                self.tramsRuta.append(Tram(circulable,coords))

        URL = "http://netiproa.corppro.imi.bcn:81/karta/api/Ruta/Utm/" + str(self.coordInici.x()) + "/" + str(self.coordInici.y()) + "/" + str(self.coordFinal.x()) + "/" + str(self.coordFinal.y()) + "/EPSG:25831"

        #filecontent = readRemoteXML(URL)
        filecontent = readLocalXML(r"C:/QVista/ruta1.xml")

        parseXML(filecontent)


    def obtenirRuta(self):
        """ Pre: la ruta ja ha estat calculada. project és un QgsMapCanvas
        """

        return self.tramsRuta

    #def mostrarLlegenda(window? qwidget?):
        """ Pre: la ruta ha estat calculada
        """

    def obtenirPuntsGir(self):
        return self.girsRuta


if __name__ == "__main__":
    projecteInicial='mapesOffline/qVista default map.qgs'
    with qgisapp():
        canvas=QgsMapCanvas()
        canvas.setContentsMargins(0,0,0,0)
        project=QgsProject().instance()
        root=project.layerTreeRoot()
        bridge=QgsLayerTreeMapCanvasBridge(root,canvas)
        bridge.setCanvasLayers()

        # llegim un projecte de demo

        project.read(projecteInicial)
        
        ruta = Ruta(QgsPointXY(434799.933, 4584672.930),QgsPointXY(433463.058, 4583356.121))
        ruta.calculaRuta()
        pintarRuta(ruta.obtenirRuta(),canvas)
        canvas.show()