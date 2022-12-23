program Dalikliai;

  function rastiSkaiciuSuDaugiausiaDalikliuIntervale(skaiciusNuo,
    skaiciusIki: integer): integer;
    { randamas maziausias intervalo [m, n] skaicius }
    { turintis daugiausia daliksliu; m, n - naturalieji skaiciai }
  var
    tiriamojoDalikliu: integer; { kiek dalikliu turi tiriamasis skaicius }
    maksimaliaiDalikliu: integer; { ieskomas maksimalus dalikliu skaicius }
    skaiciusSuDaugiausiaDalikliu: integer;
    { ieskomas daugiausia dalikliu turintis skaicius }
    i: integer; { intervalo skaiciai }

    function gautiDalikliuSkaiciu(skaicius: integer): integer;
      { kiek dalikliu turi skaicius k }
    var
      daliklis: integer; { daliklis }
      dalikliuSkaicius: integer; { dalikliu skaicius }

    begin
      dalikliuSkaicius := 0;
      daliklis := 1;
      while daliklis * daliklis < skaicius do
      begin
        if skaicius mod daliklis = 0 then dalikliuSkaicius := dalikliuSkaicius + 2;
        { yra du dalikliai: daliklis ir skaicius div daliklis }
        daliklis := daliklis + 1;
      end;
      if daliklis * daliklis = skaicius then dalikliuSkaicius := dalikliuSkaicius + 1;
      { dar prisides vienas daliklis }
      Result := dalikliuSkaicius;
    end;

  begin { daugiausia }
    maksimaliaiDalikliu := gautiDalikliuSkaiciu(skaiciusNuo);
    skaiciusSuDaugiausiaDalikliu := skaiciusNuo;
    for i := skaiciusNuo + 1 to skaiciusIki do { perziurimas visas intervalas }
    begin
      tiriamojoDalikliu := gautiDalikliuSkaiciu(i);
      if tiriamojoDalikliu > maksimaliaiDalikliu then
        { jei parasytume >=, rastume didziausia intervalo skaiciu turinti daugiausia dalikliu }
      begin
        maksimaliaiDalikliu := tiriamojoDalikliu;
        skaiciusSuDaugiausiaDalikliu := i;
      end;
    end;
    Result := skaiciusSuDaugiausiaDalikliu;
  end;

begin
  WriteLn(rastiSkaiciuSuDaugiausiaDalikliuIntervale(14, 14));
  WriteLn(rastiSkaiciuSuDaugiausiaDalikliuIntervale(1, 1));
  WriteLn(rastiSkaiciuSuDaugiausiaDalikliuIntervale(2, 8));
  WriteLn(rastiSkaiciuSuDaugiausiaDalikliuIntervale(4, 12));
  WriteLn(rastiSkaiciuSuDaugiausiaDalikliuIntervale(13, 17));
  WriteLn(rastiSkaiciuSuDaugiausiaDalikliuIntervale(10, 1999));
  ReadLn;
end.
