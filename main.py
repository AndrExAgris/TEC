import re


def output(lista_formatada):
    print('salvando...')
    with open('mt.out', 'w') as arquivo:
        for elemento in lista_formatada:
            linha = ' '.join(elemento)
            arquivo.write(linha + '\n')
    print('MT convertida esta em mt.out')


def guarda_primeiro_estado(lista_de_estados, lista_formatada):
    
    for elemento in lista_formatada:
        if elemento:    
            lista_de_estados.append(elemento[0])        
       
    lista_de_estados = list(set(lista_de_estados)) 
    return lista_de_estados


def rotina_inicial_sipser(lista_formatada, in_place=True):

    inicio = [
        # Transições iniciais
        ['0', '0', '#', 'r', 'passa0'],
        ['0', '1', '#', 'r', 'passa1'],

        # Estado passa0
        ['passa0', '0', '0', 'r', 'passa0'],
        ['passa0', '1', '0', 'r', 'passa1'],
        ['passa0', '_', '0', 'r', 'retornaInicio'],

        # Estado passa1
        ['passa1', '0', '1', 'r', 'passa0'],
        ['passa1', '1', '1', 'r', 'passa1'],
        ['passa1', '_', '1', 'r', 'retornaInicio'],

        # Retorno ao início
        ['retornaInicio', '*', '*', 'l', 'retornaInicio'],
        ['retornaInicio', '#', '#', 'r', 'ini'],

        # Ignora movimentos extremos à esquerda
        ['*', '#', '#', 'r', '*'],
    ]

    if in_place:
        lista_formatada.extend(inicio)
        return lista_formatada
    else:
        return lista_formatada + inicio


def sipser_para_standard(lista_formatada):

    for elemento in lista_formatada:
        if elemento[0] == '0':
            elemento[0] = 'ini'
        if elemento[4] == '0':
            elemento[4] = 'ini'
                
    lista_formatada = rotina_inicial_sipser(lista_formatada)
        
    return lista_formatada


def main():   
    mt_lida = []
    
    with open("mt.in", "r") as arquivo_in:
        for linha in arquivo_in:
            if linha == ';S' or ';I':
                mt_lida.append(linha)
            else:
                linha = re.split(r'(\s)',arquivo_in.readline())
                linha = ' '.join(linha).split()
                mt_lida.append(linha)
    
    lista_formatada = [linha_lida.split() for linha_lida in mt_lida]
    lista_de_estados = []
    
    if ';S' in lista_formatada[0]:
        print('Convertendo de Sipser para Standard\n')
        lista_formatada.pop(0)
    
        lista_de_estados = guarda_primeiro_estado(lista_de_estados,lista_formatada)    
        
        sipser_para_standard(lista_formatada)
        output(lista_formatada)
    else:
        if ';I' in lista_formatada[0]:
            print('Não implementado\n')
            
            
if __name__ == "__main__":
    main()

