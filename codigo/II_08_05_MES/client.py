from opcua import Client
from opcua import ua
#import time

class conection():
    
    url = "opc.tcp://DESKTOP-O1K4I2D:4840"
    client = Client(url)
    client.connect()

    

def get_valor(string):
    local = "ns=4;s=|var|CODESYS Control Win V3 x64.Application.PLC_PRG." + string
    get_var = conection.client.get_node(local)
    return get_var.get_value()


def set_valor_bool(string, valor):
    local = "ns=4;s=|var|CODESYS Control Win V3 x64.Application.ID_PECA." + string
    set_var = conection.client.get_node(local)
    set_var.set_value(valor, ua.VariantType.Boolean)
    
    
def set_valor_int(string, valor): 
    local = "ns=4;s=|var|CODESYS Control Win V3 x64.Application.ID_PECA." + string
    set_var = conection.client.get_node(local)
    set_var.set_value(ua.Variant(valor, ua.VariantType.UInt16))

def set_valor_str(string, valor): 
    local = "ns=4;s=|var|CODESYS Control Win V3 x64.Application.ID_PECA." + string
    set_var = conection.client.get_node(local)
    set_var.set_value(ua.Variant(valor, ua.VariantType.String))