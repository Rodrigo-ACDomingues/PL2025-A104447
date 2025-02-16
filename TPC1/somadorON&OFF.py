def somador_on_off():
    soma = 0
    ligado = True
    
    while True:
        try:
            linha = input().strip()
            if not linha:
                break
            
            numero_atual = ''
            i = 0
            while i < len(linha):
                char = linha[i]
                
                if char.isdigit():
                    numero_atual += char
                else:
                    if numero_atual:
                        if ligado:
                            soma += int(numero_atual)
                        numero_atual = ''
                    
                    if char == '=':
                        print(f">> {soma}")
                    
                if linha[i:i+3].lower() == 'off':
                    ligado = False
                    i += 2
                elif linha[i:i+2].lower() == 'on':
                    ligado = True
                    i += 1
                
                i += 1
            
            if numero_atual and ligado:
                soma += int(numero_atual)
        except EOFError:
            break
    
    print(f">> {soma}")
    
# Executa o programa
somador_on_off()