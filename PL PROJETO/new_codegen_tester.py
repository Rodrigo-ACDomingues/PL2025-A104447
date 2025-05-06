import os
from pascal_lex import lexer
from pascal_yacc import parser
from new_codegen import GeradorVM
import traceback

def correr_codigo_vm(ficheiro_pas):
    caminho = os.path.join("testes", ficheiro_pas)
    with open(caminho, "r", encoding="utf-8") as f:
        codigo = f.read()

    try:
        lexer.lineno = 1
        ast = parser.parse(codigo, lexer=lexer)

        # Instancia e gera o código VM
        gerador = GeradorVM()
        codigo_vm = gerador.gerar(ast)

        # Guarda o código gerado no ficheiro .vm
        nome_base = os.path.splitext(ficheiro_pas)[0]
        os.makedirs("codigoVM", exist_ok=True)
        with open(os.path.join("codigoVM", f"{nome_base}.vm"), "w", encoding="utf-8") as out:
            out.write("\n".join(codigo_vm))

        print(f"[✔] Código VM gerado para {ficheiro_pas}, verifique na pasta 'codigoVM'.")
    except Exception as e:
        print(f"[✘] Erro ao gerar código para {ficheiro_pas} → {e}")
        traceback.print_exc()

# Testa todos os ficheiros .pas na pasta "testes"
for ficheiro in os.listdir("testes"):
    if ficheiro.endswith(".pas") and not ficheiro.startswith("Erro"):
        correr_codigo_vm(ficheiro)
