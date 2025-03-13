import ply.lex as lex

# Definindo os estados
states = (
    ('somadoron', 'inclusive'),  # O estado 'somadoron' é 'inclusive', ou seja, ele é ativado pela palavra 'ON' e desativado por 'OFF'
)

# Definindo os tokens
tokens = (
    'NUMBER',
    'ON',
    'OFF',
    'EQUALS',
)

# Variável global para o somador
somador = 0

# Regras para os tokens
def t_somadoron_NUMBER(t):
    r'-?\d+'  # Reconhece números inteiros, positivos ou negativos
    t.value = int(t.value)
    t.lexer.somador += t.value  # Atualiza o valor do somador
    return t

def t_NUMBER(t):
    r'-?\d+'  # Reconhece números inteiros
    t.value = int(t.value)
    return t

def t_ON(t):
    r'(?i:on)'  # Reconhece 'ON' (case-insensitive)
    t.lexer.begin('somadoron')  # Muda para o estado 'somadoron'
    return t

def t_OFF(t):
    r'(?i:off)'  # Reconhece 'OFF' (case-insensitive)
    t.lexer.begin('INITIAL')  # Retorna ao estado inicial
    return t

def t_EQUALS(t):
    r'\='  # Reconhece o símbolo '='
    print(f"Somador: {t.lexer.somador}")  # Imprime o valor atual do somador
    return t

def t_error(t):
    print(f"Símbolo inválido na linha {t.lineno}, {t.value[0]}")
    t.lexer.skip(1)

# Ignorar espaços em branco e tabulação
t_ignore = ' \t'

# Criando o lexer
lexer = lex.lex()

# Inicializando a variável somador
lexer.somador = 0

# Entrada para o lexer
lexer.input("ON 3 5 OFF 2 =")  # Exemplo de entrada

# Processando os tokens
while (tok := lexer.token()):
    pass  # O lexer já está processando os tokens
