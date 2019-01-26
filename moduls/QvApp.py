# -*- coding: utf-8 -*-

from qgis.PyQt.QtSql import QSqlDatabase, QSqlQuery
from qgis.PyQt.QtCore import QTranslator, QLibraryInfo
from qgis.PyQt.QtNetwork import QNetworkProxy
from moduls.QvSingleton import Singleton
from pathlib import Path
from moduls.QvGithub import QvGithub
import sys
import getpass
import uuid
import traceback
import os
import json

_PATH_PRO = 'N:\\SITEB\\APL\\PYQGIS\\QVISTA\\CODI\\'

_PATH_HELP = 'help/'

_DB_QVISTA = dict()

_DB_QVISTA['DSV'] = {
    'Database': 'QOCISPATIAL',
    'HostName': 'GEOPP1.imi.bcn',
    'Port': 1551,
    'DatabaseName': 'GEOPP1',
    'UserName': 'QVISTA_CONS',
    'Password': 'QVISTA_CONS'
}

_DB_QVISTA['PRO'] = {
    'Database': 'QOCISPATIAL',
    'HostName': 'GEOPR1.imi.bcn',
    'Port': 1551,
    'DatabaseName': 'GEOPR1',
    'UserName': 'QVISTA_CONS',
    'Password': 'QVISTA_CONS'
}

_PROXY = {
    'HostName': 'iprx.imi.bcn',
    'Port': 8080
}

def _fatalError(type, value, tb):
    QvApp().bugFatalError(type, value, tb)
    
#     error = repr(traceback.format_tb(tb))
#     error = error[-1000:]
#     print('ERROR -', error)
#     QvApp().logRegistre('LOG_ERROR', error[-1000:])

sys.excepthook = _fatalError

