from moduls.QvImports import *
from moduls.QvConstants import QvConstants
class QvMenuBar(QMenuBar):
    '''Classe per fer que la menubar del qVista faci arrossegable el programa
    '''
    def __init__(self,parent: QWidget=None):
        super().__init__(parent)
        self.setContextMenuPolicy(Qt.PreventContextMenu)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button()==Qt.LeftButton:
            self.parentWidget().oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if event.buttons() & Qt.LeftButton:
            delta = QPoint(event.globalPos() - self.parentWidget().oldPos)
            if abs(delta.y())<15: return
            if self.parentWidget().maximitzada:
                self.parentWidget().restaurarFunc()
                #Desmaximitzar
            # print(delta)
            self.parentWidget().move(self.parentWidget().x() + delta.x(), self.parentWidget().y() + delta.y())
            self.parentWidget().oldPos = event.globalPos()
            
    def mouseDoubleClickEvent(self,event):
        super().mouseDoubleClickEvent(event)
        if event.button()==Qt.LeftButton:
            self.parentWidget().restaurarFunc()
    def enterEvent(self,event):
        super().enterEvent(event)
        self.setCursor(QvConstants.cursorClick())
    def leaveEvent(self,event):
        super().leaveEvent(event)
        self.setCursor(QvConstants.cursorFletxa())