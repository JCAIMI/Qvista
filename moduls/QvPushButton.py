from moduls.QvImports import * 
from moduls.QvConstants import QvConstants

class QvPushButton(QPushButton):
    def __init__(self, icon, text, destacat=False, parent=None):
        QPushButton.__init__(self,icon,text,parent)
        self.formata(destacat)
    def __init__(self, text='', destacat=False, parent=None):
        QPushButton.__init__(self,text,parent)
        self.formata(destacat)
    def formata(self,destacat):
        colors=(QvConstants.COLORBLANC,QvConstants.COLORFOSC)
        if destacat:
            colors=(QvConstants.COLORBLANC,QvConstants.COLORDESTACAT)
        self.setStyleSheet(
            "margin: 20px;"
            "border: none;"
            "padding: 5px 20px;"
            "color: %s;"
            "background-color: %s" % colors)
        self.setGraphicsEffect(QvConstants.ombraWidget())
        self.setFont(QvConstants.FONTTEXT)
    def setDestacat(self,destacat):
        self.formata(destacat)
    def enterEvent(self,event):
        QPushButton.enterEvent(self,event)
        self.setCursor(Qt.PointingHandCursor)
    def leaveEvent(self,event):
        QPushButton.leaveEvent(self,event)
        self.setCursor(Qt.ArrowCursor)