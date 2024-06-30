### Problemy i wyzwania

## Problem z rozpoznawaniem ścian po wytrenowaniu modelu
Podczas testowania wyuczonego modelu okazało się, że robot ma problem z rozpoznawaniem ścian labiryntu i często nie radzi sobie z unikanie przeszkód. Może to wynikać z kilku czynników:

1. Nieodpowiednie nagrody: Nagrody przyznawane podczas treningu mogą być niewystarczająco motywujące dla robota do unikania przeszkód.
2. Niedostateczna różnorodność danych uczących: Dane używane do treningu mogły nie obejmować wystarczającej liczby scenariuszy, co sprawia, że model nie radzi sobie w nowych sytuacjach.
3. Architektura modelu: Model może wymagać większej liczby warstw lub innych hiperparametrów, aby lepiej uczyć się złożonych zależności.

## Aby poprawić wyniki, należy zwrócić uwagę na:

1. Lepsze definiowanie nagród, aby bardziej penalizować kolizje i nagradzać bezkolizyjne przejazdy.
2. Generowanie bardziej różnorodnych danych uczących, które obejmują różne scenariusze.
3. Eksperymentowanie z architekturą modelu, aby znaleźć optymalną konfigurację.