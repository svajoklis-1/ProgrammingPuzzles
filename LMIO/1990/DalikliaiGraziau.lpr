program DalikliaiGraziau;

const
  MAX = 2000; { intervalo didziauskas rezis }

type
  dal = array [1..MAX] of integer; { dalikliams kaupti }

  function daug_dalikliu(m, n: integer): integer;
  var
    skaiciausDalikliu: dal; { kiek skaicius turi dalikliu }
    didziausiasDalikliuSkaicius: integer; { maksimalus dalikliu skaicius }
    kartotinis: integer; { skaiciu 2, 3, 4, ...kartotiniai }
    tiriamasSkaicius: integer; { tiriamas intervalo skaicius }
    skaiciusSuDaugiausiaDalikliu: integer;
  begin
    skaiciausDalikliu[1] := 1;

    for tiriamasSkaicius := 2 to n do { visi skaiciai dalus is }
      skaiciausDalikliu[tiriamasSkaicius] := 2; { vieneto ir saves }

    for tiriamasSkaicius := 2 to n div 2 do
    begin
      kartotinis := tiriamasSkaicius + tiriamasSkaicius;
      while kartotinis <= n do
      begin
        skaiciausDalikliu[kartotinis] := skaiciausDalikliu[kartotinis] + 1;
        kartotinis := kartotinis + tiriamasSkaicius;
      end;
    end; { dalikliai surasti: masyvas skaiciausDalikliu uzpildytas }

    { randamas dalikliu maksimumas }
    didziausiasDalikliuSkaicius := skaiciausDalikliu[m];
    skaiciusSuDaugiausiaDalikliu := m;
    for tiriamasSkaicius := m + 1 to n do
      if skaiciausDalikliu[tiriamasSkaicius] > didziausiasDalikliuSkaicius then
      begin
        didziausiasDalikliuSkaicius := skaiciausDalikliu[tiriamasSkaicius];
        skaiciusSuDaugiausiaDalikliu := tiriamasSkaicius;
      end;
    Result := skaiciusSuDaugiausiaDalikliu;
  end;

begin
  WriteLn(daug_dalikliu(14, 14));
  WriteLn(daug_dalikliu(1, 1));
  WriteLn(daug_dalikliu(2, 8));
  WriteLn(daug_dalikliu(4, 12));
  WriteLn(daug_dalikliu(13, 17));
  WriteLn(daug_dalikliu(10, 1999));
  ReadLn;
end.
