from qgis.core import QgsPointXY
from qgis.PyQt import QtCore
from qgis.PyQt.QtCore import QObject, pyqtSignal, QSortFilterProxyModel
from qgis.PyQt.QtGui import QValidator
from qgis.PyQt.QtWidgets import QCompleter
import sys
import csv
import collections
import unicodedata
import re
import csv
from PyQt5.QtSql import *
from moduls.QvApp import QvApp
from moduls.QvBafarada import QvBafarada


def encaixa(sub,string):
    '''Retorna True si alguna de les paraules de sub encaixa exactament dins de string (és a dir, a sub hi ha "... xxx ..." i a string també) i la resta apareixen però no necessàriament encaixant'''
    string=string.lower()
    # pos=string.find(chr(29))
    # string=string[:pos]
    subs=sub.split(' ')
    words=string.split(' ')
    encaixaUna=False
    for x in subs:
        if len(x)<3: continue #no té sentit si escrius "av d" que et posi a dalt de tot el Carrer d'Aiguablava perquè la d encaixa exactament amb una paraula
        if x not in string: return False #Un dels substrings de la cerca no apareix dins de l'adreça
        if x in words: encaixaUna=True #Hem trobat una que encaixa
    return encaixaUna

def conte(sub, string):
    '''Retorna true si string conté tots els strings representats a subs '''
    string=string.lower()
    subs=sub.split(' ')
    for x in subs:
        if x not in string:
            return False
    return True

def comenca(sub,string):
    '''Retorna True si alguna de les paraules de string comença per alguna de les paraules de sub'''
    string=string.lower()
    subs=sub.split(' ')
    comencaUna=False
    for x in subs:
        if x=='': 
            continue
        trobat=(x in string)
        if not trobat: return False
        #Si ja hem trobat que comença amb una no cal tornar a comprovar-ho. Seguim iterant només perquè la resta han d'estar contingudes
        if not comencaUna and re.search(' '+x,' '+string) is not None:
            comencaUna=True
    return comencaUna

def variant(sub,string,variants):
    #TODO: Fer test de velocitat. Si va massa lent, busquem simplement que sub estigui dins d'una variant
    subs=sub.split(' ')
    for x in variants.split(','):
        esVariant=True
        for y in subs:
            if y not in x:
                esVariant=False
                break
        if esVariant: 
            return True
    return False


class CompleterAdreces(QCompleter):
    def __init__(self,elems,widget):
        super().__init__(elems, widget)
        #self.elements=elems
        #Tindrem un diccionari on la clau serà el carrer i el valor les variants
        aux=[x.split(chr(29)) for x in elems]
        self.variants={x[0]:x[1].lower() for x in aux} 
        self.elements=list(self.variants.keys())
        self.le=widget
        # Aparellem cada carrer amb el rang del seu codi
        aux=zip(self.obteRangCodis(),self.elements)
        # Creem un diccionari que conté com a clau el nom del carrer i com a valor el codi
        # Així podrem ordenar els carrers en funció d'aquests codis
        self.dicElems={y:y[x[0]:x[1]] for x, y in aux}
        self.popup().selectionModel().selectionChanged.connect(self.seleccioCanviada)
        self.modelCanviat=False
    def obteRangCodis(self):
        #Fem servir una expressió regular per buscar el rang dels codis. Creem un generador que conté el resultat
        return (re.search("\([0-9]*\)",x).span() for x in self.elements)
    def seleccioCanviada(self,nova,antiga):
        text=self.popup().currentIndex().data()
        ind=text.find(chr(30))
        if ind!=-1:
            text=text[:ind-1]
        self.le.setText(text.strip())
        # print(text)
    def update(self,word):
        '''Funció que actualitza els elements'''
        if len(word)<3 and self.modelCanviat: 
            self.model().setStringList(self.elements)
            self.modelCanviat=False
            return
        self.word=word.lower()
        
        # Volem dividir la llista en cinc llistes
        # -Carrers on un dels elements cercats encaixen amb una paraula del carrer
        # -Carrers on una de les paraules del carrer comencen per un dels elements cercats
        # -Carrers que contenen les paraules cercades
        # -Carrers que tenen una variant que contingui les paraules cercades
        # -La resta
        # Podria semblar que la millor manera és crear quatre llistes, fer un for, una cadena if-then-else i posar cada element en una de les quatre. Però això és molt lent 
        # Aprofitant-nos de que les coses definides per python són molt ràpides (ja que es programen en C) podem resoldre el problema utilitzant funcions d'ordre superior i operacions sobre sets
        # Bàsicament farem servir filter per filtrar els elements que compleixen la funció, desar-los, i els extreurem dels restants.



        altres=set(self.elements)
        encaixen=set(filter(lambda x: encaixa(self.word,x), altres))
        altres=altres-encaixen
        comencen=set(filter(lambda x: comenca(self.word,x),altres))
        altres=altres-comencen
        contenen=set(filter(lambda x: conte(self.word,x), altres))
        altres=altres-contenen
        variants=set(filter(lambda x: variant(self.word,x,self.variants[x]), altres))
        
        
        ordenacio=lambda x: self.dicElems[x]
        #No mola posar-li les variants al string, però el completer ho necessita
        variants=[x+chr(29)+self.variants[x] for x in variants] 
        self.model().setStringList(sorted(encaixen,key=ordenacio)+sorted(comencen,key=ordenacio)+sorted(contenen,key=ordenacio)+sorted(variants))
        self.m_word=word
        self.complete()
        self.modelCanviat=True
    def splitPath(self,path):
        self.update(path)
        res=path.split(' ')
        return [res[-1]]

