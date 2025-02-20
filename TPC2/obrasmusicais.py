import re

def ler_dataset(nome_arquivo):
    with open(nome_arquivo, 'r', encoding='utf-8-sig') as f:
        conteudo = f.read()

    linhas_raw = re.findall(r'(?:".*?"|[^\n])+', conteudo, re.DOTALL)
    linhas = []

    for linha in linhas_raw:
        linha_limpa = ' '.join(linha.strip().splitlines())
        linhas.append(linha_limpa)

    header = linhas[0].strip().split(';') 
    dados = [linha.strip().split(';') for linha in linhas[1:] if linha.strip()]
    return header, dados

def validar_linha(linha):
    if len(linha) != 7:  
        return False
    
    titulo = linha[0].strip()
    periodo = linha[3].strip()
    compositor = linha[4].strip()

    if not re.match("^[A-Za-záéíóúãõçÁÉÍÓÚÀà\s]+$", periodo):
        return False

    if not re.match("^[A-Za-záéíóúãõçÁÉÍÓÚÀà\s,]+$", compositor):
        return False
    
    return True

def processar_dados(dados):
    compositores = set()
    distribuicao_periodo = {}
    obras_por_periodo = {}
    linhas_ignoradas = 0
    linhas_ignoradas_detalhes = []

    dados_filtrados = []
    for linha in dados:
        if not validar_linha(linha):
            linhas_ignoradas += 1
            linhas_ignoradas_detalhes.append(linha)
        else:
            dados_filtrados.append(linha)

    for linha in dados_filtrados:
        titulo = linha[0].strip()         # Nome da obra
        periodo = linha[3].strip()        # Período
        compositor = linha[4].strip()     # Compositor

        compositores.update([nome.strip() for nome in compositor.split(',')])

        # Contagem de obras por período
        distribuicao_periodo[periodo] = distribuicao_periodo.get(periodo, 0) + 1

        # Lista de títulos por período
        if periodo not in obras_por_periodo:
            obras_por_periodo[periodo] = []
        obras_por_periodo[periodo].append(titulo)

    return sorted(compositores), distribuicao_periodo, {k: sorted(v) for k, v in obras_por_periodo.items()}, linhas_ignoradas, linhas_ignoradas_detalhes


def main():
    nome_arquivo = 'obras.csv'
    header, dados = ler_dataset(nome_arquivo)
    compositores, distribuicao, obras_periodo, linhas_ignoradas, linhas_ignoradas_detalhes = processar_dados(dados)

    print("Lista ordenada de compositores: ")
    for compositor in compositores:
        print(f"- {compositor}")

    print("\nDistribuição das obras por período: ")
    for periodo, quantidade in distribuicao.items():
        print(f"{periodo}: {quantidade} obras")

    print("\nObras organizadas por período: ")
    for periodo, obras in obras_periodo.items():
        print(f"{periodo}:")
        for obra in obras:
            print(f"  - {obra}")

    if linhas_ignoradas > 0:
        print(f"\nAviso: {linhas_ignoradas} linha(s) foram ignoradas por estarem mal formatadas.")
        #print("\nLinhas ignoradas: ")
        #for linha in linhas_ignoradas_detalhes:
        #    print(f"- {linha}")

if __name__ == "__main__":
    main()
