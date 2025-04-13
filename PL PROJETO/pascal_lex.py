import ply.lex as lex

tokens = [
    'ID',
    'NUMBER',
    'STRING_LITERAL',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'ASSIGN',
    'EQ', 'NE', 'LT', 'LE', 'GT', 'GE',
    'LPAREN', 'RPAREN',
    'LBRACKET', 'RBRACKET',
    'COLON', 'SEMICOLON', 'COMMA', 'DOT', 'DOTDOT'
]

reserved = {
    'program': 'PROGRAM',
    'var': 'VAR',
    'begin': 'BEGIN',
    'end': 'END',
    'integer': 'INTEGER',
    'real': 'REAL',
    'readln': 'READLN',
    'writeln': 'WRITELN',
    'write': 'WRITE',
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'for': 'FOR',
    'to': 'TO',
    'do': 'DO',
    'while': 'WHILE',
    'div': 'DIV',
    'mod': 'MOD',
    'function': 'FUNCTION',
    'true': 'TRUE',
    'false': 'FALSE',
    'boolean': 'BOOLEAN',
    'array': 'ARRAY',
    'of': 'OF',
    'not': 'NOT',
    'and': 'AND',
    'or': 'OR',
    'string': 'STRING',
    'downto': 'DOWNTO',
}

tokens += list(reserved.values())

t_PLUS       = r'\+'
t_MINUS      = r'-'
t_TIMES      = r'\*'
t_DIVIDE     = r'/'
t_ASSIGN     = r':='
t_EQ         = r'='
t_NE         = r'<>'
t_LT         = r'<'
t_LE         = r'<='
t_GT         = r'>'
t_GE         = r'>='
t_LPAREN     = r'\('
t_RPAREN     = r'\)'
t_LBRACKET   = r'\['
t_RBRACKET   = r'\]'
t_COLON      = r':'
t_SEMICOLON  = r';'
t_COMMA      = r','
t_DOTDOT     = r'\.\.'
t_DOT        = r'\.'

t_ignore  = ' \t'

def t_COMMENT(t):
    r'\{[^}]*\}'
    pass

def t_REAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING_LITERAL(t):
    r'\'([^\\\n]|(\\.))*?\''
    t.value = t.value[1:-1]
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value.lower(), 'ID')
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    raise SyntaxError(f"Caractere ilegal '{t.value[0]}' (linha {t.lineno})")

lexer = lex.lex()


