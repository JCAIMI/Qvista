import sys
import pydoc
import importlib

my_module = importlib.import_module('QvMapeta')
request=my_module.QvMapeta
# moduleName = ['QvMapeta'] 
# modul = map(__import__, moduleName)

# import my_module

def output_help_to_file(filepath, request):
    """
    Funcion help_to_file
    muy guapa por cierto
    """
    # f = open(filepath, 'a+')
    f = open(filepath, 'w')
    sys.stdout = f
    # pydoc.help(request)
    help(request)
    f.close()
    sys.stdout = sys.__stdout__
    return



# output_help_to_file(r'QvMapeta.txt',QvMapeta.QvMapeta)
output_help_to_file(r'QvMapeta.txt',request)



