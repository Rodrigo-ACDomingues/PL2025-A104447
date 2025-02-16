import sys

def somador_on_off(texto):
    soma = 0
    acumulador = 0
    ligado = True
    numero_atual = ''
    i = 0
    
    while i < len(texto):
        char = texto[i]
        
        if char.isdigit():
            numero_atual += char
        else:
            if numero_atual:
                if ligado:
                    acumulador += int(numero_atual)
                numero_atual = ''
            
            if char == '=':
                print(acumulador)
            
        if texto[i:i+3].lower() == 'off':
            ligado = False
            i += 2
        elif texto[i:i+2].lower() == 'on':
            ligado = True
            i += 1
        
        i += 1
    
    if numero_atual and ligado:
        acumulador += int(numero_atual)
    
    print(f">> {acumulador}")

if __name__ == "__main__":

    entrada_teste = """Hoje, 7 de Fevereiro de 2025, o professor de Processamento de Linguagens
deu-nos
este trabalho para fazer.=OfF
E deu-nos 7= dias para o fazer... ON
Cada trabalho destes vale 0.25 valores da nota final!"""
    
    from io import StringIO
    import sys
    
    sys.stdin = StringIO(entrada_teste)  # Simula entrada pelo terminal
    somador_on_off(sys.stdin.read())  # Executa o programa

