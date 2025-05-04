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

def tipo_var(nome, vars):
    if nome.lower() == "bin":
        return "string"
    return "integer"

def gerar_codigo(ast, nome_ficheiro="programa.pas"):
    verificar_semantica(ast)
    global output, label_counter
    output = []
    label_counter = 0

    tipo, nome, declaracoes, bloco = ast

    global_vars = {}
    pos = 0
    for decl in declaracoes:
        if isinstance(decl, list):
            for d in decl:
                if d[0] == 'var_decl':
                    tipo = d[2]
                    for var in d[1]:
                        tipo = d[2]
                        if isinstance(tipo, tuple) and tipo[0] == 'array':
                            tamanho = tipo[2] - tipo[1] + 1
                            escrever(f"pushi {tamanho}")
                            escrever("allocn")
                        else:
                            escrever("pushi 0")
                        escrever(f"storeg {pos}")
                        global_vars[var] = pos
                        pos += 1

    escrever("start")
    gerar_bloco(bloco, global_vars)
    escrever("stop")

    for decl in declaracoes:
        if isinstance(decl, list):
            for d in decl:
                if d[0] == 'function':
                    nome_func, params, _, func_decls, func_bloco = d[1:]
                    escrever(f"{nome_func}:")
                    escrever("start")
                    local_vars = {}

                    for idx, p in enumerate(params):
                        for nome_param in p[1]:
                            local_vars[nome_param] = ('param', -1 - idx)

                    pos_local = 0
                    for bloco_vars in func_decls:
                        for v in bloco_vars:
                            if v[0] == 'var_decl':
                                for nome in v[1]:
                                    local_vars[nome] = ('local', pos_local)
                                    escrever("pushi 0")
                                    pos_local += 1

                    local_vars[nome_func] = ('local', pos_local)
                    escrever("pushi 0")
                    gerar_bloco(func_bloco, local_vars)
                    ret_pos = local_vars[nome_func][1]
                    escrever(f"pushl {ret_pos}")
                    escrever("return")

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

        if isinstance(var, tuple) and var[0] == 'array_access':
            arr_name = var[1]
            index_expr = var[2]
            gerar_expr(('var', arr_name), vars)
            gerar_expr(index_expr, vars)
            gerar_expr(expr, vars)
            escrever("storen")
        else:
            gerar_expr(expr, vars)
            if var in vars:
                pos = vars[var]
                if isinstance(pos, tuple):
                    if pos[0] == 'local':
                        escrever(f"storel {pos[1]}")
                    elif pos[0] == 'param':
                        escrever("pushfp")
                        escrever(f"store {pos[1]}")
                else:
                    escrever(f"storeg {pos}")
            else:
                raise Exception(f"Variável '{var}' não encontrada no contexto.")

    elif tipo == 'read':
        _, var = instr
        if isinstance(var, tuple) and var[0] == 'array_access':
            gerar_expr(('var', var[1]), vars)
            gerar_expr(var[2], vars)
            escrever("read")
            escrever("dup 1")
            nome = var[1]
            if tipo_var(nome, vars) != "string":
                escrever("atoi")
            escrever("storen")
        else:
            escrever("read")
            escrever("dup 1")
            nome = var[1]
            if tipo_var(nome, vars) != "string":
                escrever("atoi")
            if nome in vars:
                pos = vars[nome]
                if isinstance(pos, tuple):
                    if pos[0] == 'local':
                        escrever(f"storel {pos[1]}")
                    elif pos[0] == 'param':
                        escrever("pushfp")
                        escrever(f"store {pos[1]}")
                else:
                    escrever(f"storeg {pos}")
            else:
                raise Exception(f"Variável '{nome}' não encontrada no contexto.")

    elif tipo == 'write':
        _, modo, exprs = instr
        for e in exprs:
            gerar_expr(e, vars)
            if isinstance(e, tuple) and e[0] == 'str':
                escrever("writes")
            else:
                escrever("writei")
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
        escrever("infeq" if direcao == 'to' else "supeq")
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
        elif tipo == 'var':
            if expr[1] in vars:
                pos = vars[expr[1]]
                if isinstance(pos, tuple):
                    if pos[0] == 'local':
                        escrever(f"pushl {pos[1]}")
                    elif pos[0] == 'param':
                        escrever("pushfp")
                        escrever(f"load {pos[1]}")
                else:
                    escrever(f"pushg {pos}")
        elif tipo == 'bool':
            escrever("pushi 1" if expr[1] else "pushi 0")
        elif tipo == 'call':
            nome_func = expr[1]
            args = expr[2]
            if nome_func == 'length':
                gerar_expr(args[0], vars)
                escrever("strlen")
            else:
                for arg in args:
                    gerar_expr(arg, vars)
                escrever(f"pusha {nome_func}")
                escrever("call")
        elif tipo in ('+', '-', '*', 'div', 'mod', '=', '<', '<=', '>', '>=', '<>', 'and', 'or'):
            gerar_expr(expr[1], vars)
            gerar_expr(expr[2], vars)
            operadores = {
                '+': 'add', '-': 'sub', '*': 'mul', 'div': 'div', 'mod': 'mod',
                '=': 'equal', '<': 'inf', '<=': 'infeq', '>': 'sup', '>=': 'supeq',
                '<>': ('equal', 'not'), 'and': 'and', 'or': 'or'
            }
            instrucao = operadores[tipo]
            if isinstance(instrucao, tuple):
                for inst in instrucao:
                    escrever(inst)
            else:
                escrever(instrucao)
        elif tipo == 'not':
            gerar_expr(expr[1], vars)
            escrever("not")
        elif tipo == 'array_access':
            nome = expr[1]
            if tipo_var(nome, vars) == 'string':
                gerar_expr(('var', nome), vars)    
                gerar_expr(expr[2], vars)           
                escrever("pushi 1")
                escrever("sub")                      
                escrever("charat")
            else:
                gerar_expr(('var', nome), vars)
                gerar_expr(expr[2], vars)
                escrever("loadn")

        else:
            raise NotImplementedError(f"Expressão não suportada: {expr}")
