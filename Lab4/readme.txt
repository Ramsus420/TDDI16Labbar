Mönsterigenkänning
==================

- Ungefärligt antal timmar spenderade på labben (valfritt):


- Vad är tidskomplexiteten (i ordo-notation) för värstafallstiden av
  programmen som en funktion av N (antal punkter). Ge en kort motivering.

  Matchar brute-lösningen sitt värstafall i praktiken, eller har den ett
  medelfall som är bättre?

brute: värsta O(N⁴) om många linjer
      Medel: också O(N⁴) men något snabbare eftersom den ibland kan skippa en loop om den inte hittar linjer.

fast: O(N²logn) för alla


- Fyll i tabellen nedan med riktiga körtider i sekunder när det känns
  vettigt att vänta på hela beräkningen.
  Ge uppskattningar av körtiden (baserat på tidskomplexiteten)
  i övriga fall.
    
      N       brute       sortering
 ----------------------------------
    150       0,042       0,014
    200       0,100       0,032
    300       0,300       0,069
    400       0,701       0,109
    800       5,616       0,377
   1600       46,307      1,590
   3200       383,728     6,712
   6400       6139,648    28,807
  12800       98234,368   128,142


- Energianvändning

  Antag att du använder mönsterigenkänningsprogrammet för att analysera
  data från en kamera. Kameran sitter i en byggnad och tar en bild
  på stommen av byggnaden var 30:e minut. Bilden förbehandlas sedan
  lite, innan punkter som representerar stommen skickas till
  mönsterigenkänningsprogrammet. Hittas inte tillräckligt många raka
  linjer så betyder det att något håller på att gå sönder, och
  att byggnaden behöver noggrannare inspektion.

  Hur mycket energi sparar du på ett år om du använder din snabbare
  sorteringslösning i stället för brute-lösningen? Du kan anta följande:
  - Systemet körs 24/7 under hela året.
  - Inget annat körs på det här systemet.
  - Systemet drar 8 W när det inte gör något (idle)
  - Systemet drar 36 W när det arbetar (med 1 kärna)
  - Räkna med att ditt program körs var 30:e minut (= 2 gånger/timme)
  - För- och efterbehandling är snabba, så vi kan bortse från dem
  - Indata till programmet innehåller ca 6400 punkter
  - Det är inte skottår (= 365 dagar)

  Att jämföra med drar en kombinerad kyl/frys ca 200 kWh per år
  (enligt Energimyndigheten).
 
  Kom ihåg: energi mäts ofta i kWh, vilket är:
   energi (kWh) = effekt (kW) * tid (h)

  Tips: ett sätt att räkna på är att först räkna förbrukningen av
  ett system som inte gör något på ett helt år, sedan lägga till
  den extra förbrukningen (36 W - 8 W = 28 W) för tiden som systemet
  är aktiv.

  (Siffrorna är löst baserade på en Intel i9-9900K, vi räknar bara på
  CPU:n för enkelhets skull, besparingarna blir sannolikt större om
  vi räknar på större delar av systemet, även om andra komponenter
  också drar ström i "idle".)


BERÄKNINGAR SE CALC.PY

Förbrukning av brute på ett år: 668 kWh

Förbrukning av sotering på ett år: 73 kWh

Skillnad: 595 kWh