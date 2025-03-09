Objetivo
Este projeto tem como objetivo construir um analisador léxico para uma linguagem de query. A principal função do analisador é processar as consultas e separar a entrada em tokens, que representam os componentes da linguagem.

Como Funciona
O analisador léxico processa uma consulta, separando-a em componentes classificados como tokens, cada um representando uma parte distinta da consulta, como:
- Palavras-chave: select, where, limit, etc.
- Variáveis: como ?nome, ?desc.
- Identificadores: como dbo:MusicalArtist, foaf:name.
- Strings: valores como "Chuck Berry"@en.

Processo de Tokenização
O código usa expressões regulares para identificar cada tipo de token. Durante o processo de análise, ele:
- Ignora comentários e espaços em branco.
- Identifica palavras-chave e classifica-as adequadamente.
- Reconhece variáveis e identificadores.
- Trata strings entre aspas, considerando também a linguagem de codificação (por exemplo, "Chuck Berry"@en).