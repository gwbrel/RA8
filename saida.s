.global _start
.text
_start:

@ ---- Linha 1: 3.14 2.0 + ----
.data
  @ Dados da Linha 1
val_1_0: .double 3.14
val_1_1: .double 2.0

.text
  @ Codigo da Linha 1
    LDR r0, =val_1_0
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =val_1_1
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    VPOP {d1}           @ Desempilha b
    VPOP {d0}           @ Desempilha a
    VADD.F64 d0, d0, d1
    VPUSH {d0}

@ ---- Linha 2: 5 3 * ----
.data
  @ Dados da Linha 2
val_2_0: .double 5
val_2_1: .double 3

.text
  @ Codigo da Linha 2
    LDR r0, =val_2_0
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =val_2_1
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    VPOP {d1}           @ Desempilha b
    VPOP {d0}           @ Desempilha a
    VMUL.F64 d0, d0, d1
    VPUSH {d0}

@ ---- Linha 3: 10 2 / ----
.data
  @ Dados da Linha 3
val_3_0: .double 10
val_3_1: .double 2

.text
  @ Codigo da Linha 3
    LDR r0, =val_3_0
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =val_3_1
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    VPOP {d1}           @ Desempilha b
    VPOP {d0}           @ Desempilha a
    VDIV.F64 d0, d0, d1
    VPUSH {d0}

@ ---- Linha 4: 8 3 % ----
.data
  @ Dados da Linha 4
val_4_0: .double 8
val_4_1: .double 3

.text
  @ Codigo da Linha 4
    LDR r0, =val_4_0
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =val_4_1
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    VPOP {d1}           @ Desempilha b
    VPOP {d0}           @ Desempilha a
    VDIV.F64 d2, d0, d1         @ d2 = a / b
    VCVT.S32.F64 s4, d2         @ trunca quociente
    VCVT.F64.S32 d2, s4         @ quociente inteiro como double
    VMUL.F64 d2, d2, d1         @ d2 = trunc(a/b) * b
    VSUB.F64 d0, d0, d2         @ d0 = a - trunc(a/b)*b
    VPUSH {d0}

@ ---- Linha 5: 2 3 ^ ----
.data
  @ Dados da Linha 5
val_5_0: .double 2
val_5_1: .double 3

.text
  @ Codigo da Linha 5
    LDR r0, =val_5_0
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =val_5_1
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    VPOP {d1}           @ Desempilha b
    VPOP {d0}           @ Desempilha a
    VCVT.S32.F64 s0, d0    @ base → int
    VCVT.S32.F64 s1, d1    @ exp  → int
    VMOV r0, s0             @ r0 = base
    VMOV r1, s1             @ r1 = expoente
    MOV  r2, #1             @ r2 = resultado = 1
pot_loop_5_0:
    CMP  r1, #0
    BEQ  pot_fim_5_0
    MUL  r2, r2, r0         @ resultado *= base
    SUB  r1, r1, #1         @ expoente--
    B    pot_loop_5_0
pot_fim_5_0:
    VMOV s0, r2
    VCVT.F64.S32 d0, s0    @ int → double
    VPUSH {d0}

@ ---- Linha 6: (3 4 +) ----
.data
  @ Dados da Linha 6
val_6_0: .double 3
val_6_1: .double 4

.text
  @ Codigo da Linha 6
    LDR r0, =val_6_0
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =val_6_1
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    VPOP {d1}           @ Desempilha b
    VPOP {d0}           @ Desempilha a
    VADD.F64 d0, d0, d1
    VPUSH {d0}

@ ---- Linha 7: ((1.5 2.0 *) (3.0 4.0 *) /) ----
.data
  @ Dados da Linha 7
val_7_0: .double 1.5
val_7_1: .double 2.0
val_7_2: .double 3.0
val_7_3: .double 4.0

.text
  @ Codigo da Linha 7
    LDR r0, =val_7_0
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =val_7_1
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    VPOP {d1}           @ Desempilha b
    VPOP {d0}           @ Desempilha a
    VMUL.F64 d0, d0, d1
    VPUSH {d0}
    LDR r0, =val_7_2
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =val_7_3
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    VPOP {d1}           @ Desempilha b
    VPOP {d0}           @ Desempilha a
    VMUL.F64 d0, d0, d1
    VPUSH {d0}
    VPOP {d1}           @ Desempilha b
    VPOP {d0}           @ Desempilha a
    VDIV.F64 d0, d0, d1
    VPUSH {d0}

@ ---- Linha 8: (5 MEM) ----
.data
  @ Dados da Linha 8
val_8_0: .double 5
mem_pos_8: .double 0.0

.text
  @ Codigo da Linha 8
    LDR r0, =val_8_0
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =mem_pos_8
    VPOP {d0}
    VSTR.F64 d0, [r0]    @ Salva na RAM
    VPUSH {d0}

@ ---- Linha 9: (1 RES) ----
.data
  @ Dados da Linha 9
val_9_0: .double 1

.text
  @ Codigo da Linha 9
    LDR r0, =val_9_0
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    VPOP {d0}           @ Pega o indice N
    @ No simulador, acessaria o array de historico
    BL recuperar_historico

@ Erro na linha 10 '3.14.5 2 +': Número malformado: 3.14.5

@ ---- Fim da Execução ----
    MOV r7, #1          @ Syscall de Exit no Linux ARM
    MOV r0, #0          @ Retorna status 0 (Sucesso)
    SVC 0               @ Executa chamada de sistema

@ ---- Subrotinas Auxiliares ----
recuperar_historico:
    @ STUB: Função vazia para evitar erro de compilação.
    @ Em uma implementação completa, a lógica para ler a memória RAM
    @ com base no índice passado no registrador d0 iria aqui.
    BX lr               @ Retorna para onde a função foi chamada
