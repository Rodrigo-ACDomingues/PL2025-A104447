program SomatorioPares;
function SomaPares(n: integer): integer;
var
i, soma: integer;
begin
soma := 0;
i := 0;
while i <= n do
begin
if i mod 2 = 0 then
soma := soma + i;
i := i + 1;
end;
SomaPares := soma;
end;
var
numero, resultado: integer;
begin
readln(numero);
resultado := SomaPares(numero);
writeln('Soma dos pares até ', numero, ': ', resultado);
end.
