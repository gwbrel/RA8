import sys


#FASE1: ANALISADOR LÉXICO (AFD)


def lerArquivo(file_path: str) -> list:
    linhas = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                linhas.append(line.strip())
    except FileNotFoundError:
        print(f"Erro: Arquivo '{file_path}' não encontrado.")
        sys.exit(1)
    return linhas

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
    while a < len(linha):
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


# FASE2: - AMBIENTE DE EXECUÇÃO (IEEE 754 & Memória)

class AmbienteExecucao:
    def __init__(self):
        self.memoria = {}
        self.historico = []
        self.mem_counter = 0

    def calcular(self, a, b, op):
        if op == '+':  return float(a + b)
        if op == '-':  return float(a - b)
        if op == '*':  return float(a * b)
        if op == '/':  return float(a / b)
        if op == '//': return float(int(a) // int(b))
        if op == '%':  return float(int(a) % int(b))
        if op == '^':  return float(a ** int(b))
        raise ValueError(f"Operador sem suporte: {op}")

    def executarExpressao(self, tokens):
        pilha = []
        for token in tokens:
            tipo, valor = token

            if tipo == 'ABRE_PAR':
                pilha.append('(')
            elif tipo == 'FECHA_PAR':
                grupo = []
                while pilha and pilha[-1] != '(':
                    grupo.append(pilha.pop())
                if pilha: pilha.pop() # Remove '('
                grupo.reverse()

                # Logica MEM: Se encontrar o comando MEM no grupo
                if 'MEM' in grupo:
                    val = grupo[0] if not isinstance(grupo[0], str) else grupo[1]
                    nome = f"var{self.mem_counter}"
                    self.memoria[nome] = float(val)
                    self.mem_counter += 1
                    pilha.append(float(val))
                
                # Logica RES: Se encontrar o comando RES
                elif 'RES' in grupo:
                    n = int(grupo[0])
                    if n <= 0 or n > len(self.historico):
                        raise ValueError(f"RES({n}) inválido. Histórico possui {len(self.historico)} itens.")
                    pilha.append(self.historico[-n])
                
                else:
                    for item in grupo: pilha.append(item)

            elif tipo in ('numINT', 'numReal'):
                pilha.append(float(valor))
            elif tipo in ('MEM', 'RES'):
                pilha.append(valor)
            elif tipo == 'OP':
                if len(pilha) < 2: raise ValueError(f"Pilha insuficiente para {valor}")
                b = pilha.pop()
                a = pilha.pop()
                pilha.append(self.calcular(a, b, valor))

        resultado = pilha[0] if pilha else 0.0
        # So vai ser adicionado ao se a linha nao for apenas uma consulta de RES ou MEM solitaria
        if any(t[0] == 'OP' for t in tokens) or ('MEM' in [t[1] for t in tokens]):
            self.historico.append(resultado)
        return resultado

# -FASE 3 - GERACAO DE ASSEMBLY ARMv7

def gerarAssembly(tokens, id_linha):
    asm_data = [f".data", f"  @ Dados da Linha {id_linha}"]
    asm_text = [f".text", f"  @ Codigo da Linha {id_linha}"]
    num_idx = 0

    for tipo, valor in tokens:
        if tipo in ('ABRE_PAR', 'FECHA_PAR'): continue
        
        if tipo in ('numINT', 'numReal'):
            label = f"val_{id_linha}_{num_idx}"
            asm_data.append(f"{label}: .double {valor}")
            asm_text.append(f"    LDR r0, ={label}")
            asm_text.append(f"    VLDR.F64 d0, [r0]")
            asm_text.append(f"    VPUSH {{d0}}")
            num_idx += 1
            
        elif tipo == 'OP':
            asm_text.append("    VPOP {d1}           @ Desempilha b")
            asm_text.append("    VPOP {d0}           @ Desempilha a")
            if valor == '+': asm_text.append("    VADD.F64 d0, d0, d1")
            elif valor == '-': asm_text.append("    VSUB.F64 d0, d0, d1")
            elif valor == '*': asm_text.append("    VMUL.F64 d0, d0, d1")
            elif valor == '/': asm_text.append("    VDIV.F64 d0, d0, d1")
            else: asm_text.append(f"    BL rotina_{valor}")
            asm_text.append("    VPUSH {d0}")

        elif tipo == 'MEM':
            label_mem = f"mem_pos_{id_linha}"
            asm_data.append(f"{label_mem}: .double 0.0")
            asm_text.append(f"    LDR r0, ={label_mem}")
            asm_text.append("    VPOP {d0}")
            asm_text.append("    VSTR.F64 d0, [r0]    @ Salva na RAM")
            asm_text.append("    VPUSH {d0}")

        elif tipo == 'RES':
            asm_text.append("    VPOP {d0}           @ Pega o indice N")
            asm_text.append("    @ No simulador, acessaria o array de historico")
            asm_text.append("    BL recuperar_historico")

    return "\n".join(asm_data) + "\n\n" + "\n".join(asm_text)

# EXECUÇÃO PRINCIPAL

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python main.py arquivo.txt")
        sys.exit(1)

    ambiente = AmbienteExecucao()
    linhas = lerArquivo(sys.argv[1])

    with open("tokens.txt", "w", encoding="utf-8") as f_tok, \
         open("saida.s", "w", encoding="utf-8") as f_asm:

        for i, linha in enumerate(linhas, 1):
            if not linha: continue
            try:
                tokens = parseExpresao(linha)
                res = ambiente.executarExpressao(tokens)
                asm = gerarAssembly(tokens, i)

                # Salva tokens no .txt
                f_tok.write(f"Linha {i}: {linha}\n")
                f_tok.write(f"  -> Tokens:    {tokens}\n")
                f_tok.write(f"  -> Resultado: {res}\n\n")

                # Salva assembly no .s
                f_asm.write(f"@ ---- Linha {i}: {linha} ----\n")
                f_asm.write(asm + "\n\n")

                # Continua exibindo no terminal também
                print(f"Linha {i}: {linha}")
                print(f"  -> Tokens:    {tokens}")
                print(f"  -> Resultado: {res}")
                print(f"  -> Assembly:\n{asm}\n")

            except Exception as e:
                msg = f"Erro na linha {i} '{linha}': {e}\n"
                print(msg)
                f_tok.write(msg)
                f_asm.write(f"@ {msg}")

    print("=== ESTADO FINAL DA MÁQUINA ===")
    print(f"Memória:         {ambiente.memoria}")
    print(f"Histórico (RES): {ambiente.historico}")
    print("\nArquivos gerados: tokens.txt | saida.s")
