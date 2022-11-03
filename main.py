# Justificação de textos
def limpa_texto(texto):
    '''Elimina espaços do texto original.

    Sem dependências

    Parametros: str
    Retorna: str
    '''
    return ' '.join(texto.split())

def corta_texto(texto, largura):
    '''Divide o texto pela ultima palavra completa em função da largura.

    Sem depenências
    
    Parametros: str, int
    Retorna: (str,str)
    '''
    palavras = texto.split()
    len_total = 0
    i = 0
    # Econtrar a última palavra completa contida pela largura desejada
    for i, palavra in enumerate(palavras):
        len_total += len(palavra)
        if largura < len_total:
            break
        # Contar com o espaço entre palavras
        len_total += 1
    if len(texto) <= largura:
        i += 1
    return ' '.join(palavras[:i]), ' '.join(palavras[i:])

def insere_espacos(texto, largura):
    '''Preenche a string com espaços em função da largura.

    Sem dependências
    
    Parametros: str, int
    Retorna: str
    '''

    palavras = texto.split()
    
    # numero_espacos -> numero de vezes que duas palavras devem ser separadas
    # espaco_para_preencher -> numero de caracteres vazios necessários
    numero_espacos = len(palavras)-1
    espaco_para_preencher = largura - (len(texto)-numero_espacos)

    if len(palavras) > 1:   
        espaco_default = espaco_para_preencher // numero_espacos
        espacos_restantes = espaco_para_preencher - (numero_espacos * espaco_default)

        mapa_espacos = [espaco_default] * numero_espacos

        for i in range(espacos_restantes):
            mapa_espacos[i] += 1 
        
        palavra_final = ''
        for i, palavra in enumerate(palavras):
            if i < numero_espacos:
                palavra_final += palavra + ' '*mapa_espacos[i]
            else:
                palavra_final += palavra
        return palavra_final
    else:
        # Se apenas existe uma palavra, adicionar os espaços correspondentes no final
        return texto + ' '*espaco_para_preencher

def justifica_texto(texto, largura):
    '''Justifica uma string com a largura expecificada.

    Depende de: limpa_texto(), corta_texto(), insere_espacos(), 

    Parametros: str, int
    Retorna: tuple
    '''
    if type(texto) != str or type(largura) != int or len(texto) == 0\
         or largura <= 0 or not(all(len(palavra) <= largura for palavra in texto.split())):
        raise ValueError('justifica_texto: argumentos invalidos')
    
    texto_justificado = corta_texto(limpa_texto(texto), largura)
    tuplo_justificado = ()

    def insere_espacos_fim(txt):
        espaco_para_preencher = largura - (len(txt))
        return txt + ' '*espaco_para_preencher

    while True:
        # Verificar se é a última frase e justificar de forma diferente
        if len(texto_justificado[1]) > 0:
            tuplo_justificado += (insere_espacos(texto_justificado[0], largura),)
            texto_justificado = texto_justificado[1]
            texto_justificado = corta_texto(texto_justificado, largura)
        else:
            tuplo_justificado += (insere_espacos_fim(texto_justificado[0]),)
            break

    return tuplo_justificado

# Método de Hondt

def calcula_quocientes(votos, deputados):
    '''Calcula os quocientes de cada partido segundo o Método de Hondt.

    Sem dependências
    
    Parametros: dict, int
    Retorna: dict
    '''
    quocientes = votos.copy()

    for partido, num_votos in quocientes.items():
        quocientes[partido] = [float(num_votos)]
        for i in range(1, deputados):
            quocientes[partido].append(float(quocientes[partido][0] / (i+1)))

    return quocientes


def atribui_mandatos(votos, deputados):
    '''A partir do cálculo dos quocientes, ordenar os partidos
    em função dos resultados obtidos nas respetivas votações.
    
    Depende de: calcula_quocientes()

    Parametros: dict, int
    Retorna: list
    '''
    quocientes = calcula_quocientes(votos, deputados)
    mandatos = list()

    # Ordenar os partidos de forma crescente em função do número total de votos
    # de forma a facilitar situações de empate
    partidos_ordenados = dict(sorted(quocientes.items(), key=lambda votos : votos[1][0]))

    while len(mandatos) < deputados:        
        partido_a_eleger = ('', 0)
        for partido, num_votos in partidos_ordenados.items():
            if num_votos[0] > partido_a_eleger[1]:
                partido_a_eleger = (partido, num_votos[0])
        
        partidos_ordenados[partido_a_eleger[0]] = partidos_ordenados[partido_a_eleger[0]][1:]
        mandatos.append(partido_a_eleger[0])

    return mandatos

def obtem_partidos(informacao):
    '''Obtem todos os partidos que participaram nas eleições
    
    Sem dependências

    Parametros: dict
    Retorna: list
    '''
    partidos_final = set()
    for circulo in informacao.values():
        for partidos in circulo['votos'].keys():
            partidos_final.add(partidos)
    
    partidos_final = sorted(partidos_final)

    return partidos_final

