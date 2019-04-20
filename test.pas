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

PROCEDURE P2(a:INTEGER);
BEGIN
   IF a>1 THEN
      BEGIN
         r := r * a;
         a := a - 1;
         P2(a);
      END;
   ELSE
      WRITELN(r);
END;

BEGIN {Test}
   a := 1;
   r := 1;
   s := 'Hello World';
   P1(a, s + ' Meow');
   WRITELN('Please enter a number to calculate the factorial:');
   READLN(a);
   P2(a);
   WRITELN(a);
END.  {Test}
