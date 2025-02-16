def ler_dataset(nome_arquivo):
    with open(nome_arquivo, 'r', encoding='utf-8') as f:
        linhas = f.readlines()
    
    header = linhas[0].strip().split(';')  # Assume que o separador é ponto e vírgula
    dados = [linha.strip().split(';') for linha in linhas[1:]]
    return header, dados


def processar_dados(dados):
    compositores = set()
    distribuicao_periodo = {}
    obras_por_periodo = {}
    
    for linha in dados:
        compositor, titulo, periodo = linha[0], linha[1], linha[2]
        compositores.add(compositor)
        
        # Contagem de obras por período
        distribuicao_periodo[periodo] = distribuicao_periodo.get(periodo, 0) + 1
        
        # Lista de títulos por período
        if periodo not in obras_por_periodo:
            obras_por_periodo[periodo] = []
        obras_por_periodo[periodo].append(titulo)
    
    return sorted(compositores), distribuicao_periodo, {k: sorted(v) for k, v in obras_por_periodo.items()}


def main():
    nome_arquivo = 'dataset_obras.txt'  # Substitua pelo nome do seu arquivo
    header, dados = ler_dataset(nome_arquivo)
    compositores, distribuicao, obras_periodo = processar_dados(dados)
    
    print("Lista ordenada de compositores:")
    print(compositores)
    
    print("\nDistribuição de obras por período:")
    for periodo, quantidade in distribuicao.items():
        print(f"{periodo}: {quantidade}")
    
    print("\nObras organizadas por período:")
    for periodo, obras in obras_periodo.items():
        print(f"{periodo}: {obras}")


if __name__ == "__main__":
    main()
