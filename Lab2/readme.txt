Bildmatchning
=============

- Ungefärligt antal timmar spenderade på labben (valfritt):


- Vad är tidskomplexiteten på "slow.cpp" och din implementation av "fast.cpp",
  uttryckt i antalet bilder (n).

slow: n²
fast: n


- Hur lång tid tar det att köra "slow.cpp" respektive "fast.cpp" på de olika
  datamängderna?
  Tips: Använd flaggan "--nowindow" för enklare tidsmätning.
  Tips: Det är okej att uppskatta tidsåtgången för de fall du inte orkar vänta
  på att de blir klara.
  Tips: Vid uppskattning av körtid för "slow.cpp" är det en bra idé att beräkna
  tiden det tar att läsa in (och skala ner) bilderna separat från tiden det tar att
  jämföra bilderna. (Varför?)

|--------+-----------+----------+----------|
|        | inläsning | slow.cpp | fast.cpp |
|--------+-----------+----------+----------|
| tiny   |  72-232   |   49     |    41    |
| small  |  534-541  |   114    |    118   |
| medium | 2121-2149 |   563    |    109   |
| large  |52541-55528| 555384   |    126   |
|--------+-----------+----------+----------|


- Testa olika värden på "summary_size" (exempelvis mellan 6 och 10). Hur
  påverkar detta vilka dubbletter som hittas i datamängden "large"?
  8: 18st ny 16st match 8
  6: 18st ny 18st match 9
  10: 10st ny 10st match 5


- Algoritmen som implementeras i "compute_summary" kan ses som att vi beräknar
  en hash av en bild. Det är dock inte helt lätt att hitta en bra sådan funktion
  som helt motsvarar vad vi egentligen är ute efter. Vilken eller vilka
  egenskaper behöver "compute_summary" ha för att vi ska kunna lösa problemet i
  labben? Tycker du att den givna funktionen uppfyller dessa egenskaper?

  Det blir en avvägning mellan hur detaljerad man är i sammanfattningen och tidskomplexiteten för funktionen.
  Vi vill idealt ta fram en funktion som är så snabb som möjligt men som även kan identifiera så många dubletter som möjligt.
  Vi tycker den giva fungerar tillräckligt bra för denna labb, den har bra tidskomplexitet och vi kan välja hur nogranna vi vill vara
  när vi tar fram image_summary. 
  Egenskaper som comupute summary behöver ha är unikhet alltså att den bör generera en unik "hash" för varje unik bild
  och konsistens alltså att samma bild bör alltid resultera i samma sammanfattning. Den bör också vara snabb nog att hantera stora mängder bilder.
  Det bör också finnas en balans för hur känslig den är mellan två nästan identiska bilder.



- Ser du några problem med metoden för att se om två bilder är lika dana?
  Föreslå en alternativ metod för att hitta bilder som är lika. Vad har
  ditt/dina förslag för för- och nackdelar jämfört med det som föreslås i
  labben? Fokusera exempelvis på vilka typer av skillnader i bilder som
  hanteras, eller vilken tidskomplexitet som kan uppnås. Ditt förslag behöver
  inte vara snabbare än det som föreslås i labben, men du ska komma på
  åtminstone en fördel med din metod.

  Ja vi använder brightness från pixel.h som bara tar medelvärdet av R G och B så vi riskerar att
  hitta dubletter där färgerna är olika men värdet för brightness är samma.
  För att komma runt detta måste vi titta på R G och B separat.
  Istället för att använda brightness kan vi skapa en struct med R G och B variabler som bools och använda i horisontal och vertical vectorn
  istället för bara en bool för brightness. 
  Detta kommer använda mer minne och utföra fler instruktioner men tidskomplexiteten borde fortförande vara O(n).
  Det kommer förmodligen att vara lite långsammare att kolla på rgb separat än att kolla brightness men det kan
  vara värt det om man inte vill att programmet är färgblint. 