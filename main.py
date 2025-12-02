#!/usr/bin/env python3
import re

def salvar_arquivo_saida(lista_transicoes):
    """Salva a lista de transições no arquivo mt.out"""
    print('Salvando no arquivo mt.out...')
    with open('mt.out', 'w') as arquivo:
        for transicao in lista_transicoes:
            linha = ' '.join(transicao)
            arquivo.write(linha + '\n')
    print('Arquivo mt.out criado com sucesso!')


def extrair_estados_unicos(lista_estados, lista_transicoes):
    """Extrai todos os estados únicos da máquina"""
    for transicao in lista_transicoes:
        if transicao:
            lista_estados.append(transicao[0])
    
    lista_estados = list(set(lista_estados))
    print('\nEstados encontrados:', lista_estados)
    return lista_estados


def adicionar_rotina_inicial_fita_semi(lista_transicoes):
    """Insere rotina inicial para conversão de fita semi-infinita"""
    # Rotina que adiciona # no início e faz shift para direita
    inicial_zero = ['0', '0', '#', 'r', 'move0']
    inicial_um = ['0', '1', '#', 'r', 'move1']

    move0_ler0 = ['move0', '0', '0', 'r', 'move0']
    move0_ler1 = ['move0', '1', '0', 'r', 'move1']
    move0_branco = ['move0', '_', '0', 'r', 'voltaComeco']

    move1_ler0 = ['move1', '0', '1', 'r', 'move0']
    move1_ler1 = ['move1', '1', '1', 'r', 'move1']
    move1_branco = ['move1', '_', '1', 'r', 'voltaComeco']

    volta_geral = ['voltaComeco', '*', '*', 'l', 'voltaComeco']
    volta_hash = ['voltaComeco', '#', '#', 'r', 'q_ini']
    
    # Ignora movimentos além da parede à esquerda
    bloqueia_esq = ['*', '#', '#', 'r', '*']
    
    lista_transicoes.append(inicial_zero)
    lista_transicoes.append(inicial_um)
    lista_transicoes.append(move0_ler0)
    lista_transicoes.append(move0_ler1)
    lista_transicoes.append(move0_branco)
    lista_transicoes.append(move1_ler0)
    lista_transicoes.append(move1_ler1)
    lista_transicoes.append(move1_branco)
    lista_transicoes.append(volta_geral)
    lista_transicoes.append(volta_hash)
    lista_transicoes.append(bloqueia_esq)

    return lista_transicoes


def converter_semi_para_infinita(lista_transicoes):
    """Converte fita semi-infinita para fita duplamente infinita"""
    print('\n=== Conversão: Semi-infinita -> Duplamente Infinita ===')
    
    # Renomeia estados iniciais '0' para 'q_ini'
    for transicao in lista_transicoes:
        if transicao[0] == '0':
            transicao[0] = 'q_ini'
        if transicao[4] == '0':
            transicao[4] = 'q_ini'
    
    print('Estados renomeados')
    
    # Insere rotina inicial
    lista_transicoes = adicionar_rotina_inicial_fita_semi(lista_transicoes)
    
    print('Rotina inicial adicionada')
    
    return lista_transicoes


def adicionar_rotina_inicial_fita_dupla(lista_transicoes):
    """Insere rotina inicial para conversão de fita duplamente infinita"""
    # Adiciona # no início e & no final, depois retorna
    inicial_zero = ['0', '0', '#', 'r', 'move0']
    inicial_um = ['0', '1', '#', 'r', 'move1']

    move0_ler0 = ['move0', '0', '0', 'r', 'move0']
    move0_ler1 = ['move0', '1', '0', 'r', 'move1']
    move0_branco = ['move0', '_', '0', 'r', 'colocaMarca']

    move1_ler0 = ['move1', '0', '1', 'r', 'move0']
    move1_ler1 = ['move1', '1', '1', 'r', 'move1']
    move1_branco = ['move1', '_', '1', 'r', 'colocaMarca']

    marca_fim = ['colocaMarca', '_', '&', 'l', 'voltaComeco']

    volta_geral = ['voltaComeco', '*', '*', 'l', 'voltaComeco']
    volta_hash = ['voltaComeco', '#', '#', 'r', 'q_ini']
    
    lista_transicoes.append(inicial_zero)
    lista_transicoes.append(inicial_um)
    lista_transicoes.append(move0_ler0)
    lista_transicoes.append(move0_ler1)
    lista_transicoes.append(move0_branco)
    lista_transicoes.append(move1_ler0)
    lista_transicoes.append(move1_ler1)
    lista_transicoes.append(move1_branco)
    lista_transicoes.append(volta_geral)
    lista_transicoes.append(volta_hash)
    lista_transicoes.append(marca_fim)
    
    return lista_transicoes


