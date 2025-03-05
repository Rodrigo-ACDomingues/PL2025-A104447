import re

def markdown_para_html(markdown):
    html = []

    linhas = markdown.split('\n')
    dentro_lista = False

    for linha in linhas:
        if linha.startswith('# '):
            html.append(f'<h1>{linha[2:].strip()}</h1>')
        elif linha.startswith('## '):
            html.append(f'<h2>{linha[3:].strip()}</h2>')
        elif linha.startswith('### '):
            html.append(f'<h3>{linha[4:].strip()}</h3>')

        # Lista
        elif re.match(r'\d+\.', linha.strip()):
            if not dentro_lista:
                html.append('<ol>')
                dentro_lista = True
            item = re.sub(r'\d+\.\s*', '', linha)
            html.append(f'<li>{item.strip()}</li>')
        else:
            if dentro_lista:
                html.append('</ol>')
                dentro_lista = False

            # Bold
            linha = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', linha)

            # Itálico
            linha = re.sub(r'\*(.*?)\*', r'<i>\1</i>', linha)

            # Imagem
            linha = re.sub(r'!\[(.*?)\]\((.*?)\)', r'<img src="\2" alt="\1"/>', linha)

            # Link
            linha = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', linha)

            html.append(linha)

    if dentro_lista:
        html.append('</ol>')

    return '\n'.join(html)

markdown_texto = """
# Exemplo

Este é um **exemplo** de texto com *itálico* e [link](http://www.exemplo.com).

1. Primeiro item
2. Segundo item
3. Terceiro item

Veja esta imagem: ![Coelho](http://www.coelho.com)
"""

html = markdown_para_html(markdown_texto)
print(html)
