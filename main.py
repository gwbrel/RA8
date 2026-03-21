def lerArquivo(file_path: str) -> list:
    linhas = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            linhas.append(line)
        return linhas
    
    def parseExpresao():
        pass