class ValidadorNums(QValidator):
    '''NO UTILITZADA. Serviria per poder impedir que es posin números no existents per l'adreça'''
    def __init__(self,elems,parent):
        super().__init__(parent)
        self.permesos=elems.keys()
    def validate(self,input,pos):
        if input in self.permesos:
            return QValidator.Acceptable, input, pos
        filt=filter(lambda x: x.startswith(input), self.permesos)
        if any(True for _ in filt):
            return QValidator.Intermediate, input, pos
        return QValidator.Invalid, input, pos



        

class QCercadorAdreca(QObject):

    # __carrersCSV = 'dades\Carrers.csv'

    __CarrersNum_sqlite='Dades\CarrersNums.db' #???

    sHanTrobatCoordenades = pyqtSignal(int, 'QString')  # atencion

    def __init__(self, lineEditCarrer, lineEditNumero, origen = 'SQLITE'):
        super().__init__()
       
        # self.pare= pare

        self.origen = origen
        self.leCarrer = lineEditCarrer
        self.leNumero = lineEditNumero
        self.connectarLineEdits()
        self.carrerActivat = False

        self.dictCarrers = {}
        self.dictNumeros = collections.defaultdict(dict)

        # self.db = QSqlDatabase.addDatabase('QSQLITE', 'CyN') # Creamos la base de datos
        # self.db.setDatabaseName(self.__CarrersNum_sqlite) # Le asignamos un nombre


        # self.db.setConnectOptions("QSQLITE_OPEN_READONLY")

        self.db= QvApp().dbGeo
        
        if self.db is None:   #not self.db.open(): # En caso de que no se abra
            QMessageBox.critical(None, "Error al abrir la base de datos.\n\n"
                    "Click para cancelar y salir.", QMessageBox.Cancel)

        self.query = QSqlQuery(self.db) # Intancia del Query
        self.txto =''
        self.calle_con_acentos=''
        self.habilitaLeNum()



        self.iniAdreca()

        if self.llegirAdreces():
            # si se ha podido leer las direciones... creando el diccionario...
            self.prepararCompleterCarrer()

    def habilitaLeNum(self):
        self.carrerActivat=False
        return #De moment no es desactivarà mai
        #Hauria de funcionar només amb la primera condició, però per raons que escapen al meu coneixement, no anava :()
        self.leNumero.setEnabled(self.calle_con_acentos!='' or self.txto!='')

    def cercadorAdrecaFi(self):
        if self.db.isOpen():
            self.db.close()

    def prepararCompleterCarrer(self):
        # creo instancia de completer que relaciona diccionario de calles con lineEdit
        # self.completerCarrer = QCompleter(self.dictCarrers, self.leCarrer)
        self.completerCarrer = CompleterAdreces(self.dictCarrers, self.leCarrer)
        # Determino funcionamiento del completer
        self.completerCarrer.setFilterMode(QtCore.Qt.MatchContains)
        self.completerCarrer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        # Funcion que se ejecutará cuando 
        self.completerCarrer.activated.connect(self.activatCarrer)
        # Asigno el completer al lineEdit
        self.leCarrer.setCompleter(self.completerCarrer)   

    def prepararCompleterNumero(self):
        self.dictNumerosFiltre = self.dictNumeros[self.codiCarrer]
        self.completerNumero = QCompleter(self.dictNumerosFiltre, self.leNumero)
        self.completerNumero.activated.connect(self.activatNumero)
        self.completerNumero.setFilterMode(QtCore.Qt.MatchStartsWith)
        self.completerNumero.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.leNumero.setCompleter(self.completerNumero)  
        # self.leNumero.setValidator(ValidadorNums(self.dictNumeros[self.codiCarrer],self))


    def iniAdreca(self):
        self.iniAdrecaCarrer()
        self.iniAdrecaNumero()

    def iniAdrecaCarrer(self):
        self.nomCarrer = ''
        self.codiCarrer = ''

    def iniAdrecaNumero(self):
        self.numeroCarrer = ''
        self.coordAdreca = None
        self.infoAdreca = None

    def connectarLineEdits(self):
        self.leCarrer.textChanged.connect(self.esborrarNumero)
        self.leCarrer.editingFinished.connect(self.trobatCarrer)
        self.leCarrer.mouseDoubleClickEvent = self.clear_leNumero_leCarrer
        self.leCarrer.setAlignment(Qt.AlignLeft)

        self.leNumero.editingFinished.connect(self.trobatNumero)
        # self.leNumero.returnPressed.connect(self.trobatNumero)

    def clear_leNumero_leCarrer(self, carrer):
        self.carrerActivat=False
        self.leNumero.clear()
        self.leCarrer.clear()

    # Venimos del completer, un click en desplegable ....
    def activatCarrer(self, carrer):
        self.carrerActivat = True
        # print(carrer)

        nn= carrer.find(chr(30))
        if nn==-1:
            ss=carrer
        else:
            ss= carrer[0:nn-1]

        self.calle_con_acentos=ss.rstrip()

        self.leCarrer.setAlignment(Qt.AlignLeft)  
        self.leCarrer.setText(self.calle_con_acentos)


        # self.leCarrer.setText(carrer)
        self.iniAdreca()
        if carrer in self.dictCarrers:
            self.nomCarrer = carrer
            self.codiCarrer = self.dictCarrers[self.nomCarrer]



            try:
                index = 0
                # self.query = QSqlQuery() # Intancia del Query
                # self.query.exec_("select codi, num_lletra_post, etrs89_coord_x, etrs89_coord_y, num_oficial  from Numeros where codi = '" + self.codiCarrer +"'")

                self.query.exec_("select codi,case num_lletra_post when '0' then ' ' else num_lletra_post end,  etrs89_coord_x, etrs89_coord_y, num_oficial  from Numeros   where codi = '" + self.codiCarrer +"'")   
                # self.query.exec_("select codi,case num_lletra_post when '0' then ' ' else num_lletra_post end,  etrs89_coord_x, etrs89_coord_y, case num_oficial when '0' then ' ' else num_oficial end  from Numeros   where codi = '" + self.codiCarrer +"'")   



                while self.query.next():
                    row= collections.OrderedDict()
                    row['NUM_LLETRA_POST']=  self.query.value(1) # Numero y Letra
                    row['ETRS89_COORD_X']=   self.query.value(2) # coor x
                    row['ETRS89_COORD_Y']=   self.query.value(3) # coor y
                    row['NUM_OFICIAL']=      self.query.value(4) # numero oficial

                    self.dictNumeros[self.codiCarrer][self.query.value(1)] = row
                    index += 1

                self.query.finish()
                # self.db.close()
    
                self.prepararCompleterNumero()
                self.focusANumero()
                
            except Exception as e:
                print(str(e))
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                
                msg.setText(str(sys.exc_info()[1]))
                # msg.setInformativeText("OK para salir del programa \nCANCEL para seguir en el programa")
                msg.setWindowTitle("qVista ERROR")
                msg.setStandardButtons(QMessageBox.Close)
                retval = msg.exec_() #No fem res amb el valor de retorn (???)

                print('QCercadorAdreca.iniAdreca(): ', sys.exc_info()[0], sys.exc_info()[1])
                return False
            else:
                pass

            
        else:
            info= "ERROR >> [1]" 
            self.sHanTrobatCoordenades.emit(1,info) #adreça vacia
        self.habilitaLeNum()
        # self.prepararCompleterNumero()
        # self.focusANumero()

    def trobatCarrer(self):
        if self.leCarrer.text()=='': 
            self.leNumero.setCompleter(None)
            return
        if not self.carrerActivat:
            # print(self.leCarrer.text())
            #així obtenim el carrer on estàvem encara que no l'haguem seleccionat explícitament
            self.txto=self.completerCarrer.popup().currentIndex().data()
            if self.txto is None:
                self.txto = self.completerCarrer.currentCompletion()
            if self.txto=='': 
                return

            nn= self.txto.find(chr(30))
            if nn==-1:
                ss=self.txto
            else:
                ss= self.txto[0:nn-1]

            # ss= self.txto[0:nn-1]
            self.calle_con_acentos=ss.rstrip()

            self.leCarrer.setAlignment(Qt.AlignLeft)  
            self.leCarrer.setText(self.calle_con_acentos)

            self.iniAdreca()
            if self.txto != self.nomCarrer:
                # self.iniAdreca()
                if self.txto in self.dictCarrers:
                    self.nomCarrer = self.txto
                    self.codiCarrer = self.dictCarrers[self.nomCarrer]
                    self.focusANumero()


                    try:
                        index = 0
                        # self.query = QSqlQuery() # Intancia del Query
                        # self.query.exec_("select codi, num_lletra_post, etrs89_coord_x, etrs89_coord_y, num_oficial  from Numeros where codi = '" + self.codiCarrer +"'")
                        self.query.exec_("select codi,case num_lletra_post when '0' then ' ' else num_lletra_post end,  etrs89_coord_x, etrs89_coord_y, num_oficial  from Numeros   where codi = '" + self.codiCarrer +"'")   

                        while self.query.next():
                            row= collections.OrderedDict()
                            row['NUM_LLETRA_POST']=  self.query.value(1) # Numero y Letra
                            row['ETRS89_COORD_X']=   self.query.value(2) # coor x
                            row['ETRS89_COORD_Y']=   self.query.value(3) # coor y
                            row['NUM_OFICIAL']=      self.query.value(4) # numero oficial

                            self.dictNumeros[self.codiCarrer][self.query.value(1)] = row
                            index += 1
                        
                        self.query.finish()
                        # self.db.close()
                        self.prepararCompleterNumero()
                        self.focusANumero()
                        
                    except Exception as e:
                        print(str(e))
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Warning)
                        
                        msg.setText(str(sys.exc_info()[1]))
                        # msg.setInformativeText("OK para salir del programa \nCANCEL para seguir en el programa")
                        msg.setWindowTitle("qVista ERROR")
                        msg.setStandardButtons(QMessageBox.Close)
                        retval = msg.exec_() #No fem res amb el valor de retorn (???)

                        print('QCercadorAdreca.iniAdreca(): ', sys.exc_info()[0], sys.exc_info()[1])
                        return False

                else:
                    info="ERROR >> [2]"
                    self.sHanTrobatCoordenades.emit(2,info) #direccion no está en diccicionario
                    self.iniAdreca()
            else:
                info="ERROR >> [3]"
                self.sHanTrobatCoordenades.emit(3,info)    #nunca
        else:
            info="ERROR >> [4]"
            self.sHanTrobatCoordenades.emit(4,info) #adreça vac 
        self.habilitaLeNum() 
        

            
    def llegirAdreces(self):
        if self.origen == 'SQLITE':
            ok = self.llegirAdrecesSQlite()
        else:
            ok = False
        return ok

    def llegirAdrecesSQlite(self):
        try:
            index = 0
            # self.query = QSqlQuery() # Intancia del Query
            self.query.exec_("select codi , nom_oficial , variants  from Carrers") 

            while self.query.next():
                codi_carrer = self.query.value(0) # Codigo calle
                nombre = self.query.value(1) # numero oficial
                variants = self.query.value(2) #Variants del nom
                nombre_sin_acentos= self.remove_accents(nombre)
                if nombre == nombre_sin_acentos:
                    # clave= nombre + "  (" + codi_carrer + ")"
                    clave= nombre + "  (" + codi_carrer + ")                                                  "+chr(30)
                else:
                    clave= nombre + "  (" + codi_carrer + ")                                                  "+chr(30)+"                                                         " + nombre_sin_acentos
                    # asignacion al diccionario
                variants.replace(',',50*' ')
                clave+=chr(29)+50*' '+variants
                self.dictCarrers[clave] = codi_carrer
                
                index += 1
     
            self.query.finish()
            # self.db.close()
            return True
        except Exception as e:
            print(str(e))
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            
            msg.setText(str(sys.exc_info()[1]))
            # msg.setInformativeText("OK para salir del programa \nCANCEL para seguir en el programa")
            msg.setWindowTitle("qVista ERROR")
            msg.setStandardButtons(QMessageBox.Close)
            retval = msg.exec_() #No fem res amb el valor de retorn (???)

            print('QCercadorAdreca.llegirAdrecesSQlite(): ', sys.exc_info()[0], sys.exc_info()[1])
            return False



    # Normalización caracteres quitando acentos
    def remove_accents(self,input_str):
        nfkd_form = unicodedata.normalize('NFKD', input_str)
        only_ascii = nfkd_form.encode('ASCII', 'ignore')
        return only_ascii.decode("utf8")


    def activatNumero(self,txt):
        self.leNumero.setText(txt)
        self.iniAdrecaNumero()
        # if self.leCarrer.text() in self.dictCarrers:
        self.txto = self.completerCarrer.currentCompletion()
        if self.txto in self.dictCarrers:
            if  txt in self.dictNumerosFiltre:
                self.numeroCarrer = txt
                self.infoAdreca = self.dictNumerosFiltre[self.numeroCarrer]
                self.coordAdreca = QgsPointXY(float(self.infoAdreca['ETRS89_COORD_X']), \
                                            float(self.infoAdreca['ETRS89_COORD_Y']))

                self.NumeroOficial= self.infoAdreca['NUM_OFICIAL']
                self.leNumero.setText(self.NumeroOficial)
                self.leNumero.clearFocus()

                info="[0]"
                self.sHanTrobatCoordenades.emit(0,info)  
                if self.leNumero.text()==' ':
                    self.leNumero.clear()


        else :
            info="ERROR >> [5]"
            self.sHanTrobatCoordenades.emit(5,info)  #numero          

    def trobatNumero(self):
        #Si no hi ha carrer, eliminem el completer del número
        if self.leCarrer.text()=='':
            self.leNumero.setCompleter(None)
        if self.leNumero.text()=='':
            return
        # self.txto = self.completerCarrer.currentCompletion()
        try:
            # if self.leCarrer.text() in self.dictCarrers:
            if self.txto in self.dictCarrers:
                
                if self.leNumero.text() != '':
                    txt=self.completerNumero.popup().currentIndex().data()
                    if txt is None:
                        txt = self.completerNumero.currentCompletion()
                    # txt = self.completerNumero.currentCompletion()
                    self.leNumero.setText(txt)
                else:
                    txt = ' '

                if txt != '': # and txt != self.numeroCarrer:
                    self.iniAdrecaNumero()
                    if self.nomCarrer != '':
                        if  txt in self.dictNumerosFiltre:
                            self.numeroCarrer = txt
                            self.infoAdreca = self.dictNumerosFiltre[self.numeroCarrer]
                            self.coordAdreca = QgsPointXY(float(self.infoAdreca['ETRS89_COORD_X']), \
                                                        float(self.infoAdreca['ETRS89_COORD_Y']))
                            self.NumeroOficial= self.infoAdreca['NUM_OFICIAL']
                            self.leNumero.clearFocus()
                            self.leNumero.setText(self.NumeroOficial)
                            info="[0]"
                            self.sHanTrobatCoordenades.emit(0,info) 
                            if self.leNumero.text()==' ':
                                self.leNumero.clear()
               
                        else:
                            info="ERROR >> [6]"
                            self.sHanTrobatCoordenades.emit(6,info)  #numero no está en diccicionario
                    else:
                        info="ERROR >> [7]"
                        self.sHanTrobatCoordenades.emit(7,info) #adreça vacia  nunca
                else:
                    info="ERROR >> [8]"
                    self.sHanTrobatCoordenades.emit(8,info)   #numero en blanco
            else:
                self.leNumero.clear()
                info="ERROR >> [9]"
                self.sHanTrobatCoordenades.emit(9,info)   #numero en blanco
        except: 
            return
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            info_rsc= 'ERROR: '+ str(sys.exc_info()[0])
            msg.setText(info_rsc)
            # msg.setInformativeText("OK para salir del programa \nCANCEL para seguir en el programa")
            msg.setWindowTitle("qVista >> QVCercadorAdreca>> trobatNumero")
            
            msg.setStandardButtons(QMessageBox.Close)
            retval = msg.exec_() #No fem res amb el valor de retorn (???)

    def focusANumero(self):
        self.leNumero.setFocus()

    def esborrarNumero(self):
        # self.carrerActivat = False
        self.calle_con_acentos=''
        self.leNumero.clear()
        #self.leNumero.setCompleter(None)


from moduls.QvImports import *
if __name__ == "__main__":
    projecteInicial='projectes/BCN11_nord.qgs'

    with qgisapp() as app:
        app.setStyle(QStyleFactory.create('fusion'))

        canvas = QgsMapCanvas()
        canvas.setGeometry(10,10,1000,1000)
        canvas.setCanvasColor(QColor(10,10,10))
        le1 = QLineEdit()
        le2 = QLineEdit()
        le1.setWindowTitle("Calle")
        le1.show()
        le2.setWindowTitle("Numero")
        le2.show()

        QCercadorAdreca(le1, le2)
        project= QgsProject().instance()
        root = project.layerTreeRoot()
        bridge = QgsLayerTreeMapCanvasBridge(root, canvas)

        project.read(projecteInicial)

        canvas.show()