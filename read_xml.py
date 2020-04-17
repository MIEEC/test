import xml.etree.ElementTree as ET

tree = ET.parse('command4.xml')                                                     #Faz o parse do ficheiro a ler
root = tree.getroot()                                                               #Encontra o Elemento
length = len(tree.findall('Order'))                                                 #Dá o numero de ordens

#Definição dos arrays onde a info vai ser guardada
get_order, get_from, get_to, get_quant, get_delay, get_unload, get_destination = ["" for x in range(length)],  ["" for x in range(length)], ["" for x in range(length)], ["" for x in range(length)], ["" for x in range(length)], ["" for x in range(length)], ["" for x in range(length)]
x=0

for child in root:                                                                  #O order number é obtido no root
     get_order.insert(x,child.attrib.get('Number')) and                             #Ciclo for que guarda o order number no devido array na Posição x (q esta definida como 0 logo a primeira)

for i in range(length):                                                             #root[0] equivale aos sub-elementos da primeira order number
     for child in root[i]:                                                          #root[1] equivale aos sub-elementos da segunda order number e por ai em diante
          x=length-i-1                                                              #As order number no print em baixo estavam a dar ao contrario, assim inverte a ordem
          get_from.insert(i,child.attrib.get('From'))                               # No array get_from estamos a inserir na posição i o atributo que obtemos ao procurar por ('From') no root[i] respetivo
          get_to.insert(i,child.attrib.get('To'))
          get_quant.insert(i,child.attrib.get('Quantity'))
          get_delay.insert(i,child.attrib.get('MaxDelay'))
          get_unload.insert(i,child.attrib.get('Type'))
          get_destination.insert(i,child.attrib.get('Destination'))
          print("Order Number:%s\nTransform from:%s\nTo:%s\nQuantity:%s\nMaxDelay:%s\nUnload Type:%s\nDestination:%s\n" %
             (get_order[x],get_from[i], get_to[i], get_quant[i], get_delay[i],get_unload[i],get_destination[i]))
