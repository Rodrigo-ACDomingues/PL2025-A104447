from pascal_seman import verificar_semantica
import os

label_counter = 0
output = []

def nova_label(prefixo="L"):
    global label_counter
    label = f"{prefixo}{label_counter}"
    label_counter += 1
    return label

def escrever(codigo):
    output.append(codigo)

def gerar_codigo(ast, nome_ficheiro="programa.pas"):
    verificar_semantica(ast)
    global output, label_counter
    output = []
    label_counter = 0

    tipo, nome, declaracoes, bloco = ast

    # Construir tabela de variáveis globais
    global_vars = {}
    pos = 0
    for decl in declaracoes:
        if isinstance(decl, list):
            for d in decl:
                if d[0] == 'var_decl':
                    for var in d[1]:
                        global_vars[var] = pos
                        escrever("pushi 0")
                        pos += 1

    escrever("start")
    gerar_bloco(bloco, global_vars)
    escrever("stop")

    # Geração de funções (sem suporte a chamadas ainda)
    for decl in declaracoes:
        if isinstance(decl, list):
            for d in decl:
                if d[0] == 'function':
                    nome_func, params, _, func_decls, func_bloco = d[1:]
                    escrever(f"{nome_func}:")
                    local_vars = {}
                    pos_local = 0
                    for p in params:
                        for nome_param in p[1]:
                            local_vars[nome_param] = pos_local
                            escrever("pushi 0")  # espaço
                            pos_local += 1
                    for bloco_vars in func_decls:
                        for v in bloco_vars:
                            if v[0] == 'var_decl':
                                for nome in v[1]:
                                    local_vars[nome] = pos_local
                                    escrever("pushi 0")
                                    pos_local += 1
                    local_vars[nome_func] = pos_local  # para o valor de retorno
                    escrever("pushi 0")
                    gerar_bloco(func_bloco, local_vars)
                    escrever("pushg 0")  # simplificação para return
                    escrever("return")

    # Escreve na pasta
    pasta_saida = "codigoVM"
    os.makedirs(pasta_saida, exist_ok=True)
    nome_out = os.path.splitext(os.path.basename(nome_ficheiro))[0] + ".vm"
    caminho_out = os.path.join(pasta_saida, nome_out)
    with open(caminho_out, 'w') as f:
        for linha in output:
            f.write(linha + "\n")

def gerar_bloco(bloco, vars):
    _, instrucoes = bloco
    for instr in instrucoes:
        if instr:
            gerar_instr(instr, vars)

def gerar_instr(instr, vars):
    tipo = instr[0]

    if tipo == 'assign':
        _, var, _, expr = instr
        gerar_expr(expr, vars)
        if var in vars:
            escrever(f"storeg {vars[var]}")
        else:
            raise Exception(f"Variável '{var}' não encontrada no contexto.")

    elif tipo == 'read':
        _, var = instr
        escrever("read")
        escrever("atoi")
        escrever(f"storeg {vars[var[1]]}")

    elif tipo == 'write':
        _, modo, exprs = instr
        for e in exprs:
            gerar_expr(e, vars)
            escrever("writes") if inferir_tipo_literal(e) == 'string' else escrever("writei")
        if modo == 'writeln':
            escrever("writeln")

    elif tipo == 'if':
        _, cond, then_instr, else_instr = instr
        label_fim = nova_label("ENDIF")
        label_senao = nova_label("ELSE") if else_instr else label_fim

        gerar_expr(cond, vars)
        escrever(f"jz {label_senao}")
        gerar_instr(then_instr, vars)
        if else_instr:
            escrever(f"jump {label_fim}")
            escrever(f"{label_senao}:")
            gerar_instr(else_instr, vars)
        escrever(f"{label_fim}:")

    elif tipo == 'while':
        _, cond, corpo = instr
        label_inicio = nova_label("WHILE")
        label_fim = nova_label("ENDWHILE")

        escrever(f"{label_inicio}:")
        gerar_expr(cond, vars)
        escrever(f"jz {label_fim}")
        gerar_instr(corpo, vars)
        escrever(f"jump {label_inicio}")
        escrever(f"{label_fim}:")

    elif tipo == 'for':
        _, var, inicio, fim, corpo, direcao = instr
        gerar_expr(inicio, vars)
        escrever(f"storeg {vars[var]}")
        label_inicio = nova_label("FOR")
        label_fim = nova_label("ENDFOR")

        escrever(f"{label_inicio}:")
        escrever(f"pushg {vars[var]}")
        gerar_expr(fim, vars)
        escrever("inf" if direcao == 'to' else "sup")
        escrever(f"jz {label_fim}")
        gerar_instr(corpo, vars)
        escrever(f"pushg {vars[var]}")
        escrever("pushi 1")
        escrever("add" if direcao == 'to' else "sub")
        escrever(f"storeg {vars[var]}")
        escrever(f"jump {label_inicio}")
        escrever(f"{label_fim}:")

    elif tipo == 'block':
        _, instrs = instr
        for i in instrs:
            if i is not None:
                gerar_instr(i, vars)

