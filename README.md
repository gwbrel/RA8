# RA1-21 — Compilador RPN para Assembly ARMv7

## Informações Acadêmicas

| Campo | Detalhe |
|-------|---------|
| **Instituição** | PUCPR — Pontifícia Universidade Católica do Paraná |
| **Disciplina** | Compiladores |
| **Professor** | Frank Alcantara |
| **Aluno** | Gabriel Luis Inacio de Souza |
| **Grupo Canvas** | RA1 21 |

## Interpretador de Expressões com Analisador Léxico, Execução em Pilha e Geração de Assembly ARMv7

Este projeto apresenta a implementação de um interpretador de expressões matemáticas composto por três módulos principais: um analisador léxico baseado em um Autômato Finito Determinístico (AFD), um ambiente de execução fundamentado em uma máquina de pilha com suporte a memória e histórico, e um gerador de código em Assembly para a arquitetura ARMv7. O sistema é capaz de reconhecer, avaliar e traduzir expressões aritméticas, demonstrando conceitos fundamentais da construção de compiladores e interpretação de linguagens.

---

## Arquitetura do Sistema

O sistema é estruturado em três fases principais:

Analisador Léxico

Ambiente de Execução

Gerador de Assembly

 **Fluxo Geral**

 ```
Arquivo de Entrada → Leitura de Linhas
                            ↓
                    Análise Léxica (AFD) → Geração de Tokens → Execução (Máquina de Pilha)
                                                                                ↓
                                                                        Memória e Histórico → Resultado → Geração de Assembly ARMv7

```
---

## Analisador Léxico

O analisador léxico é implementado como um Autômato Finito Determinístico implícito, responsável por percorrer a entrada caractere por caractere e identificar padrões léxicos.

 **Tokens Reconhecidos**
 
```
Números inteiros (numINT)
Números reais (numReal)
Operadores (OP)
Parênteses (ABRE_PAR, FECHA_PAR)
Identificadores especiais (MEM, RES)

```
 **Estrutura do AFD**

O autômato possui estados implícitos, entre os quais:

```
Estado inicial (q0)
Estado de número inteiro (qNUM)
Estado de número real (qREAL)
Estado de identificador (qID)
Estado de operador de divisão (qDIV)

```
---

## Ambiente de Execução

A execução das expressões é realizada por uma máquina de pilha, que processa os tokens gerados pelo analisador léxico.

  **Modelo de Execução:**

A pilha é utilizada para armazenar operandos intermediários. As operações seguem o padrão:
  1. Inserção de operandos na pilha
  2. Remoção de operandos para aplicação de operadores
  3. Inserção do resultado na pilha

 **Operações Suportadas**
 
- Adição (+)
- Subtração (-)
- Multiplicação (*)
- Divisão (/)
- Divisão inteira (//)
- Módulo (%)
- Potência (^)
  
**Gerenciamento de Memória**

O sistema implementa um mecanismo de armazenamento por meio do comando MEM, que salva valores em uma estrutura de memória interna

---

## Geração de Código Assembly

A terceira fase consiste na tradução dos tokens para instruções Assembly compatíveis com a arquitetura ARMv7, utilizando operações de ponto flutuante (VFP).

**Estrutura do Código Gerado**

  O código é dividido em duas seções:

- data: armazenamento de constantes
- text: instruções executáveis

## Estrutura de Arquivos

```
projeto/
├── main.py          # Código principal
├── teste.txt        # Arquivo de entrada (Criado por você)
├── tokens.txt       # Gerado automaticamente após execução
└── saida.s          # Gerado automaticamente após execução

```

## Como Executar

### Passo 1 — Gerar os tokens e o Assembly

```bash
python main.py teste.txt
```
### Como Executar no CPUlator
  1. Escolha o sistema ARMv7 DE1-SoC
  2. Selecione o arquivo saida.s no editor
  3. Selecione Compile and Load, depois Continue
  4. Após a execução parar, vá em Memory (Ctrl-M)
  5. Digite re_0 no campo "Go to address" para ver os resultados
