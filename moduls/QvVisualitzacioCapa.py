# -*- coding:utf-8 -*-

from PyQt5 import QtCore, QtGui,QtWidgets

from dlgLayerProperties_ui import Ui_LayerProperties

class QvVisualitzacioCapa( QtWidgets.QDialog, Ui_LayerProperties ):
    """ Open a dialog to manage the layer properties """
    def __init__( self, parent, layer ):
        self.parent = parent
        QtWidgets.QDialog.__init__( self, self.parent )
        self.setupUi( self )
        self.layer = layer
        self.updateControls()
        # self.connect( self.chkScale, SIGNAL( "stateChanged(int)" ), self.chkScaleChanged )
        self.chkScale.stateChanged.connect(self.chkScaleChanged)
        self.accepted.connect(self.apply )
        self.rejected.connect(self.close )
        self.sliderTransparencia.setValue(100-self.layer.opacity()*100)
        self.sliderTransparencia.valueChanged.connect(self.transparencia)

    def transparencia(self):
        self.layer.setOpacity((100-self.sliderTransparencia.value())/100)
        self.layer.triggerRepaint()

    def updateControls(self):  
        self.txtLayerName.setText( self.layer.name() )

        if self.layer.type() == 0: # Vector Layer
            self.lblDisplayField.setVisible( True )
            self.cboDisplayFieldName.setVisible( True )
            self.cboDisplayFieldName.setEnabled( True )

            self.fields = self.layer.fields()

            self.cboDisplayFieldName.addItem("Sense etiquetes")
            self.cbTipField.addItem("Sense etiquetes")
            for field in self.fields:
                #if not field.type() == QVariant.Double:
                    # self.displayName = self.vectorLayer.attributeDisplayName( key )
                self.cboDisplayFieldName.addItem( field.name() )
                self.cbTipField.addItem( field.name() )

            # self.fields = self.layer.fields()
            # self.cboDisplayFieldName.addItem("Sense etiquetes")
            # for field in self.fields:
            #     #if not field.type() == QVariant.Double:
            #         # self.displayName = self.vectorLayer.attributeDisplayName( key )
            #     self.cboDisplayFieldName.addItem( field.name() )
            print(self.layer.displayField())
            idx = self.cboDisplayFieldName.findText( self.layer.displayField() )
            self.cboDisplayFieldName.setCurrentIndex( idx )
        else:
            self.lblDisplayField.setVisible( False )
            self.cboDisplayFieldName.setVisible( False )
            self.cboDisplayFieldName.setEnabled( False )

        self.cboDisplayFieldName.currentTextChanged.connect(self.fieldCanviat)
        self.cbTipField.currentTextChanged.connect(self.tipFieldCanviat)
            
        if self.layer.hasScaleBasedVisibility():
            self.chkScale.setCheckState(QtCore.Qt.Checked )
            self.chkScaleChanged( 1 ) 
            self.initialScaleDependency = True
        else:
            self.chkScale.setCheckState( QtCore.Qt.Unchecked )
            self.chkScaleChanged( 0 ) 
            self.initialScaleDependency = False

        self.initialMaxScale = self.layer.minimumScale() # To know if refresh the canvas
        self.initialMinScale = self.layer.maximumScale()
        self.maxScaleSpinBox.setValue( self.layer.minimumScale() )
        self.minScaleSpinBox.setValue( self.layer.maximumScale() )

    def tipFieldCanviat(self):
        layer = self.parent.llegenda.currentLayer()
        if layer is not None:
            if self.cbTipField.currentText() != 'Sense etiqueta':
                layer.setDisplayExpression(self.cbTipField.currentText())
            else:
                # Desactivar tooltips
                pass

    def fieldCanviat(self):
        if self.cboDisplayFieldName.currentText() != 'Sense etiqueta':
            self.parent.pintaLabels(self.cboDisplayFieldName.currentText())

    def chkScaleChanged( self, state ):
        """ Slot. """
        if state:
            self.lblMaxScale.setEnabled( True )
            self.lblMinScale.setEnabled( True )
            self.maxScaleSpinBox.setEnabled( True )
            self.minScaleSpinBox.setEnabled( True )            
        else:
            self.lblMaxScale.setEnabled( False )
            self.lblMinScale.setEnabled( False )
            self.maxScaleSpinBox.setEnabled( False )
            self.minScaleSpinBox.setEnabled( False )            

    def apply( self ):            
        """ Apply the new symbology to the vector layer """
        newLayerName = self.txtLayerName.text()
        if newLayerName:
            if not newLayerName == self.layer.name():
                self.layer.setLayerName( newLayerName )
                self.emit( SIGNAL( "layerNameChanged(PyQt_PyObject)" ), self.layer )

        # if self.cboDisplayFieldName.isEnabled():
        # self.layer.setDisplayField( self.cboDisplayFieldName.currentText() )

        if self.chkScale.checkState() == QtCore.Qt.Checked:
            self.layer.setScaleBasedVisibility( True )
            self.layer.setMaximumScale( self.minScaleSpinBox.value() )
            self.layer.setMinimumScale( self.maxScaleSpinBox.value() )
            finalScaleDependency = True
        else:
            self.layer.setScaleBasedVisibility( False )
            finalScaleDependency = False

        if ( not self.initialScaleDependency == finalScaleDependency ) or \
           ( finalScaleDependency and ( ( not self.initialMaxScale == self.maxScaleSpinBox.value() ) or \
            ( not self.initialMinScale == self.minScaleSpinBox.value() ) ) ):
            self.parent.canvas.refresh() # Scale dependency changed, so refresh

    def mostrar( self ):
        """ Show the modal dialog """
        self.exec_()
