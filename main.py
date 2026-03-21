def lerArquivo(file_path: str) -> list:
    linha = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            linha.append(line)
        return linha
    

def tratarnumero(linha, a):
    buffer = ""
    while a < len(linha) and (linha[a].isdigit() or linha[a] == '.'):
        buffer += linha[a]
        a += 1
    if buffer.count('.') > 1:
        raise ValueError({buffer})
    tipo = "numReal" if "." in buffer else "numINT"
    return a, (tipo, buffer)

def tratarbarra(linha, a):
    if a + 1 < len(linha) and linha[a+1] == '/':
        return a + 2, ("//")
    return a + 1, ("/")

def tratar_identificador(linha, a):
    buffer = ""
    while a < len(linha) and (linha[a].isalnum()):
        buffer += linha[a]
        a += 1
# verificar se o keyword eh obrigatorio ou eh uma memoria (variavel)
    tipo = "RES" if buffer == "RES" else "MEM"
    return a, (tipo, buffer)

def parseExpresao(linha):
        tokens = []
        a = 0
        tamanho = len(linha)
        while a < tamanho:
            char = linha[a]
            #ignorar espaco
            if char.isspace():
                a += 1
                continue
            #pararenteses
            if char == '(':
                tokens.append(("("))
                a += 1
            elif char == ')':
                tokens.append((")"))
                a += 1
            #Numeros
            elif char.isdigit():
                a, token = tratarnumero(linha, a)
                tokens.append(token)
            #operador aritmetico
            elif char in '+*-^%':
                tokens.append(char)
                a += 1
            #barra / ou //
            elif char == '/':
                a, token = tratarbarra(linha, a)
                tokens.append(token)
            #tratar identificadores "RES" ou Nomes de Memorias
            elif char.isalpha():
                a, token = tratar_identificador(linha, a)
                tokens.append(token)
            else:
                raise ValueError(f"Erro Lexico '{char}' nao reconhecido")
        return tokens
