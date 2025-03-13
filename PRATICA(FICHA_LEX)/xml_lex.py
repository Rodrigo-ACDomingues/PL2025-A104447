import ply.lex as lex

states = (
    ('tag', 'exclusive'),
)

tokens = (
    'SITA', # <
    'SFT', # >
    'SIFT', # </
    'NOMETAG',
    'VALOR'
)

def t_SIFT (t):
    r'</'
    t.lexer.begin('tag')
    return t

def t_SITA (t):
    r'<'
    t.lexer.begin('tag')
    return t

def t_tag_SFT (t):
    r'>'
    t.lexer.begin('INITIAL')
    return t

def t_tag_NOMETAG (t):
    r'\w+'
    return t

def t_VALOR (t):
    r'\w+'
    return t

t_ANY_ignore = r' '

def t_ANY_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)    

def t_ANY_error(t):
    print(f"Illegal character: {t.value[0]}")
    t.lexer.skip(1)
    
lexer = lex.lex()

data = '''
<pessoa>
    <nome>Maria</nome>
    <idade>32</idade>
</pessoa>
'''

def analyse(phrase):
    lexer.input(phrase)
    tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        
        tokens.append(tok)
    return tokens

toks = analyse(data)

for t in toks:
    print(f"{t.type} : {t.value}")