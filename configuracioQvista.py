import os

#Parametres configuració inicial

titolFinestra = 'qVista 0.1'

carpetaCataleg = "N:/9SITEB/Publicacions/qVista/CatalegProjectes/"
projecteInicial='n:/9siteb/publicacions/qvista/dades/projectes/bcn11_nord.qgs'

if not os.path.isdir(carpetaCataleg):
    carpetaCataleg = "../dades/CatalegProjectes/"
    projecteInicial = 'mapesOffline/DistrictesMartorell.qgz'
    