from pascal_lex import lexer 
from pascal_yacc import parser

print("Insere o código Pascal abaixo (termina com linha vazia):\n")

linhas = []
while True:
    try:
        linha = input()
        if linha.strip() == "":
            break
        linhas.append(linha)
    except EOFError:
        break

codigo = "\n".join(linhas)

lexer.input(codigo)

#print("\nTokens encontrados:")
#for token in lexer:
#    print(token)

print("-----------------Analise_Sintatica-----------------")
#parser.parse(codigo, debug = True)
yacc = parser.parse(codigo)
print(yacc)


