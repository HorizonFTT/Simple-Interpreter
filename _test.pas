PROGRAM Test;
VAR
   a : INTEGER;
   r : INTEGER;
   s : STRING;

PROCEDURE P1(a:INTEGER; s:STRING);
VAR
   i :INTEGER;
BEGIN
   FOR i := a TO 3 DO
      BEGIN
         WRITELN(s);
      END;
END;

FUNCTION P2(a:INTEGER): INTEGER;
BEGIN
   IF a>1 THEN
      BEGIN
         r := r * a;
         a := a - 1;
         P2 := P2(a);
      END;
   ELSE
      P2 := r
END;

BEGIN {Test}
   a := 1;
   r := 1;
   s := 'Hello World';
   P1(a, s + ' Meow');
   WRITELN('Please enter a number to calculate the factorial:');
   {READLN(a);}
   {WRITELN(P2(a));}
   WRITELN(a);
END.  {Test}
