import ply.lex as lex

# Define tokens as a tuple (not a set)
tokens = (
    'PALAVRA',
    'VIRGULA',
    'SINAL'
)

# Define regular expressions for each token
def t_PALAVRA(t):
    r'\w+'  # Matches any word (letters, numbers, and underscores)
    return t

def t_VIRGULA(t):
    r'\,'  # Matches a comma
    return t

def t_SINAL(t):
    r'[!?.;]'  # Matches any of the symbols !, ?, ., or ;
    return t

# Define a rule for handling illegal characters
def t_error(t):
    print(f"Carácter ilegal {t.value[0]}")
    t.lexer.skip(1)

# Define tokens to be ignored (spaces and tabs)
t_ignore = ' \t'

# Create the lexer
lexer = lex.lex()

# Function to analyze a sentence
def analisar(frase):
    lexer.input(frase)
    tokens_encontrados = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens_encontrados.append((tok.value, tok.type))
    return tokens_encontrados

# Test sentence
frase = "Boaaaaas! pessoooooalllll? daqui.quem fala, é o FEROMONAS"
resultado = analisar(frase)

# Print the results
for token, tipo in resultado:
    print(f"{token}: {tipo}")
