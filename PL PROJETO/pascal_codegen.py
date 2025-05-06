import os
from pascal_seman import verificar_semantica

# Gera código VM a partir de AST Pascal (1-based strings ajustado a 0-based)
label_counter = 0
output = []


def nova_label(prefix="L"):
    global label_counter
    label = f"{prefix}{label_counter}"
    label_counter += 1
    return label


def escrever(instr):
    output.append(instr)


def gerar_codigo(ast, nome_ficheiro="programa.pas"):
    """
    Traduz uma AST Pascal para instruções da VM EWVM,
    ajustando índices de string (Pascal 1-based → VM 0-based).
    """
    verificar_semantica(ast)
    global output, label_counter
    output = []
    label_counter = 0

    _, _, declaracoes, bloco = ast

    # Mapas de variáveis: posição e tipo
    global_vars = {}
    var_types = {}
    pos = 0

    # Alocar variáveis globais e registar tipo
    for decl_list in declaracoes:
        if isinstance(decl_list, list):
            for d in decl_list:
                if d[0] == 'var_decl':
                    _, nomes, tipo = d
                    for var in nomes:
                        t = tipo.lower()
                        var_types[var] = t
                        if t == 'string':
                            # string vazia
                            escrever('pushs ""')
                        else:
                            # inteiro 0
                            escrever('pushi 0')
                        escrever(f'storeg {pos}')
                        global_vars[var] = pos
                        pos += 1

    # Início do programa
    escrever('start')
    gerar_bloco(bloco, global_vars, var_types)
    escrever('stop')

    # Gravar .vm
    pasta = 'codigoVM'
    os.makedirs(pasta, exist_ok=True)
    base = os.path.splitext(os.path.basename(nome_ficheiro))[0]
    out = os.path.join(pasta, base + '.vm')
    with open(out, 'w') as f:
        f.write("\n".join(output))


def gerar_bloco(bloco, vars_idx, vars_type):
    _, instrs = bloco
    for instr in instrs:
        if instr:
            gerar_instr(instr, vars_idx, vars_type)


def gerar_instr(instr, vars_idx, vars_type):
    tipo_instr = instr[0]

    if tipo_instr == 'assign':
        _, var, _, expr = instr
        gerar_expr(expr, vars_idx, vars_type)
        escrever(f'storeg {vars_idx[var]}')

    elif tipo_instr == 'read':
        _, var = instr
        name = var[1]
        escrever('read')
        if vars_type[name] != 'string':
            escrever('atoi')
        escrever(f'storeg {vars_idx[name]}')

    elif tipo_instr == 'write':
        _, modo, exprs = instr
        for e in exprs:
            gerar_expr(e, vars_idx, vars_type)
            if isinstance(e, tuple) and e[0] == 'str':
                escrever('writes')
            else:
                escrever('writei')
        if modo == 'writeln':
            escrever('writeln')

    elif tipo_instr == 'if':
        _, cond, entao, senao = instr
        lbl_else = nova_label('ELSE') if senao else None
        lbl_end = nova_label('ENDIF')

        gerar_expr(cond, vars_idx, vars_type)
        escrever(f'jz {lbl_else or lbl_end}')
        gerar_instr(entao, vars_idx, vars_type)
        if senao:
            escrever(f'jump {lbl_end}')
            escrever(f'{lbl_else}:')
            gerar_instr(senao, vars_idx, vars_type)
        escrever(f'{lbl_end}:')

    elif tipo_instr == 'while':
        _, cond, corpo = instr
        lbl_in = nova_label('WHILE')
        lbl_out = nova_label('ENDWHILE')
        escrever(f'{lbl_in}:')
        gerar_expr(cond, vars_idx, vars_type)
        escrever(f'jz {lbl_out}')
        gerar_instr(corpo, vars_idx, vars_type)
        escrever(f'jump {lbl_in}')
        escrever(f'{lbl_out}:')

    elif tipo_instr == 'for':
        # ('for', var, inicio, fim, bloco, direcao)
        _, var, inicio, fim, bloco_for, direcao = instr
        lbl_start = nova_label('FOR')
        lbl_end   = nova_label('ENDFOR')
        # inicializar contador
        gerar_expr(inicio, vars_idx, vars_type)
        escrever(f'storeg {vars_idx[var]}')
        escrever(f'{lbl_start}:')
        # checar condição
        escrever(f'pushg {vars_idx[var]}')
        gerar_expr(fim, vars_idx, vars_type)
        if direcao == 'downto':
            escrever('supeq')
        else:
            escrever('infeq')
        escrever(f'jz {lbl_end}')
        # corpo
        gerar_instr(bloco_for, vars_idx, vars_type)
        # passo
        escrever(f'pushg {vars_idx[var]}')
        escrever('pushi 1')
        escrever('sub' if direcao=='downto' else 'add')
        escrever(f'storeg {vars_idx[var]}')
        escrever(f'jump {lbl_start}')
        escrever(f'{lbl_end}:')

    elif tipo_instr == 'block':
        for sub in instr[1]:
            if sub:
                gerar_instr(sub, vars_idx, vars_type)

    else:
        raise NotImplementedError(f'Instrucao {tipo_instr} nao suportada')


def gerar_expr(expr, vars_idx, vars_type):
    if not isinstance(expr, tuple):
        raise TypeError(f'Expr invalida: {expr}')

    tipo = expr[0]
    if tipo == 'num':
        escrever(f'pushi {expr[1]}')
    elif tipo == 'str':
        # string literal: se for char simples, empilha código ASCII, senão heap
        s = expr[1]
        if len(s) == 1:
            escrever(f'pushi {ord(s)}')
        else:
            escrever(f'pushs "{s}"')
    elif tipo == 'var':
        escrever(f'pushg {vars_idx[expr[1]]}')

    elif tipo == 'array_access':
        # Pascal strings are 1-based → ajustar a 0-based
        _, nome_arr, idx = expr
        # endereço de string
        escrever(f'pushg {vars_idx[nome_arr]}')
        # índice Pascal
        gerar_expr(idx, vars_idx, vars_type)
        # ajustar para 0-based
        escrever('pushi 1')
        escrever('sub')
        # extrair char
        escrever('charat')

    elif tipo in ('+', '-', '*', 'div', 'mod', '=', '<>', '<', '<=', '>', '>=', 'and', 'or'):
        op_map = {
            '+':'add','-':'sub','*':'mul','div':'div','mod':'mod',
            '=':'equal','<>':'equal; not','<':'inf','<=':'infeq',
            '>':'sup','>=':'supeq','and':'and','or':'or'
        }
        gerar_expr(expr[1], vars_idx, vars_type)
        gerar_expr(expr[2], vars_idx, vars_type)
        for cmd in op_map[tipo].split(';'):
            escrever(cmd.strip())

    elif tipo == 'not':
        gerar_expr(expr[1], vars_idx, vars_type)
        escrever('not')

    elif tipo == 'bool':
        escrever('pushi ' + ('1' if expr[1] else '0'))

    elif tipo == 'call':
        _, nome, args = expr
        if nome.lower() == 'length':
            gerar_expr(args[0], vars_idx, vars_type)
            escrever('strlen')
        else:
            for a in args:
                gerar_expr(a, vars_idx, vars_type)
            escrever(f'pusha {nome}')
            escrever('call')

    else:
        raise NotImplementedError(f'Expressao {tipo} nao suportada')
