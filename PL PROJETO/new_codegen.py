import os

class GeradorVM:
    def __init__(self):
        self.codigo = []                # Instruções VM
        self.variaveis = {}             # nome → índice
        self.vars = self.variaveis      # alias para compatibilidade
        self.arrays = {}                # nome → (inicio, fim, tipo)
        self.labels = 0                 # contador para labels únicos
        self.proximo_indice = 0         # próximo endereço de memória global
        self.acesso_manual = False       # acesso manual a arrays

    def emit(self, instrucao, argumento=None):
        if argumento is not None:
            self.codigo.append(f"{instrucao} {argumento}")
        else:
            self.codigo.append(instrucao)
            
    def gerar_call(self, expr):
        # expr = ('call', 'nome_funcao', [arg1, arg2, ...])
        _, nome_funcao, argumentos = expr

        # 1. Empilhar os argumentos (ordem: esquerda → direita)
        for arg in argumentos:
            self.gerar_expr(arg)

        # 2. Gerar a chamada
        self.codigo.append(f"call {nome_funcao}")


    def nova_label(self, base):
        self.labels += 1
        return f"{base.upper()}{self.labels}"

    def declarar_variaveis(self, declaracoes):
        for decl in declaracoes:
            if decl[0] == 'var_decl':
                nomes = decl[1]
                tipo = decl[2]
                for nome in nomes:
                    self.variaveis[nome] = self.proximo_indice
                    if isinstance(tipo, tuple) and tipo[0] == 'array':
                        inicio, fim, _ = tipo[1], tipo[2], tipo[3]
                        self.arrays[nome] = (inicio, fim)
                        for i in range(inicio, fim + 1):
                            self.codigo.append(f"pushi 0  // {nome}_{i}")
                            self.proximo_indice += 1
                    elif tipo == 'string':
                        # assume strings até 100 caracteres
                        self.arrays[nome] = (1, 100)
                        for i in range(1, 101):
                            self.codigo.append(f"pushi 0  // {nome}_{i}")
                            self.proximo_indice += 1
                    else:
                        self.codigo.append(f"pushi 0  // {nome}")
                        self.proximo_indice += 1

    def gerar(self, ast):
        if not isinstance(ast, tuple) or ast[0] != 'program':
            raise Exception(f"AST inválida ou inesperada: {ast}")

        if len(ast) == 4:
            _, nome, declaracoes, bloco = ast
        elif len(ast) == 5:
            _, nome, funcoes, declaracoes, bloco = ast
            # Junta as funções às declarações
            declaracoes = funcoes + [declaracoes]
        else:
            raise Exception(f"AST inesperada (esperado 4 ou 5 elementos): {ast}")

        self.codigo.append("// Declaração de variáveis")
        for d in declaracoes:
            if isinstance(d, list):
                self.declarar_variaveis(d)
            elif isinstance(d, tuple) and d[0] == 'var_decl':
                self.declarar_variaveis([d])
            # Funções são ignoradas por enquanto

        self.codigo.append("start")
        self.gerar_bloco(bloco)
        self.codigo.append("stop")
        return self.codigo

    def gerar_bloco(self, bloco):
        _, instrucoes = bloco
        for instr in instrucoes:
            if instr:
                self.gerar_instrucao(instr)

    def gerar_instrucao(self, instr):
        tipo = instr[0]

        if tipo == 'assign':
            _, nome, _, expr = instr
            self.gerar_expr(expr)
            if isinstance(nome, str):
                idx = self.vars[nome]
                self.codigo.append(f"storeg {idx}")
            elif nome[0] == 'array_access':
                self.gerar_array_store(nome[1], nome[2])

        elif tipo == 'write':
            _, modo, exprs = instr
            for e in exprs:
                self.gerar_expr(e)
                if e[0] == 'str':
                    self.codigo.append("writes")
                elif e[0] == 'var' and self.is_string_var(e[1]):
                    self.codigo.append("writes")
                else:
                    self.codigo.append("writei")
            if modo == 'writeln':
                self.codigo.append("writeln")

        elif tipo == 'read':
            _, alvo = instr
            self.codigo.append("read")
            self.codigo.append("atoi")
            if alvo[0] == 'var':
                idx = self.vars[alvo[1]]
                self.codigo.append(f"storeg {idx}")
            elif alvo[0] == 'array_access':
                self.gerar_array_store(alvo[1], alvo[2])

        elif tipo == 'if':
            _, cond, then_instr, else_instr = instr
            label_else = self.nova_label("else")
            label_end = self.nova_label("endif")
            self.gerar_expr(cond)
            self.codigo.append(f"jz {label_else}")
            self.gerar_instrucao(then_instr)
            self.codigo.append(f"jump {label_end}")
            self.codigo.append(f"{label_else}:")
            if else_instr:
                self.gerar_instrucao(else_instr)
            self.codigo.append(f"{label_end}:")

        elif tipo == "for":
            var, inicio, fim, corpo, direcao = instr[1:]

            self.gerar_expr(inicio)        # expr de início
            self.emit("storeg", self.vars[var])  # i := inicio

            label_inicio = self.nova_label()
            label_fim = self.nova_label()

            self.emit(f"{label_inicio}:")
            self.emit("pushg", self.vars[var])   # i
            self.gerar_expr(fim)                 # n
            self.emit("infeq")                   # i <= n
            self.emit("jz", label_fim)           # if not (i <= n) jump fim

            self.gerar_instrucao(corpo)          # corpo do ciclo

            self.emit("pushg", self.vars[var])
            self.emit("pushi", 1)
            self.emit("add")
            self.emit("storeg", self.vars[var])  # i := i + 1
            self.emit("jump", label_inicio)
            self.emit(f"{label_fim}:")

        elif tipo == 'block':
            self.gerar_bloco(instr)

    def gerar_expr(self, expr):
        if expr[0] == 'num':
            self.codigo.append(f'pushi {expr[1]}')
        elif expr[0] == 'bool':
            self.codigo.append(f'pushi {1 if expr[1] else 0}')
        elif expr[0] == 'var':
            idx = self.variaveis[expr[1]]
            self.codigo.append(f'pushg {idx}')
        elif expr[0] == 'str':
            self.codigo.append(f'pushs "{expr[1]}"')
        elif expr[0] == 'call':
            self.gerar_call(expr)
        elif expr[0] == 'array_access':
            nome = expr[1]
            indice = expr[2]
            if self.acesso_manual:
                # Acesso manual até 100 elementos
                for i in range(1, 101):
                    if indice[0] == 'num':
                        self.codigo.append(f'pushi {indice[1]}')
                    elif indice[0] == 'var':
                        self.codigo.append(f'pushg {self.variaveis[indice[1]]}')
                    self.codigo.append(f'pushi {i}')
                    self.codigo.append('equal')
                    self.codigo.append(f'jz NEXT_{i}')
                    self.codigo.append(f'pushg {self.variaveis[f"{nome}_{i}"]}')
                    self.codigo.append(f'jump ENDARRAY_{nome}')
                    self.codigo.append(f'NEXT_{i}:')
                self.codigo.append(f'pushi 0  // valor por defeito')
                self.codigo.append(f'ENDARRAY_{nome}:')
            else:
                self.codigo.append(f'pushg {self.variaveis[nome]}')
                if indice[0] == 'num':
                    self.codigo.append(f'pushi {indice[1]}')
                elif indice[0] == 'var':
                    self.codigo.append(f'pushg {self.variaveis[indice[1]]}')
                self.codigo.append('charat')
        elif expr[0] in ('+', '-', '*', 'div', 'mod', '=', '<>', '<', '<=', '>', '>=', 'and', 'or'):
            self.gerar_expr(expr[1])
            self.gerar_expr(expr[2])
            op_map = {
                '+': 'add', '-': 'sub', '*': 'mul', 'div': 'div', 'mod': 'mod',
                '=': 'equal', '<>': 'equal\nnot', '<': 'inf', '<=': 'infeq',
                '>': 'sup', '>=': 'supeq', 'and': 'and', 'or': 'or'
            }
            self.codigo.append(op_map[expr[0]])
        elif expr[0] == 'not':
            self.gerar_expr(expr[1])
            self.codigo.append('not')

        elif expr[0] == 'call':
            self.gerar_call(expr)

        else:
            raise Exception(f"Expressão inválida: {expr}")


    def gerar_array_access(self, nome, index_expr):
        for i in range(self.arrays[nome][0], self.arrays[nome][1] + 1):
            idx = i - self.arrays[nome][0] + 1
            label_next = self.nova_label("next")
            label_end = self.nova_label("fim")

            self.gerar_expr(index_expr)  # empilha o índice dinâmico
            self.codigo.append(f"pushi {idx}")
            self.codigo.append("equal")
            self.codigo.append(f"jz {label_next}")
            self.codigo.append(f"pushg {i}")
            self.codigo.append(f"jump {label_end}")
            self.codigo.append(f"{label_next}:")
        self.codigo.append(f"{label_end}:")

    def gerar_array_store(self, nome, index_expr):
        for i in range(self.arrays[nome][0], self.arrays[nome][1] + 1):
            idx = i - self.arrays[nome][0] + 1
            label_next = self.nova_label("nexts")
            label_end = self.nova_label("fims")

            self.gerar_expr(index_expr)
            self.codigo.append(f"pushi {idx}")
            self.codigo.append("equal")
            self.codigo.append(f"jz {label_next}")
            self.codigo.append("swap")
            self.codigo.append(f"storeg {i}")
            self.codigo.append(f"jump {label_end}")
            self.codigo.append(f"{label_next}:")
        self.codigo.append(f"{label_end}:")

    def is_string_var(self, nome):
        return nome in self.vars and nome.startswith("bin")
    
def gerar_codigo(ast, nome_ficheiro):
    nome_base = os.path.splitext(nome_ficheiro)[0]
    gerador = GeradorVM()
    codigo_vm = gerador.gerar(ast)

    os.makedirs("codigoVM", exist_ok=True)
    with open(f"codigoVM/{nome_base}.vm", "w") as f:
        f.write("\n".join(codigo_vm))