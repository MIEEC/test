import xml.etree.ElementTree as ET
import psycopg2
import datetime


def db_inserir_ordem(numero_de_ordem, tipo_de_ordem, quantidade, peca_inicial, peca_final, destino, hora_entrada_ordem):
    
    connection= psycopg2.connect(host="db.fe.up.pt", database="up201603858", user="up201603858", password="onr482mNS", port="5432")
    connection.autocommit= True
    cursor = connection.cursor()
    
    sql_insert_query = ("""INSERT INTO "Ordens" ("ID","Tipo","estado","pecas_processadas","pecas_em_processamento","pecas_pendentes","peca_inicial", "peca_final", "Destino", "hora_entrada_ordem") VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""")
    
    insert_tuple = (numero_de_ordem , tipo_de_ordem, 'pendente','0', '0', quantidade, peca_inicial, peca_final, destino, hora_entrada_ordem)
    
    cursor.execute(sql_insert_query, insert_tuple)
    
    connection.commit()
    
    connection.close()

    return


 
tree = ET.parse('command4.xml')                                                     
root = tree.getroot()

for order in root: #can be a order(transform ou unload) or a upload
    hora_entrada_ordem = datetime.datetime.now()

    if(order.tag == 'Request_Stores'):
        print('Ordem de carga')
        ##  ----------- manda a ordem de carga para o PLC ?? --------- ######
    elif(order.tag == 'Order'):
        numero_de_ordem = order.get('Number')
        print('numero de ordem: ' + numero_de_ordem)
        for transform in order.iter('Transform'):
            tipo_de_ordem = str(transform.tag)
            print('tipo de ordem: '+  tipo_de_ordem)
            peca_inicial = transform.get('From')
            peca_final = transform.get('To')
            destino=0
            print('Transformar P'+peca_inicial[1]+ ' em P'+ peca_final[1])
            quantidade = transform.get('Quantity')
            print('Numa quantidade: '+ quantidade)
            print()
          
     

        for unload in order.iter('Unload'):
            tipo_de_ordem = str(unload.tag)
            print('tipo de ordem: '+  tipo_de_ordem)
            peca = unload.get('Type')
            print('Unload da P'+peca_inicial[1])
            destino = unload.get('Destination')
            print('Para o destino: '+ destino[1])
            quantidade = unload.get('Quantity')
            print('Numa quantidade: '+ quantidade)
            
        
    db_inserir_ordem(numero_de_ordem, tipo_de_ordem, quantidade, peca_inicial, peca_final, destino, hora_entrada_ordem)
    print(destino)
 

print('conexao feita')



