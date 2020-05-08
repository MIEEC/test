from getOrder import *
from basedados import *
from client import*
import time


def main():
        
    #------INICIALIZAÇÃO--------
    reinicia_armazem()
    #receber_ordem()
    
    while True:
        tamanho = nr_ordens_pendentes()
        for i in range(1,tamanho):
            if pedidos_pendentes_tipo(i) == 'Transform':
                #-------SLECIONAR PROCESSO CONSOANTE PI E PF--------
                id_processo = seleciona_processo(pedidos_pendentes_pi(i), pedidos_pendentes_pf(i))
                
                while pecas_pendentes_quantidade(i) > 0:
                    #--------PRCESSAR PEDIDO---------
                    if (seleciona_inventario(pedidos_pendentes_pi(i)) > 1):
                        if ordem_por_iniciar(i) == 'True':
                            ordem_a_processar(i)
                            hora_inicio_ordem(i)
                          
                        if get_valor("sAT1") == 'False':
                            #-----ENVIAR INFO DO PROCESSO PARA O PLC-----    
                            set_valor_int("ferramenta", int(ferramenta(id_processo)))
                            set_valor_int("peca_i", separar_P(pedidos_pendentes_pi(i)))
                            set_valor_str("maquina", maquina(id_processo))
                            set_valor_int("tempo", int(tempo(id_processo)))
                             
                            #------ATUALIZAR BASE DE DADOS-------
                            saida_peca(pedidos_pendentes_pi(i))
                            atualizar_pecas_pendentes(i)
                            atualizar_pecas_em_processamento(i)
                             
                            #------VERIFICAR SE HÁ NOVAS ORDENS-----
                            tamanho = nr_ordens_pendentes()
                              
                            time.sleep(0.5)
                            set_valor_int("peca_i", 0)
                          
                        #------VERIFICAR PEÇA PROCESSADA | WAREHOUSE_IN: VARIAVEL QUE DETETA ENTRADA NO ARMAZEM------------
                        if get_valor("warehouse_in") == 'True':
                            atualizar_pecas_processadas(i)
                            #-----NESTE MOMENTO A PECA É CONSIDERADA PROCESSADA QUANDO ENTRA NO ARMAZEM---- A ALTERAR!
                            entrada_peca(pedidos_pendentes_pf(i))
                          
                    else:
                        ordem_suspenso(i)
                        break
      
                hora_fim_ordem(i)


    
def separar_P(peca):
    return int(peca.split('P')[1])

main()