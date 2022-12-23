program SavaitgaliuSkaicius;

{$mode objfpc}

uses
  SysUtils;

type
  TMetai = 1583..3000;

var
  ivestis: string;
  metai: integer;
  baigiama: boolean = False;

  function arMetaiKeliamieji(metai: TMetai): boolean; { ar TMetai keliamieji }
  begin
    Result := (metai mod 400 = 0) or (metai mod 100 <> 0) and (metai mod 4 = 0);
  end;

  function savaitesDienuMetuose(metai: TMetai): integer;
    { nustatoma, kuria savaites diena prasideda TMetai }
    { savaites dienos numeruojamos: 1 - pirmadienis .. 7 - sekmadienis }
  var
    m: TMetai;
    d: integer;
    i: integer;
  begin
    m := 1978;
    d := 7;
    for i := m - 1 downto metai do { jei duoti TMetai ankstesni }
      if arMetaiKeliamieji(i) then
        d := ((d - 2) + 7) mod 7
      else
        d := ((d - 1) + 7) mod 7;
    if d = 0 then
      d := 7;
    Result := d;
  end;

  function savaitgaliuSkaiciusMetuose(m: TMetai): integer;
  var
    savaitgalioDienu: integer; { sestadieniu ir sekmadieniu skaicius }
  begin
    case savaitesDienuMetuose(m) of
      1..4: savaitgalioDienu := 104;
      5, 7: savaitgalioDienu := 105;
      6: if arMetaiKeliamieji(m) then
          savaitgalioDienu := 106
        else
          savaitgalioDienu := 105;
      otherwise
        savaitgalioDienu := 0;
    end;
    Result := savaitgalioDienu;
  end;

begin
  while not baigiama do
  begin
    Write('Iveskite metus: ');
    ReadLn(ivestis);
    if ivestis = '' then
    begin
      baigiama := True;
      Continue;
    end;

    try
      begin
        metai := StrToInt(ivestis);
      end;
    except
      on E: EConvertError do
      begin
        WriteLn('Ivesta neteisinga reiksme');
        WriteLn(E.Message);
        WriteLn;
        Continue;
      end;
    end;

    WriteLn('Savaitgalio dienu: ', savaitgaliuSkaiciusMetuose(metai));
    WriteLn();
  end;
end.
