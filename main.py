def lerArquivo(file_path: str) -> list:
    linhas = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            linhas.append(line)
        return linhas
    
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
