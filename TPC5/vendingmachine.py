import json
import os
import re

STOCK_FILE = "TPC5/stock.json"

def carregar_stock():
    if not os.path.exists(STOCK_FILE):
        return []
    try:
        with open(STOCK_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Erro ao carregar JSON!")
        return []

def guardar_stock(stock):
    with open(STOCK_FILE, "w", encoding="utf-8") as f:
        json.dump(stock, f, indent=4, ensure_ascii=False)

def listar_produtos(stock):
    print("\ncod  | nome                 | quantidade | preço")
    print("-------------------------------------------------")
    for produto in stock:
        print(f"{produto['cod']:4} | {produto['nome'][:20]:20} | {produto['quant']:9} | {produto['preco']:.2f}")

def processar_comando(comando, stock, saldo):
    comando = comando.strip().upper()

    if comando == "LISTAR":
        listar_produtos(stock)

    elif comando.startswith("MOEDA "):
        moedas = re.findall(r'(\d+)([EC])', comando)
        for valor, tipo in moedas:
            valor = int(valor)
            saldo += valor * 100 if tipo == "E" else valor  # 1E = 100C
        print(f"Saldo: {saldo}c")

    elif comando.startswith("SELECIONAR "):
        codigo = comando.split()[1]
        produto = next((p for p in stock if p["cod"] == codigo), None)
        
        if not produto:
            print("Produto não encontrado!")
            return saldo
        
        if produto["quant"] == 0:
            print("Produto esgotado!")
            return saldo
        
        if saldo < produto["preco"] * 100:
            print(f"Saldo insuficiente! Saldo: {saldo}c | Pedido: {int(produto['preco'] * 100)}c")
            return saldo
        
        saldo -= int(produto["preco"] * 100)
        produto["quant"] -= 1
        print(f"Pode retirar o produto: {produto['nome']}")
        print(f"Saldo restante: {saldo}c")
        guardar_stock(stock)

    elif comando == "SAIR":
        if saldo > 0:
            troco = calcular_troco(saldo)
            print(f"Pode retirar o troco: {troco}")
        print("Até à próxima!")
        exit()
    
    else:
        print("Comando inválido!")

    return saldo

def calcular_troco(saldo):
    moedas = [50, 20, 10, 5, 2, 1]
    troco = []
    for moeda in moedas:
        while saldo >= moeda:
            saldo -= moeda
            troco.append(f"1x {moeda}c")
    return ", ".join(troco)

def main():
    stock = carregar_stock()
    saldo = 0
    print("Máquina ligada. Escreva 'LISTAR' para ver os produtos ou 'SAIR' para sair.")

    while True:
        comando = input(">> ")
        saldo = processar_comando(comando, stock, saldo)

if __name__ == "__main__":
    main()