def gerar_expr(expr, vars):
    if isinstance(expr, tuple):
        tipo = expr[0]

        if tipo == 'num':
            escrever(f"pushi {expr[1]}")
        elif tipo == 'str':
            escrever(f"pushs \"{expr[1]}\"")
        elif tipo == 'bool':
            escrever("pushi 1" if expr[1] else "pushi 0")
        elif tipo == 'var':
            escrever(f"pushg {vars[expr[1]]}")
        elif tipo == 'call':
            for arg in expr[2]:
                gerar_expr(arg, vars)
            escrever("pushn 1")  # espaço para o return
            escrever(f"call {expr[1]}")
        elif tipo == '+':
            gerar_expr(expr[1], vars)
            gerar_expr(expr[2], vars)
            escrever("add")
        elif tipo == '-':
            gerar_expr(expr[1], vars)
            gerar_expr(expr[2], vars)
            escrever("sub")
        elif tipo == '*':
            gerar_expr(expr[1], vars)
            gerar_expr(expr[2], vars)
            escrever("mul")
        elif tipo == 'div':
            gerar_expr(expr[1], vars)
            gerar_expr(expr[2], vars)
            escrever("div")
        elif tipo == 'mod':
            gerar_expr(expr[1], vars)
            gerar_expr(expr[2], vars)
            escrever("mod")
        elif tipo == '=':
            gerar_expr(expr[1], vars)
            gerar_expr(expr[2], vars)
            escrever("equal")
        elif tipo == '<':
            gerar_expr(expr[1], vars)
            gerar_expr(expr[2], vars)
            escrever("inf")
        elif tipo == '<=':
            gerar_expr(expr[1], vars)
            gerar_expr(expr[2], vars)
            escrever("infeq")
        elif tipo == '>':
            gerar_expr(expr[1], vars)
            gerar_expr(expr[2], vars)
            escrever("sup")
        elif tipo == '>=':
            gerar_expr(expr[1], vars)
            gerar_expr(expr[2], vars)
            escrever("supeq")
        elif tipo == '<>':
            gerar_expr(expr[1], vars)
            gerar_expr(expr[2], vars)
            escrever("equal")
            escrever("not")
        elif tipo == 'not':
            gerar_expr(expr[1], vars)
            escrever("not")
        elif tipo == 'and':
            gerar_expr(expr[1], vars)
            gerar_expr(expr[2], vars)
            escrever("and")
        elif tipo == 'or':
            gerar_expr(expr[1], vars)
            gerar_expr(expr[2], vars)
            escrever("or")
        elif tipo == 'array_access':
            gerar_expr(expr[2], vars)
            escrever(f"pushg {vars[expr[1]]}")
            escrever("add")
            escrever("loadn")
        else:
            raise NotImplementedError(f"Expressão não suportada: {expr}")

def inferir_tipo_literal(expr):
    if isinstance(expr, tuple) and expr[0] == 'str':
        return 'string'
    elif isinstance(expr, tuple) and expr[0] == 'num':
        return 'integer'
    return 'integer'
