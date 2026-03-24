import sys

# FASE 1: ANALISADOR LÉXICO

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
        raise ValueError(f"Número malformado: {buffer}")
    tipo = "numReal" if "." in buffer else "numINT"
    return a, (tipo, buffer)


def tratarbarra(linha, a):
    if a + 1 < len(linha) and linha[a+1] == '/':
        return a + 2, ("OP", "//")
    return a + 1, ("OP", "/")


def tratar_identificador(linha, a):
    buffer = ""
    while a < len(linha) and linha[a].isalnum():
        buffer += linha[a]
        a += 1
    tipo = "RES" if buffer == "RES" else "MEM"
    return a, (tipo, buffer)


def parseExpresao(linha):
    tokens = []
    a = 0
    tamanho = len(linha)
    while a < tamanho:
        char = linha[a]
        if char.isspace():
            a += 1
            continue
        if char == '(':
            tokens.append(("ABRE_PAR", "("))
            a += 1
        elif char == ')':
            tokens.append(("FECHA_PAR", ")"))
            a += 1
        elif char.isdigit():
            a, token = tratarnumero(linha, a)
            tokens.append(token)
        elif char in '+*-^%':
            tokens.append(("OP", char))
            a += 1
        elif char == '/':
            a, token = tratarbarra(linha, a)
            tokens.append(token)
        elif char.isalpha():
            a, token = tratar_identificador(linha, a)
            tokens.append(token)
        else:
            raise ValueError(f"Erro Lexico '{char}' nao reconhecido")
    return tokens



# FASE 2: AMBIENTE DE EXECUÇÃO

class AmbienteExecucao:
    def __init__(self):
        self.memoria = {}
        self.historico = []

    def calcular(self, a, b, op):
        if op == '+':  return a + b
        if op == '-':  return a - b
        if op == '*':  return a * b
        if op == '/':  return a / b
        if op == '//': return float(int(a) // int(b))
        if op == '%':  return float(int(a) % int(b))
        if op == '^':  return a ** int(b)
        raise ValueError(f"operador sem suporte: {op}")

    def executarExpressao(self, tokens):
        pilha = []

        for token in tokens:
            tipo, valor = token   # seguro: todos os tokens agora sao tuplas

            #abre parentese
            if tipo == 'ABRE_PAR':
                pilha.append('(')

            #Fecha parentese
            elif tipo == 'FECHA_PAR':
                grupo = []
                while pilha and pilha[-1] != '(':
                    grupo.append(pilha.pop())
                if pilha:
                    pilha.pop()  # remove o marcador '('
                grupo.reverse()

                #recall de memoria
                if len(grupo) == 1:
                    item = grupo[0]
                    if isinstance(item, str):
                        if item not in self.memoria:
                            raise ValueError(f"Variavel '{item}' nao foi definida na memoria")
                        pilha.append(self.memoria[item])
                    else:
                        pilha.append(item)

                #consulta ao historico
                elif len(grupo) == 2 and grupo[1] == 'RES':
                    n = int(grupo[0])
                    if n <= 0 or n > len(self.historico):
                        raise ValueError(
                            f"RES({n}): historico tem apenas "
                            f"{len(self.historico)} entrada(s)."
                        )
                    pilha.append(self.historico[-n])

                #store de memoria
                elif len(grupo) == 3 and grupo[2] == 'MEM':
                    nome, val, _ = grupo
                    if not isinstance(nome, str):
                        raise ValueError(f"MEM: esperado nome de variavel, recebi '{nome}'.")
                    self.memoria[nome] = float(val)
                    pilha.append(float(val))

                #grupo generico → re-empilha para operadores externos
                else:
                    for item in grupo:
                        pilha.append(item)

            #literais numericos
            elif tipo in ('numINT', 'numReal'):
                pilha.append(float(valor))

            #identificadores
            elif tipo in ('MEM', 'RES'):
                pilha.append(valor)

            #operadores aritmeticos
            elif tipo == 'OP':
                if len(pilha) < 2:
                    raise ValueError(f"Operador '{valor}': pilha insuficiente.")
                b = pilha.pop()
                a = pilha.pop()
                pilha.append(self.calcular(a, b, valor))

        resultado_final = pilha[0] if pilha else 0.0
        tem_operador = any(t[0] == 'OP' for t in tokens)
        if tem_operador:
            self.historico.append(resultado_final)
        return resultado_final



# EXECUTAR
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python main_corrigido.py arquivo_de_teste.txt")
    else:
        ambiente = AmbienteExecucao()

        try:
            with open(sys.argv[1], 'r') as arquivo:
                for num_linha, linha in enumerate(arquivo, 1):
                    linha_limpa = linha.strip()
                    if not linha_limpa:
                        continue

                    try:
                        tokens = parseExpresao(linha_limpa)
                        resultado = ambiente.executarExpressao(tokens)

                        print(f"Linha {num_linha}: {linha_limpa}")
                        print(f"  -> Resultado: {resultado}\n")

                    except Exception as e:
                        print(f"Erro na linha {num_linha} '{linha_limpa}': {e}\n")

            print("=== ESTADO FINAL DA MÁQUINA ===")
            print(f"Memória:           {ambiente.memoria}")
            print(f"Histórico (RES):   {ambiente.historico}")

        except FileNotFoundError:
            print("Erro: Arquivo não encontrado.")
