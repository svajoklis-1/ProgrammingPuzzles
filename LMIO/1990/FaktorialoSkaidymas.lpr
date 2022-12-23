program Pirma;

  function daug(x: integer): integer;
  var
    k: integer; { daugikliu skaicius }
    d: integer; { dalikliai: 3, 5, 7 }
  begin
    k := 0;
    while x mod 2 = 0 do
    begin { x dalijasi is 2 }
      k := k + 1;
      x := x div 2;
    end;
    d := 3;
    while d <= x do
      if x mod d = 0 then { x dalijasi is d }
      begin
        k := k + 1;
        x := x div d;
      end
      else
      begin
        d := d + 2; { imamas kitas nelyginis daliklis }
      end;
    Result := k;
  end;

  function kiek(n: integer): integer;
  var
    k, i: integer;

  begin
    k := 0;
    for i := 1 to n do { n! = 1 * 2 * 3 * ... * n }
      k := k + daug(i);
    Result := k;
  end;

begin
  WriteLn('1: kiek(1) = ', kiek(1));
  WriteLn('2: kiek(6) = ', kiek(6));
  WriteLn('3: kiek(11) = ', kiek(11));
  WriteLn('4: kiek(18) = ', kiek(18));
  WriteLn('5: kiek(25) = ', kiek(25));
  WriteLn('6: kiek(28) = ', kiek(28));
  ReadLn;
end.
