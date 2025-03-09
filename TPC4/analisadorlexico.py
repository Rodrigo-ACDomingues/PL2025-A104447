import ply.lex as lex

tokens = (
    'SELECT', 'WHERE', 'LIMIT',
    'VAR', 'LITERAL', 'NUMBER',
    'PREFIX', 'DOT', 'BRACE_OPEN', 'BRACE_CLOSE',
    'RDF_TYPE'
)

reserved = {
    'select': 'SELECT',
    'where': 'WHERE',
    'LIMIT': 'LIMIT',
    'a': 'RDF_TYPE'
}

def t_RESERVED(t):
    r'select|where|LIMIT|a'
    t.type = reserved.get(t.value, 'PREFIX')  # Se não for reservada, trata como PREFIX
    return t

def t_VAR(t):
    r'\?[a-zA-Z_]\w*'
    return t

def t_LITERAL(t):
    r'\"[^\"]*\"(@[a-zA-Z]+)?'
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_PREFIX(t):
    r'[a-zA-Z_]+:[a-zA-Z_]\w*'
    return t

t_DOT = r'\.'
t_BRACE_OPEN = r'\{'
t_BRACE_CLOSE = r'\}'

t_ignore = ' \t\n'

def t_error(t):
    print(f'Caractere inválido: {t.value[0]}')
    t.lexer.skip(1)

lexer = lex.lex()

data = '''select ?nome ?desc where {
?s a dbo:MusicalArtist.
?s foaf:name "Chuck Berry"@en .
?w dbo:artist ?s.
?w foaf:name ?nome.
?w dbo:abstract ?desc
} LIMIT 1000'''

lexer.input(data)

for tok in lexer:
    print(tok)
