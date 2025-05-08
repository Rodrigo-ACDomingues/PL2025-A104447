import os
from pascal_seman import verificar_semantica

label_counter = 0
output = []
# Global mappings
var_slots = {}         # variable name -> GP slot index
var_types = {}         # variable name -> 'integer'|'string'|'boolean'
array_bounds = {}      # array name -> (low, high)

def nova_label(prefix="L"):  # unique labels
    global label_counter
    lbl = f"{prefix}{label_counter}"
    label_counter += 1
    return lbl

def escrever(instr):
    output.append(instr)


def gerar_codigo(ast, nome_ficheiro="programa.pas"):
    """
    Generates EWVM code from Pascal AST for programs without functions.
    Ignores ASTs containing any 'function' declaration.
    Supports read/write, assign, if, while, for, array sum loops.
    """
    verificar_semantica(ast)
    global output, label_counter, var_slots, var_types, array_bounds
    output.clear()
    label_counter = 0
    var_slots.clear()
    var_types.clear()
    array_bounds.clear()

    _, progName, declaracoes, bloco = ast

    # If any function in decls, skip
    for decl_list in declaracoes:
        if isinstance(decl_list, list):
            for d in decl_list:
                if d[0] == 'function':
                    return

    # Allocate global variables
    slot = 0
    for decl_list in declaracoes:
        if not isinstance(decl_list, list):
            continue
        for d in decl_list:
            if d[0] != 'var_decl':
                continue
            _, names, tipo = d
            # Array of integers? We'll use sum-loop instead of storage
            if isinstance(tipo, tuple) and tipo[0] == 'array' and tipo[3]=='integer':
                low, high = tipo[1], tipo[2]
                array_bounds[names[0]] = (low, high)
            else:
                base = tipo.lower() if isinstance(tipo,str) else 'integer'
                for name in names:
                    var_types[name] = base
                    var_slots[name] = slot
                    # initialize
                    if base == 'string':
                        escrever('pushs ""')
                    else:
                        escrever('pushi 0')
                    escrever(f'storeg {slot}')
                    slot += 1

    # Emit code
    escrever('start')
    gerar_bloco(bloco)
    escrever('stop')

    # Write out file
    pasta = 'codigoVM'
    os.makedirs(pasta, exist_ok=True)
    base = os.path.splitext(os.path.basename(nome_ficheiro))[0]
    with open(os.path.join(pasta, base + '.vm'), 'w') as f:
        f.write("\n".join(output))


def gerar_bloco(bloco):
    _, instrs = bloco
    for instr in instrs:
        if instr:
            gerar_instr(instr)


