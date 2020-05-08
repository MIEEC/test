import psycopg2
import functools 
from datetime import datetime

class Base_Dados():
    
    connection= psycopg2.connect(host="db.fe.up.pt", database="up201603858", user="up201603858", password="onr482mNS", port="5432")

    connection.autocommit= True
    cursor = connection.cursor()
    
    connection.commit()
    
    uid=1

#Insere uma ordem na basedados 
def basedados_inserir_ordem(numero_de_ordem, tipo_de_ordem, quantidade, peca_inicial, peca_final, destino, hora_entrada_ordem,hora_inicio_ordem, hora_fim_ordem):
    #conta o numero de linhas da tabela
    Base_Dados.cursor.execute("SELECT COUNT (*) FROM pedidos_pendentes")  
    n_pedidos_pendentes = 1+Base_Dados.cursor.fetchone()[0]
    
    #na tabela de Ordens
    sql_insert_query = ("""INSERT INTO "ordens" ("id", "ordem_id","Tipo","estado","pecas_processadas","pecas_em_processamento","pecas_pendentes","peca_inicial", "peca_final", "Destino", "hora_entrada_ordem", "hora_inicio_ordem", "hora_fim_ordem") VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s)""")
    insert_tuple = (n_pedidos_pendentes, numero_de_ordem , tipo_de_ordem, 'pendente','0', '0', quantidade, peca_inicial, peca_final, destino, hora_entrada_ordem, hora_inicio_ordem, hora_fim_ordem)
    Base_Dados.cursor.execute(sql_insert_query, insert_tuple)

    #na tabela de pedidos_pendentes
    sql_insert_query2 = ("""INSERT INTO "pedidos_pendentes" ("id", "order_id","peca_inicial", "peca_final", "quantidade_desejada", "destino", "tipo", "hora_entrada_ordem") VALUES (%s,%s,%s,%s,%s,%s,%s, %s)""")
    insert_tuple2 =(n_pedidos_pendentes, numero_de_ordem, peca_inicial, peca_final, quantidade, destino, tipo_de_ordem, hora_entrada_ordem )
    Base_Dados.cursor.execute(sql_insert_query2, insert_tuple2)

    return

def reinicia_armazem():
    
    sql_insert_query = ("""Update "inventario" set "p1" = 54 , "p2" = 54, "p3"=54, "p4"=54, "p5"=54, "p6"=54, "p7"=54, "p8"=54, "p9"=54  where "id" = 1""")
    
    Base_Dados.cursor.execute(sql_insert_query)

    return 

def pedidos_pendentes_tipo(i):
    
    PostgreSQL_select_Query = "select tipo from pedidos_pendentes WHERE id=" + str(i)
    Base_Dados.cursor.execute(PostgreSQL_select_Query)
    Proxima_ordem_tipo = Base_Dados.cursor.fetchone()
    Proxima_ordem_tipo =  ''.join(Proxima_ordem_tipo) #a função retorna um TUPLE. Com ''.join() é tranformado em STRING
    return Proxima_ordem_tipo


def pecas_pendentes_quantidade(i):
    PostgreSQL_select_Query = "select pecas_pendetes from ordens WHERE id=" + str(i)
    Base_Dados.cursor.execute(PostgreSQL_select_Query)
    Proxima_ordem_quantidade = Base_Dados.cursor.fetchone()
    Proxima_ordem_quantidade = functools.reduce(lambda sub, ele: sub * 10 + ele, Proxima_ordem_quantidade) 
    return Proxima_ordem_quantidade


def pedidos_pendentes_pi(i):
    PostgreSQL_select_Query = "select peca_inicial from pedidos_pendentes WHERE id=" + str(i)
    Base_Dados.cursor.execute(PostgreSQL_select_Query)
    Proxima_ordem_pi = Base_Dados.cursor.fetchone()
    Proxima_ordem_pi =  ''.join(Proxima_ordem_pi)
    return Proxima_ordem_pi


def pedidos_pendentes_pf(i):
    PostgreSQL_select_Query = "select peca_final from pedidos_pendentes WHERE id=" + str(i)
    Base_Dados.cursor.execute(PostgreSQL_select_Query)
    Proxima_ordem_pf = Base_Dados.cursor.fetchone()
    Proxima_ordem_pf =  ''.join(Proxima_ordem_pf)
    return Proxima_ordem_pf
    
    
def apagar_ordem_executada():
    deleteStatement = "DELETE FROM pedidos_pendentes WHERE id= (SELECT id FROM pedidos_pendentes order by id limit 1)"
    Base_Dados.cursor.execute(deleteStatement)
    
    
def nr_ordens_pendentes():
    query = "SELECT COUNT (*) FROM pedidos_pendentes"
    Base_Dados.cursor.execute(query)
    result = Base_Dados.cursor.fetchone()
    return result[0]
 
    
def seleciona_processo(pi, pf):
    query = "SELECT id from processo WHERE pi='" + pi + "' AND pf='" + pf + "'"
    Base_Dados.cursor.execute(query)
    result = Base_Dados.cursor.fetchone()
    result = functools.reduce(lambda sub, ele: sub * 10 + ele, result)
    return result