def converter_infinita_para_semi(lista_transicoes, lista_estados):
    """Converte fita duplamente infinita para fita semi-infinita"""
    print('\n=== Conversão: Duplamente Infinita -> Semi-infinita ===')
    
    alfabeto_fita = []
    
    # Renomeia estados iniciais e coleta símbolos
    for transicao in lista_transicoes:
        if transicao:
            if transicao[0] == '0':
                transicao[0] = 'q_ini'
            if transicao[4] == '0':
                transicao[4] = 'q_ini'
            if transicao[1] != '_':
                alfabeto_fita.append(transicao[1])
    
    alfabeto_fita = list(set(alfabeto_fita))
    print('Alfabeto da fita:', alfabeto_fita)
    
    # Insere rotina inicial
    adicionar_rotina_inicial_fita_dupla(lista_transicoes)
    print('Rotina inicial configurada')
    
    # Primeiro conjunto de estados: leitura de hash e preparação
    for simbolo in alfabeto_fita:
        simbolo = str(simbolo)
        for est in lista_estados:
            est = str(est)
            trans01 = [est + 'auxHash', simbolo, '_', 'r', est + 'auxHash' + simbolo]
            lista_transicoes.append(trans01)
            
            trans1 = [est, '#', '#', 'r', est + 'auxHash']
            trans2 = [est + 'auxHash', '_', '_', 'r', est + 'auxHashVazio']
            trans3 = [est + 'auxHashVazio', '_', '_', 'r', est + 'auxHashVazio']
            lista_transicoes.append(trans1)
            lista_transicoes.append(trans2)
            lista_transicoes.append(trans3)
            
            trans4 = [est + 'auxHashVazio', simbolo, '_', 'r', est + 'auxHash' + simbolo]
            lista_transicoes.append(trans4)
    
    print('Etapa 1 concluída')
    
    # Segundo conjunto: shift entre símbolos
    for est in lista_estados:
        est = str(est)
        for simbolo in alfabeto_fita:
            simbolo = str(simbolo)
            for simbolo2 in alfabeto_fita:
                simbolo2 = str(simbolo2)
                trans5 = [est + 'auxHash' + simbolo, simbolo2, simbolo, 'r', est + 'auxHash' + simbolo2]
                lista_transicoes.append(trans5)
    
    print('Etapa 2 concluída')
    
    # Terceiro conjunto: retorno aos estados originais
    for simbolo in alfabeto_fita:
        simbolo = str(simbolo)
        for est in lista_estados:
            est = str(est)
            trans6 = [est + 'auxHashVazio' + simbolo, '_', '0', 'r', est]
            trans7 = [est + 'auxHash' + simbolo, '_', simbolo, 'r', simbolo + 'ret' + est]
            trans8 = [simbolo + 'ret' + est, '*', '*', 'l', simbolo + 'ret' + est]
            trans9 = [simbolo + 'ret' + est, '#', '#', 'r', est]
            lista_transicoes.append(trans6)
            lista_transicoes.append(trans7)
            lista_transicoes.append(trans8)
            lista_transicoes.append(trans9)
    
    print('Etapa 3 concluída')
    
    # Estados para expansão à direita
    transicoes_extras = []
    estados_excluidos = ['0', 'move0', 'move1', 'colocaMarca', 'voltaComeco']
    
    for transicao in lista_transicoes:
        est = str(transicao[0])
        if est not in estados_excluidos and est not in transicoes_extras:
            estados_excluidos.append(est)
            expande_dir = [est, '&', '_', 'r', 'expandeDireita' + est]
            retorna_expande = ['expandeDireita' + est, '_', '&', 'l', est]
            transicoes_extras.append(expande_dir)
            transicoes_extras.append(retorna_expande)
    
    lista_transicoes.extend(transicoes_extras)
    print('Etapa final concluída')
    print('Estados processados:', estados_excluidos)
    
    return lista_transicoes


def main():
    """Função principal do tradutor"""
    print('=== Tradutor de Máquinas de Turing ===\n')
    
    # Lê o arquivo de entrada
    programa_completo = []
    with open("mt.in", "r") as arquivo_entrada:
        for linha in arquivo_entrada:
            if linha.strip() in [';S', ';I']:
                programa_completo.append(linha.strip())
            else:
                linha_dividida = linha.split()
                if linha_dividida:
                    programa_completo.append(linha_dividida)
    
    print('Arquivo lido com sucesso\n')
    
    # Processa as transições
    transicoes_processadas = []
    tipo_entrada = programa_completo[0]
    
    for i in range(1, len(programa_completo)):
        if isinstance(programa_completo[i], list):
            transicoes_processadas.append(programa_completo[i])
    
    estados_maquina = []
    
    print('Tipo de entrada:', tipo_entrada)
    
    # Executa a conversão apropriada
    if tipo_entrada == ';S':
        print('Modo: Fita Semi-infinita -> Fita Duplamente Infinita\n')
        estados_maquina = extrair_estados_unicos(estados_maquina, transicoes_processadas)
        converter_semi_para_infinita(transicoes_processadas)
        salvar_arquivo_saida(transicoes_processadas)
        
    elif tipo_entrada == ';I':
        print('Modo: Fita Duplamente Infinita -> Fita Semi-infinita\n')
        estados_maquina = extrair_estados_unicos(estados_maquina, transicoes_processadas)
        converter_infinita_para_semi(transicoes_processadas, estados_maquina)
        salvar_arquivo_saida(transicoes_processadas)
    
    else:
        print(f'Erro: Tipo desconhecido "{tipo_entrada}"')
    
    print('\n=== Processo finalizado ===')


if __name__ == "__main__":
    main()