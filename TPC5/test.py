import json
import os

STOCK_FILE = "stock.json"

# Caminho absoluto para garantir que o ficheiro está onde o Python está a procurar
print("Caminho esperado:", os.path.abspath(STOCK_FILE))

# Verifica se o ficheiro existe
if not os.path.exists(STOCK_FILE):
    print("ERRO: Ficheiro não encontrado!")
    exit()

# Testa a leitura do ficheiro JSON
try:
    with open(STOCK_FILE, "r", encoding="utf-8") as f:
        stock = json.load(f)
    print("✅ JSON carregado com sucesso!")
    print(json.dumps(stock, indent=4, ensure_ascii=False))  # Mostra o conteúdo formatado
except json.JSONDecodeError:
    print("❌ ERRO: O ficheiro JSON está corrompido ou mal formatado!")
