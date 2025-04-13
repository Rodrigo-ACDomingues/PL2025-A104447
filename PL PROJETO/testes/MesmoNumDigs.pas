program MesmoNumeroDigitos;
function NumDigitos(n: integer): integer;
var
cont: integer;
begin
cont := 0;
while n <> 0 do
begin
cont := cont + 1;
n := n div 10;
end;
NumDigitos := cont;
end;
var
a, b: integer;
begin
readln(a);
readln(b);
if NumDigitos(a) = NumDigitos(b) then
writeln('Têm o mesmo número de dígitos.')
else
writeln('Têm número de dígitos diferente.');
end.