def seleciona_inventario(pi):
    query = "SELECT " + pi + " FROM inventario WHERE id=1"
    Base_Dados.cursor.execute(query)
    result = Base_Dados.cursor.fetchone()
    result = functools.reduce(lambda sub, ele: sub * 10 + ele, result) 
    return result


def ordem_a_processar(i):
    query = "UPDATE ordens SET estado = 'A Processar' WHERE id =" + str(i)
    Base_Dados.cursor.execute(query)
    

def ordem_suspenso(i):
    query = "UPDATE ordens SET estado = 'suspenso' WHERE id =" + str(i)
    Base_Dados.cursor.execute(query)


def hora_inicio_ordem(i):
    now = datetime.now()
    
    query = "UPDATE ordens SET hora_inicio_ordem = '" + str(now) + "' WHERE id =" + str(i)
    Base_Dados.cursor.execute(query)


def ordem_por_iniciar(i):
    query1 = "SELECT pecas_em_processamento FROM ordens WHERE id=" + str(i)
    query2 = "SELECT pecas_processadas FROM ordens WHERE id=" + str(i)
    
    #---BUSCAR NÚMERO DE PECAS EM PROCESSAMENTO-----
    Base_Dados.cursor.execute(query1)
    result1 = Base_Dados.cursor.fetchone()
    result1 = functools.reduce(lambda sub, ele: sub * 10 + ele, result1)
    
    #---BUSCAR NÚMERO DE PECAS PROCESSADAS-----
    Base_Dados.cursor.execute(query2)
    result2 = Base_Dados.cursor.fetchone()
    result2 = functools.reduce(lambda sub, ele: sub * 10 + ele, result2)
    
    #-----ESTÁ POR INICIAR SE AMBOS CONTADORES ESTIVEREM A 0-----
    if result1 == 0 and result2 == 0:
        return True
    else:
        return False
 
   
def hora_fim_ordem(i):
    now = datetime.now()
    
    query = "UPDATE ordens SET hora_fim_ordem = '" + str(now) + "' WHERE id =" + str(i)
    Base_Dados.cursor.execute(query)
    
        
def ferramenta(id_processo):
    query = "SELECT ferramenta FROM processo WHERE id=" + str(id_processo)
    Base_Dados.cursor.execute(query)
    result = Base_Dados.cursor.fetchone()
    result = functools.reduce(lambda sub, ele: sub * 10 + ele, result) 
    return result


def maquina(id_processo):
    query = "SELECT maquina FROM processo WHERE id=" + str(id_processo)
    Base_Dados.cursor.execute(query)
    result = Base_Dados.cursor.fetchone()
    result =  ''.join(result)
    return result


def tempo(id_processo):
    query = "SELECT tempo FROM processo WHERE id=" + str(id_processo)
    Base_Dados.cursor.execute(query)
    result = Base_Dados.cursor.fetchone()
    result = functools.reduce(lambda sub, ele: sub * 10 + ele, result) 
    return result


def atualizar_pecas_pendentes(i):
    query1 = "SELECT pecas_pendentes FROM ordens WHERE id=" + str(i)
    Base_Dados.cursor.execute(query1)
    quant = Base_Dados.cursor.fetchone()
    quant = functools.reduce(lambda sub, ele: sub * 10 + ele, quant) - 1
    
    query2 = "UPDATE ordens SET pecas_pendentes = " + str(quant) + "WHERE id =" + str(i)
    Base_Dados.cursor.execute(query2)
    
    
def atualizar_pecas_em_processamento(i):
    query1 = "SELECT pecas_em_processamento FROM ordens WHERE id=" + str(i)
    Base_Dados.cursor.execute(query1)
    quant = Base_Dados.cursor.fetchone()
    quant = functools.reduce(lambda sub, ele: sub * 10 + ele, quant) + 1
    
    query2 = "UPDATE ordens SET pecas_em_processamento = " + str(quant) + "WHERE id =" + str(i)
    Base_Dados.cursor.execute(query2)


def atualizar_pecas_processadas(i):
    query1 = "SELECT pecas_processadas FROM ordens WHERE id=" + str(i)
    Base_Dados.cursor.execute(query1)
    quant = Base_Dados.cursor.fetchone()
    quant = functools.reduce(lambda sub, ele: sub * 10 + ele, quant) + 1
    
    query2 = "UPDATE ordens SET pecas_processadas = " + str(quant) + "WHERE id =" + str(i)
    Base_Dados.cursor.execute(query2)
    
    
def saida_peca(pi):
    query = "SELECT " + pi + " FROM inventario WHERE id=1"
    Base_Dados.cursor.execute(query)
    result = Base_Dados.cursor.fetchone()
    result = functools.reduce(lambda sub, ele: sub * 10 + ele, result) 
    
    query2 = "UPDATE inventario SET " + pi + "=" + str(result-1) + " WHERE id = 1"
    Base_Dados.cursor.execute(query2)
    
    
def entrada_peca(pf):
    query = "SELECT " + pf + " FROM inventario WHERE id=1"
    Base_Dados.cursor.execute(query)
    result = Base_Dados.cursor.fetchone()
    result = functools.reduce(lambda sub, ele: sub * 10 + ele, result) + 1
    
    query2 = "UPDATE inventario SET " + pf + "=" + str(result) + " WHERE id = 1"
    Base_Dados.cursor.execute(query2)