class QvApp(Singleton):

    def __init__(self):
        if hasattr(self, 'ruta'): # Solo se inicializa una vez
            return
        
        self.ruta, self.rutaBase = self.calcRuta()  # Path de la aplicación
        self.cfg = self.readCfg()                   # Configuración de la instalación
        self.entorn = self.calcEntorn()             # 'DSV' o 'PRO'
        
        self.usuari = getpass.getuser().upper()     # Id de usuario
        self.sessio = str(uuid.uuid1())             # Id único de sesión

        self.intranet = self.calcIntranet()         # True si estamos en la intranet
        self.dbQvista = _DB_QVISTA[self.entorn]     # Conexión a Oracle según entorno

        self.proxy = self.setProxy()                # Establecer proxy
        self.gh = QvGithub(self.data())             # Establecer Github

        self.dbLog = None
        self.queryLog = None
        self.familyLog = None
        self.nameLog = None
        self.appQgis = None
        self.idioma = None
        self.qtTranslator = None
        self.qgisTranslator = None

    def data(self):
        txt = ''
        txt += 'Nom: ' + self.cfg.get('Nom', '???') + '\n'
        txt += 'Entorn: ' + self.entorn + '\n'
        txt += 'Intranet: ' + str(self.intranet) + '\n'
        txt += 'Usuari: ' + self.usuari + '\n'
        txt += 'Sessió: ' + self.sessio + '\n'
        txt += '___' + '\n'
        return txt

    def calcRuta(self):
        try:
            q1 = 'qVista\\'
            q2 = 'Codi\\'
            f = sys.argv[0]
            q = q1 + q2
            n = f.find(q)
            if n >= 0:
                ruta = f[:n+len(q)]
                rutaBase = f[:n+len(q1)]
                return ruta, rutaBase
            else:
                return '', ''
        except:
            self.bugException()
            return '', ''

    def readCfg(self):
        try:
            nom = 'install.cfg'
            fich = self.rutaBase + nom
            if not os.path.isfile(fich):
                fich = self.ruta + nom
            fp = open(fich, 'r', encoding='utf-8')
            cfg = json.load(fp)
            fp.close()
            return cfg
        except:
            self.bugException()
            return dict()

    def setProxy(self):
        try:
            val = self.cfg.get('Proxy', 'False')
            if self.intranet and val == 'True':
                proxy = QNetworkProxy()
                proxy.setType(QNetworkProxy.DefaultProxy)
                proxy.setHostName = _PROXY['HostName']
                proxy.setPort = _PROXY['Port']
                proxy.setApplicationProxy(proxy)
                return proxy
            else:
                return None
        except Exception as e:
            self.bugException()
            return None
        
    def calcEntorn(self):
        val = self.cfg.get('Producció', 'False')
        if val == 'True':
            return 'PRO'
        else:
            return 'DSV'

    def calcIntranet(self):
        return os.path.isdir(_PATH_PRO)

    def carregaIdioma(self, app, idioma = 'ca'):
        if app is None:
            return
        self.appQgis = app
        self.idioma = self.cfg.get('Idioma', idioma)
        self.qtTranslator = QTranslator()
        self.qgisTranslator = QTranslator()

        path = QLibraryInfo.location(QLibraryInfo.TranslationsPath)
        self.qtTranslator.load("qt_" + idioma, path)
        app.installTranslator(self.qtTranslator)

        path = app.i18nPath()
        path = path.replace('/./', '/')
        self.qgisTranslator.load("qgis_" + idioma, path)
        app.installTranslator(self.qgisTranslator)

    def llegirFitxerText(self, nomFich):
        try:
            txt = ''
            file = Path(nomFich)
            if file.is_file():
                file.open() 
                txt = file.read_text()
            return txt
        except:
            return ''

    def carregaAjuda(self, objecte):
        try: 
            nom = type(objecte).__name__
            if self.idioma is not None and self.idioma != '':
                nomFich = nom + '_' + self.idioma + '.html'
            else:
                nomFich = nom + '.html'
            txt = self.llegirFitxerText(_PATH_HELP + nomFich)
            if txt == '':
                txt = self.llegirFitxerText(_PATH_HELP + 'WorkInProgress.html')
            return txt
        except Exception as e:
            print(str(e))
            return ''

    # Metodos de LOG en Oracle

    def logConnexio(self):
        try:
            val = self.cfg.get('Log', 'False')
            if self.intranet and val == 'True':
                db = QSqlDatabase.addDatabase(self.dbQvista['Database'])
                if db.isValid():
                    db.setHostName(self.dbQvista['HostName'])
                    db.setPort(self.dbQvista['Port'])
                    db.setDatabaseName(self.dbQvista['DatabaseName'])
                    db.setUserName(self.dbQvista['UserName'])
                    db.setPassword(self.dbQvista['Password'])
                    if db.open():
                        return db
            return None
        except:
            return None

    def logDesconnexio(self):
        if self.dbLog is None:
            return
        try:
            conName = self.dbLog.connectionName()
            self.dbLog.close()
            self.dbLog = None
            QSqlDatabase.removeDatabase(conName)
        except:
            return

    def logRegistre(self, topic, params = None):
        if self.dbLog is None or self.queryLog is None:
            return False
        try:
            self.queryLog.prepare("CALL QV_LOG_WRITE(:IDUSER, :IDSESSION, :FAMILY, :LOGNAME, :TOPIC, :PARAMS)")
            self.queryLog.bindValue(':IDUSER', self.usuari)
            self.queryLog.bindValue(':IDSESSION', self.sessio)
            self.queryLog.bindValue(':FAMILY', self.familyLog)
            self.queryLog.bindValue(':LOGNAME', self.nameLog)
            self.queryLog.bindValue(':TOPIC', topic)
            self.queryLog.bindValue(':PARAMS', params)
            ok = self.queryLog.exec_()
            return ok
        except:
            return False

    def logInici(self, family = 'QVISTA', logname = 'DESKTOP', params = None):
        self.familyLog = family.upper()
        self.nameLog = logname.upper()
        self.dbLog = self.logConnexio()
        if self.dbLog is None:
            return False
        else:
            self.queryLog = QSqlQuery()
            return self.logRegistre('LOG_INICI', params)

    def logFi(self, params = None):
        ok = self.logRegistre('LOG_FI', params)
        self.logDesconnexio()
        return ok

    def logError(self):
        if self.dbLog is None or self.queryLog is None:
            return None
        try:
            return self.queryLog.lastError().text()
        except:
            return None

    # Métodos de reporte de bugs con Github

    def bugUser(self, tit, desc):
        val = self.cfg.get('Github', 'False')
        if val == 'True':
            return self.gh.postUser(tit, desc)
        else:
            return False

    def bugException(self):
        val = self.cfg.get('Github', 'False')
        if val == 'True':
            return self.gh.reportBug()
        else:
            return False

    def bugFatalError(self, type, value, tb):
        val = self.cfg.get('Github', 'False')
        if val == 'True':
            return self.gh.reportBug(type, value, tb)
        else:
            return False

if __name__ == "__main__":

    print(sys.argv[0])

    from qgis.core.contextmanagers import qgisapp

    gui = False

    with qgisapp(guienabled = gui) as app:

        # print(QSqlDatabase.drivers())

        qApp = QvApp()                  # Singleton
        
        qApp.carregaIdioma(app, 'ca')   # Traductor

        #
        # INICIO LOG: Si logInici() retorna False, el resto de funciones de log no hacen nada
        #
        ok = qApp.logInici()            # Por defecto: family='QVISTA', logname='DESKTOP'
        if not ok:
            print('ERROR LOG >>', qApp.logError())

        ok = qApp.logRegistre('Capa1')
        ok = qApp.logRegistre('Atributs')

        ###########

        qApp2 = QvApp()  # qApp2 equivale a qApp
        ok = qApp2.logRegistre('Print', 'B/N;1:5000')
        ok = qApp2.logRegistre('PDF', 'Color;1:1000')

        ###########

        ok = QvApp().logRegistre('Capa2')

        aux = 3 / 0

        #
        # FIN LOG: Por evento si es un programa online, o por método si es un batch
        #
        if gui:
            app.aboutToQuit.connect(QvApp().logFi)
        else:
            QvApp().logFi()


        