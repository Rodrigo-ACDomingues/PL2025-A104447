program SomaArray;
function Soma(v: array[1..5] of integer): integer;
var
i, total: integer;
begin
total := 0;
for i := 1 to 5 do
total := total + v[i];
Soma := total;
end;
var
numeros: array[1..5] of integer;
i, resultado: integer;
begin
writeln('Introduza 5 números:');
for i := 1 to 5 do
readln(numeros[i]);
resultado := Soma(numeros);
writeln('Soma = ', resultado);
end.