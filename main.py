def lerArquivo(file_path: str) -> list:
    linhas = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            linhas.append(line)
        return linhas
    

def tratarnumero(linha, a):
    buffer = ""
    while a < len(linha) and (linha[a].isdigit() or linha[a] == '.'):
        buffer += linha[a]
        a += 1
        if buffer.count('.') > 1:
            raise ValueError({buffer})
        tipo = "numReal" if "." in buffer else "numINT"

    def parseExpresao(linhas):
        tokens = []
        a = 0
        tamanho = len(linhas)
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
