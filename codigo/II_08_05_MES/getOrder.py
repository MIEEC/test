import xml.etree.ElementTree as ET
import datetime
from basedados import basedados_inserir_ordem

def receber_ordem():
    #print("xml recebido")
    tree = ET.parse('command3.xml')                                                     
    root = tree.getroot()
    #separar o xml recebido
    for order in root: #can be a order(transform ou unload) or a upload
        hora_entrada_ordem = datetime.datetime.now()
        hora_inicio_ordem=' '
        hora_fim_ordem=' '
        if(order.tag == 'Request_Stores'):
            print('Ordem de carga')
            ##  ----------- manda a ordem de carga para o PLC ?? --------- ######
        elif(order.tag == 'Order'):
            numero_de_ordem = order.get('Number')
            #print('numero de ordem: ' + numero_de_ordem)
            for transform in order.iter('Transform'):
                tipo_de_ordem = str(transform.tag)
                #print('tipo de ordem: '+  tipo_de_ordem)
                peca_inicial = transform.get('From')
                peca_final = transform.get('To')
                destino='--'
                # print('Transformar P'+peca_inicial[1]+ ' em P'+ peca_final[1])
                quantidade = transform.get('Quantity')
                # print('Numa quantidade: '+ quantidade)
                # print()
              
         
    
            for unload in order.iter('Unload'):
                tipo_de_ordem = str(unload.tag)
                #print('tipo de ordem: '+  tipo_de_ordem)
                peca_inicial = unload.get('Type')
                peca_final= '--'
                #print('Unload da P'+peca_inicial[1])
                #destino = unload.get('Destination')
                #print('Para o destino: '+ destino[1])
                quantidade = unload.get('Quantity')
                #print('Numa quantidade: '+ quantidade)
                #print()

            basedados_inserir_ordem(numero_de_ordem, tipo_de_ordem, quantidade, peca_inicial, peca_final, destino, hora_entrada_ordem, hora_inicio_ordem, hora_fim_ordem)

    return