def obtem_resultado_eleicoes(informacao):
    '''Calcula os resultados das eleições
    
    Depende de: atribui_mandatos(), obtem_partidos(),
    (Indiretamente): calcula_quocientes()
    
    Parametros: dict
    Retorna: list
    '''
    # Verificações
    if type(informacao) != dict or len(informacao) == 0:
        raise ValueError('obtem_resultado_eleicoes: argumento invalido')

    for circulo in informacao.values():
        if type(circulo) != dict or len(circulo) != 2\
            or 'deputados' not in circulo.keys() or 'votos' not in circulo.keys()\
            or type(circulo['deputados']) != int or type(circulo['votos']) != dict\
            or circulo['deputados'] <= 0 or len(circulo['votos']) == 0:

            raise ValueError('obtem_resultado_eleicoes: argumento invalido')

        if not all(type(nome_circulo)==str and len(nome_circulo)>0 for nome_circulo in informacao.keys()):
            raise ValueError('obtem_resultado_eleicoes: argumento invalido')
        
        if  not all(((type(votos) == int) and votos > 0 and (type(partido) == str)) for (partido, votos) in circulo['votos'].items()):
            raise ValueError('obtem_resultado_eleicoes: argumento invalido')
    
    resultados = {(partido):(partido, 0, 0) for partido in obtem_partidos(informacao)}

    for circulo in informacao.values():
        votos = circulo['votos']
        deputados = circulo['deputados']
        resultado_circulo = atribui_mandatos(votos, deputados)
        for partido, num_votos in votos.items():
            votos_atuais = resultados[partido][2]
            deputados_atuais = resultados[partido][1]
            resultados[partido] = (partido, deputados_atuais + resultado_circulo.count(partido), votos_atuais + num_votos)

    resultados = list(resultados.values())
    resultados = sorted(resultados, key=lambda resultado: (resultado[1],resultado[2]), reverse=True)
    return resultados

# Solução de sistemas de equações

def produto_interno(t1, t2):
    '''Calcula o produto interno de dois vetores.

    Sem dependências
    
    Parametros: tuple, tuple
    Retorna: float
    '''
    return sum(float(t1[i]*t2[i]) for i in range(len(t1)))

def verifica_convergencia(matriz, constantes, solucao_atual, precisao):
    '''Verifica a precisão das soluções apresentadas para
    um dado sistema, representado por uma matriz e um vetor
    de soluções (constantes).

    Depende de: produto_interno()
    
    Parametros: tuple, tuple, tuple, float
    Retorna: bool
    '''
    erros = []
    # Calcular o erro para cada linha da matriz aumentada
    for i in range(len(constantes)):
        resultado_linha = produto_interno(matriz[i], solucao_atual)
        erros.append(abs(resultado_linha-constantes[i]))

    return all(e<precisao for e in erros)

def retira_zeros_diagonal(matriz, constantes):
    '''Retira os zeros da diagonal principal de uma
    matriz efetuando trocas de linha.

    Sem dependências
    
    Parametros: tuple, tuple
    Retorna: (tuple, tuple)
    '''
    i = 0
    j = 0
    n_matriz = list(matriz)
    n_constantes = list(constantes)
    while i < len(matriz):
        while n_matriz[i][i] == 0 and j < len(n_matriz):
            if n_matriz[j][i] != 0 and n_matriz[i][j] != 0:
                n_matriz[i], n_matriz[j] = n_matriz[j], n_matriz[i]
                n_constantes[i], n_constantes[j] = n_constantes[j], n_constantes[i]
                j = 0
            j += 1
        i += 1
    return tuple(n_matriz), tuple(n_constantes)

def eh_diagonal_dominante(matriz):
    '''Verifica se uma matriz é diagonalmente dominante.

    Sem dependências
    
    Parametros: tuple
    Retorna: bool
    '''
    linha_atual = []
    for i in range(len(matriz)):
        linha_atual = list(matriz[i])
        elemento_diagonal = linha_atual.pop(i)
        linha_atual = [abs(el) for el in linha_atual]
        if abs(elemento_diagonal) < sum(linha_atual):
            return False
    return True

def resolve_sistema(matriz, constantes, precisao):
    '''Resolve um sistema de equações lineares recorrendo ao
    método de Jacobi.

    Depende de: retira_zeros_diagonal(), eh_diagonal_dominante(),
    verifica_convergencia(), produto_interno()
    
    Parametros: tuple, tuple, float
    Retorna: tuple
    '''
    # Verificacao da matriz
    if type(matriz) != tuple or len(matriz)==0 or len(matriz[0]) != len(matriz):
        raise ValueError('resolve_sistema: argumentos invalidos')

    for linha in matriz:
        if type(linha) != tuple or len(linha) != len(matriz[0]):
            raise ValueError('resolve_sistema: argumentos invalidos')
        else:
            for valor in linha:
                if (type(valor) != int and type(valor) != float):
                    raise ValueError('resolve_sistema: argumentos invalidos')

    # Verificacao das constantes
    if type(constantes) != tuple or len(constantes)==0 or len(constantes) != len(matriz):
        raise ValueError('resolve_sistema: argumentos invalidos')
    if not all((type(c) == int or type(c) == float) for c in constantes):
        raise ValueError('resolve_sistema: argumentos invalidos')
    
    # Verificacao da precisao
    if type(precisao) != float or precisao <= 0:
        raise ValueError('resolve_sistema: argumentos invalidos')
    
    nova_matriz, novas_constantes = retira_zeros_diagonal(matriz, constantes)

    # Verificacao da diagonal
    if not eh_diagonal_dominante(nova_matriz):
        raise ValueError('resolve_sistema: matriz nao diagonal dominante')

    estimativas = [[0 for c in constantes]] 

    while not verifica_convergencia(nova_matriz, novas_constantes, estimativas[-1], precisao):
        novas_estimativas = list()
        for i in range(len(estimativas[0])):
            f = produto_interno(nova_matriz[i], estimativas[-1])
            nova_estimativa = estimativas[-1][i] + (novas_constantes[i] - f) / nova_matriz[i][i]
            novas_estimativas.append(nova_estimativa)
        estimativas.append(novas_estimativas)

    return tuple(estimativas[-1])