import ply.lex as lex

tokens = (
    'INT',
    'REAL',
    'PALAVRA',
    'BOOLEANO',
    'FIM'
)

def t_INT(t):
    r'\d+'
    return t

def t_REAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_FIM(t):
    r'fim'
    return t

def t_BOOLEANO(t):
    r'(True|False)'
    t.value = True if t.value == 'True' else False 
    return t

def t_PALAVRA(t):
    r'\w+'
    return t

t_ignore = ' \t'

def t_error(t):
    print(f"Carácter ilegal {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()

def analisar_entrada(lista):
    entrada = ' '.join(map(str, lista))
    
    lexer.input(entrada) 
    
    tokens_encontrados = []
    while True:
        tok = lexer.token()
        if not tok:
            break 
        tokens_encontrados.append((tok.value, tok.type))
    
    return tokens_encontrados

entrada = [1, 5, 'palavra', False, 3.14, 0, 'fim']

resultado = analisar_entrada(entrada)
for valor, tipo in resultado:
    print(f"{valor}: {tipo}")
