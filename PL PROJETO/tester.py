import os
from pascal_yacc import parser
from pascal_lex import lexer

def correr_teste(path):
    with open(path) as f:
        codigo = f.read()
    try:
        lexer.lineno = 1  # Reiniciar o número da linha
        yacc = parser.parse(codigo, lexer=lexer)
        print(f"[✔] {os.path.basename(path)}")
        #print(yacc)
    except Exception as e:
        print(f"[✘] {os.path.basename(path)} → {e}")

def main():
    pasta = "testes"
    for ficheiro in sorted(os.listdir(pasta)):
        if ficheiro.endswith(".pas"):
            correr_teste(os.path.join(pasta, ficheiro))

if __name__ == "__main__":
    main()
