import ply.yacc as yacc
from pascal_lex import tokens

# Precedência dos operadores
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQ', 'NE', 'LT', 'LE', 'GT', 'GE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'DIV', 'MOD'),
    ('right', 'NOT', 'UMINUS'),
)

# Programa principal
def p_program(p):
    'program : PROGRAM ID SEMICOLON declarations block DOT'
    print("Programa válido")
    p[0] = ('program', p[2], p[4], p[5])

# Declarações de variáveis
def p_declarations(p):
    '''declarations : declaration_list
                    | empty'''
    p[0] = p[1] if p[1] else []

def p_declaration_list(p):
    '''declaration_list : declaration
                        | declaration_list declaration'''
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[2]]

def p_declaration(p):
    '''declaration : VAR var_decl_list
                   | function_decl'''
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = [p[1]]

def p_function_decl_list(p):
    '''function_decl_list : function_decl
                          | function_decl_list function_decl'''
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[2]]

def p_function_decl(p):
    'function_decl : FUNCTION ID LPAREN param_list RPAREN COLON base_type SEMICOLON declarations block SEMICOLON'
    p[0] = ('function', p[2], p[4], p[7], p[9], p[10])

def p_param_list(p):
    '''param_list : param
                  | param_list SEMICOLON param'''
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[3]]

def p_param(p):
    'param : id_list COLON type'
    p[0] = ('param', p[1], p[3])

def p_var_decl_list(p):
    '''var_decl_list : var_decl_list var_decl 
                     | var_decl'''
    p[0] = p[1] + [p[2]] if len(p) == 3 else [p[1]]

def p_var_decl(p):
    'var_decl : id_list COLON type SEMICOLON'
    p[0] = ('var_decl', p[1], p[3])

def p_id_list(p):
    '''id_list : ID
               | id_list COMMA ID'''
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[3]]

def p_type(p):
    '''type : base_type
            | array_type'''
    p[0] = p[1]

def p_array_type(p):
    'array_type : ARRAY LBRACKET NUMBER DOTDOT NUMBER RBRACKET OF base_type'
    p[0] = ('array', p[3], p[5], p[8])

def p_base_type(p):
    '''base_type : INTEGER
                 | BOOLEAN
                 | STRING
                 | REAL'''
    p[0] = p[1]

# Bloco BEGIN ... END
def p_block(p):
    'block : BEGIN statement_list END'
    p[0] = ('block', p[2])

def p_statement_list(p):
    '''statement_list : statement
                      | statement_list SEMICOLON statement'''
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[3]]

# Tipos de instruções
def p_statement(p):
    '''statement : assignment
                 | if_statement
                 | while_statement
                 | for_statement
                 | write_statement
                 | read_statement
                 | block
                 | empty'''
    p[0] = p[1]

def p_assignment(p):
    'assignment : ID ASSIGN expression'
    p[0] = ('assign', p[1], p[3])

def p_if_statement(p):
    '''if_statement : IF expression THEN statement 
                    | IF expression THEN statement ELSE statement'''
    p[0] = ('if', p[2], p[4], p[6]) if len(p) == 7 else ('if', p[2], p[4], None)

def p_while_statement(p):
    'while_statement : WHILE expression DO statement'
    p[0] = ('while', p[2], p[4])

def p_for_statement(p):
    '''for_statement : FOR ID ASSIGN expression TO expression DO statement
                     | FOR ID ASSIGN expression DOWNTO expression DO statement'''
    if p[5].lower() == 'to':
        p[0] = ('for', p[2], p[4], p[6], p[8], 'to')
    else:
        p[0] = ('for', p[2], p[4], p[6], p[8], 'downto')

def p_write_statement(p):
    '''write_statement : WRITE LPAREN write_args RPAREN
                       | WRITELN LPAREN write_args RPAREN'''
    p[0] = ('write', 'writeln' if p[1].lower() == 'writeln' else 'write', p[3])

def p_write_args(p):
    '''write_args : expression
                  | write_args COMMA expression'''
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[3]]

def p_read_statement(p):
    'read_statement : READLN LPAREN expression RPAREN'
    p[0] = ('read', p[3])

# Expressões
def p_expression(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression DIV expression
                  | expression MOD expression
                  | expression EQ expression
                  | expression NE expression
                  | expression LT expression
                  | expression LE expression
                  | expression GT expression
                  | expression GE expression
                  | expression AND expression
                  | expression OR expression'''
    p[0] = (p[2].lower(), p[1], p[3])

def p_expression_not(p):
    'expression : NOT expression'
    p[0] = ('not', p[2])

def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = ('neg', p[2])

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = ('num', p[1])

def p_expression_string(p):
    'expression : STRING_LITERAL'
    p[0] = ('str', p[1])

def p_expression_boolean(p):
    '''expression : TRUE
                  | FALSE'''
    p[0] = ('bool', p[1].lower() == 'true')

def p_expression_id(p):
    'expression : ID'
    p[0] = ('var', p[1])

def p_expression_array_access(p):
    'expression : ID LBRACKET expression RBRACKET'
    p[0] = ('array_access', p[1], p[3])

def p_expression_function_call(p):
    'expression : ID LPAREN expression_list RPAREN'
    p[0] = ('call', p[1], p[3])

def p_expression_list(p):
    '''expression_list : expression
                       | expression_list COMMA expression'''
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[3]]

# Vazio
def p_empty(p):
    'empty :'
    p[0] = None

# Erros
def p_error(p):
    if p:
        print(f"Erro de sintaxe perto de '{p.value}' (linha {p.lineno})")
    else:
        print("Erro de sintaxe: fim de ficheiro inesperado")

# Criar parser
parser = yacc.yacc()
