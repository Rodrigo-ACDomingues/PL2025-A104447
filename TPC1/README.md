# Somador on/off: criar um programa em Python (sem usar expressões regulares) que: 
1. Some todas as sequências de dígitos que encontre num texto;
2. Sempre que encontrar a string “Off” em qualquer combinação de maiúsculas e minúsculas, esse
comportamento é desligado;
3. Sempre que encontrar a string “On” em qualquer combinação de maiúsculas e minúsculas, esse
comportamento é novamente ligado;
4. Sempre que encontrar o caráter “=”, o resultado da soma é colocado na saída;
5. No fim, coloca o valor da soma na saída.

Texto enviado para stdout:
Hoje, 7 de Fevereiro de 2025, o professor de Processamento de Linguagens
deu-nos
este trabalho para fazer.=OfF
>> 2032
E deu-nos 7=
>> 2032
dias para o fazer... ON
Cada trabalho destes vale 0.25 valores da nota final!
>> 2057

# Explicação
Este programa em Python lê as entradas do terminal linha por linha e soma os números encontrados, seguindo as regras mencionadas anteriormente. Inicialmente, a soma está ativada e os números identificados são adicionados a uma soma. No entanto, sempre que a string "Off" for encontrada, independentemente de maiúsculas ou minúsculas, a soma é desativada, não permitindo que novos números sejam somados. Da mesma forma, quando a string "On" aparece, a soma é reativada. Além disso, sempre que o caractere "=" for encontrado, o programa imprime o valor atual da soma. O processo continua até que seja inserida uma linha vazia ou EOF (Ctrl+Z). No final, o programa dá print a soma com o seu valor final.