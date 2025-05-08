# Projeto de Compilador Pascal → EWVM

> **Disciplina**: Processamento de Linguagens 2024/25
> **Grupo**: 59
> **Integrantes**:  
> - a104447 - Rodrigo Abreu Correia Domingues
> - a104085 - Rafael Azevedo Correia
> - a104452 - Rui Filipe Mesquita Amaral 

---

## 1. Introdução

Este relatório descreve a implementação de um compilador simples para um subset de Pascal que gera código para a **EWVM** (Easy‑Walk Virtual Machine). Apresentamos a arquitetura geral, as fases de análise e geração de código, bem como exemplos de programas de teste.

---

## 2. Arquitetura Geral

O compilador é organizado em quatro fases principais:

1. **Análise Léxica** – Tokenização do código-fonte Pascal (`pascal_lex.py`).  
2. **Análise Sintática** – Construção de AST via Yacc/PLY (`pascal_yacc.py`).  
3. **Análise Semântica** – Verificação de tipos, escopos e declaração de variáveis (`pascal_seman.py`).  
4. **Geração de Código** – Emissão de instruções EWVM (`pascal_codegen.py`).  

Fluxo de dados:

```
.ficheiro .pas  
    └─▶ Lexer ──▶ Parser ──▶ AST ──▶ Semant ──▶ CodeGen ──▶ .vm  
```

---

## 3. Componentes Detalhados

### 3.1 Análise Léxica (`pascal_lex.py`)

- Reconhecimento de **identificadores**, **números**, **strings** e **palavras-chave**.  
- Ignora espaços em branco e comentários `{ ... }`.  
- Emissão de tokens para o parser.

### 3.2 Análise Sintática (`pascal_yacc.py`)

- Definições BNF para **declarações**, **comandos** e **expressões**.  
- Construção de AST em tuplas aninhadas, por exemplo:
  ```python
  ('assign', 'x', ':=', ('num', 42))
  ```
- Regulação de precedência de operadores.

### 3.3 Análise Semântica (`pascal_seman.py`)

- Tabela de símbolos para **variáveis** e **funções**.  
- Verificação de **compatibilidade de tipos** em atribuições, condicionais e expressões.  
- Registro de limites de **arrays** como `(lower_bound, upper_bound)`.

### 3.4 Geração de Código EWVM (`pascal_codegen.py`)

- Alocação de **GP slots** para variáveis globais (`var_slots[name]`).  
- Mapeamento de **tipos básicos** (`var_types[name]`).  
- Instruções emitidas:
  - `pushi`, `pushs`, `storeg`, `pushg`  
  - Entrada/Saída: `read`, `atoi`, `writei`, `writes`, `writeln`  
  - Controle: `jz`, `jump`, `charat`, `strlen`, operações aritméticas e lógicas  

- **Rótulos únicos**: `nova_label()` gera `WHILE0`, `FOR1`, etc.  
- Implementação de **estrutura de repetição** genérica (inicialização, teste, corpo, passo).  
- Detecção de padrão de **acumulação de array** e tradução para loop `while`.

---

## 4. Estrutura de Ficheiros

```
.
├── pascal_lex.py        # Lexer
├── pascal_yacc.py       # Parser → AST
├── pascal_seman.py      # Verificador semântico
├── pascal_codegen.py    # Gerador de código EWVM
├── teste_codegen.py     # Script de testes automáticos
└── testes/
    ├── HelloWorld.pas
    ├── Fatorial.pas
    ├── Maior3.pas
    ├── BinPraInt.pas
    ├── SomaArray.pas
    └── … demais exemplos
```

Os arquivos `.vm` gerados ficam em `codigoVM/`.

---

## 5. Exemplos de Programas

### 5.1 HelloWorld.pas

**Fonte**:
```pascal
program HelloWorld;
begin
  writeln('Ola, Mundo!');
end.
```

### 5.2 SomaArray.pas

Computa a soma dos 5 números lidos:
```pascal
program SomaArray;
var
  numeros: array[1..5] of integer;
  soma: integer;
begin
  soma := 0;
  writeln('Introduza 5 números:');
  for i := 1 to 5 do
    readln(numeros[i]);
  writeln('Soma = ', soma);
end.
```

---

## 6. Conclusões e Trabalhos Futuros

- O compilador atende aos requisitos para o subset de Pascal.  
- Limitações:
  - não suporta funções recursivas no codegen;  
  - sem tipos `real`, `record` ou `pointer`.  
- Extensões possíveis:
  - Geração de código para **calls** e **retornos**;  
  - Otimizações de laços e expressões;  
  - Detecção de erros em tempo de execução na EWVM.

---

## 7. Referências

- [PLY (Python Lex-Yacc)](http://www.dabeaz.com/ply/)  
- Especificação EWVM  
- Apostilas de **Compiladores**