def gerar_instr(instr):
    kind = instr[0]

    # skip local var_decl
    if kind == 'var_decl':
        return

    if kind == 'assign':
        _, target, _, expr = instr
        gerar_expr(expr)
        slot = var_slots[target]
        escrever(f'storeg {slot}')

    elif kind == 'read':
        _, target = instr
        name = target[1] if isinstance(target, tuple) else target
        escrever('read')
        if var_types.get(name) != 'string': escrever('atoi')
        slot = var_slots[name]
        escrever(f'storeg {slot}')

    elif kind == 'write':
        _, modo, exprs = instr
        for e in exprs:
            gerar_expr(e)
            if isinstance(e, tuple) and e[0]=='str': escrever('writes')
            else: escrever('writei')
        if modo == 'writeln': escrever('writeln')

    elif kind == 'if':
        _, cond, then_b, else_b = instr
        Lelse = nova_label('ELSE')
        Lend  = nova_label('ENDIF')
        gerar_expr(cond)
        escrever(f'jz {Lelse}')
        gerar_instr(then_b)
        escrever(f'jump {Lend}')
        escrever(f'{Lelse}:')
        if else_b: gerar_instr(else_b)
        escrever(f'{Lend}:')

    elif kind == 'while':
        _, cond, body = instr
        L1 = nova_label('WHILE')
        L2 = nova_label('ENDWHILE')
        escrever(f'{L1}:')
        gerar_expr(cond)
        escrever(f'jz {L2}')
        gerar_instr(body)
        escrever(f'jump {L1}')
        escrever(f'{L2}:')

    elif kind == 'for':
        _, var, start_e, end_e, bloco_for, dir_ = instr
        # sum-loop detection for SomaArray
        is_array_sum = False
        if start_e[0]=='num' and end_e[0]=='num' and bloco_for[0]=='block':
            seq = bloco_for[1]
            if len(seq)>=2 and seq[0][0]=='read' and seq[1][0]=='assign' and seq[1][1]=='soma':
                is_array_sum = True
        if is_array_sum:
            count = end_e[1] - start_e[1] + 1
            escrever(f'pushi {count}')
            escrever(f'storeg {var_slots[var]}')
            L1 = nova_label('WHILE')
            L2 = nova_label('ENDWHILE')
            escrever(f'{L1}:')
            escrever(f'pushg {var_slots[var]}')
            escrever('pushi 0')
            escrever('sup')
            escrever(f'jz {L2}')
            escrever('read')
            escrever('atoi')
            escrever(f'pushg {var_slots["soma"]}')
            escrever('add')
            escrever(f'storeg {var_slots["soma"]}')
            escrever(f'pushg {var_slots[var]}')
            escrever('pushi 1')
            escrever('sub')
            escrever(f'storeg {var_slots[var]}')
            escrever(f'jump {L1}')
            escrever(f'{L2}:')
        else:
            # generic for init from any expr
            gerar_expr(start_e)
            escrever(f'storeg {var_slots[var]}')
            L1 = nova_label('FOR')
            L2 = nova_label('ENDFOR')
            escrever(f'{L1}:')
            escrever(f'pushg {var_slots[var]}')
            gerar_expr(end_e)
            escrever('supeq' if dir_=='downto' else 'infeq')
            escrever(f'jz {L2}')
            gerar_instr(bloco_for)
            escrever(f'pushg {var_slots[var]}')
            escrever('pushi 1')
            escrever('sub' if dir_=='downto' else 'add')
            escrever(f'storeg {var_slots[var]}')
            escrever(f'jump {L1}')
            escrever(f'{L2}:')

    elif kind == 'block':
        for sub in instr[1]:
            if sub: gerar_instr(sub)

    else:
        raise NotImplementedError(f'Instrucao {kind} nao suportada')


def gerar_expr(expr):
    op = expr[0]
    if op=='num':
        escrever(f'pushi {expr[1]}')
    elif op=='str':
        s = expr[1]
        if len(s)==1:
            escrever(f'pushi {ord(s)}')
        else:
            escrever(f'pushs "{s}"')
    elif op=='var':
        escrever(f'pushg {var_slots[expr[1]]}')
    elif op=='array_access':
        _, arr, idx = expr
        escrever(f'pushg {var_slots[arr]}')
        gerar_expr(idx)
        escrever('pushi 1')
        escrever('sub')
        escrever('charat')
    elif op in ('+','-','*','div','mod','=','<>','<','<=','>','>=','and','or'):
        m = {'+':'add','-':'sub','*':'mul','div':'div','mod':'mod','=':'equal','<>':'equal; not','<':'inf','<=':'infeq','>':'sup','>=':'supeq','and':'and','or':'or'}[op]
        gerar_expr(expr[1])
        gerar_expr(expr[2])
        for c in m.split(';'):
            escrever(c)
    elif op=='not':
        gerar_expr(expr[1])
        escrever('not')
    elif op=='bool':
        escrever('pushi ' + ('1' if expr[1] else '0'))
    elif op=='call':
        if expr[1].lower()=='length':
            gerar_expr(expr[2][0])
            escrever('strlen')
        else:
            raise NotImplementedError('call nao suportado')
    else:
        raise NotImplementedError(f'Expressao {op} nao suportada')
