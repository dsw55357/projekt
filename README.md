# Pracowaliśmy nad stworzeniem systemu sterowania robotem w labiryncie, wykorzystując model TensorFlow. Proces ten można podzielić na kilka kluczowych etapów:

## Generowanie danych uczących:

1. Robot porusza się po labiryncie według prostego heurystycznego algorytmu, który wykorzystuje sensory do wykrywania przeszkód i nawigowania wzdłuż ścian.
2. W trakcie ruchu robota zapisywane są dane o jego stanie (pozycja, kąt) oraz akcje podejmowane przez algorytm nawigacji (np. ruch do przodu lub obrót).
3. Te dane są zapisywane do pliku JSON w formacie, który umożliwia późniejsze ich odczytanie i wykorzystanie do treningu modelu.

## Proces uczenia modelu:

1. Dane uczące są odczytywane z pliku JSON i wykorzystywane do trenowania modelu DQN (Deep Q-Network).
Model jest trenowany na podstawie zapisanych stanów, akcji, nagród, kolejnych stanów oraz informacji, czy epizod się zakończył.
2. Proces treningu obejmuje aktualizację wag modelu w celu minimalizacji błędów predykcji akcji, które prowadzą do maksymalizacji sumarycznej nagrody.


## Użycie wyuczonego modelu:

1. Po zakończeniu treningu model jest zapisywany i może być ponownie załadowany do użycia w rzeczywistej symulacji.
2. Podczas symulacji robot wykorzystuje wyuczony model do podejmowania decyzji na podstawie aktualnego stanu (pozycja, kąt) poprzez wybór akcji, która maksymalizuje przewidywaną nagrodę.
3. Model predykcyjny zastępuje wcześniejszy heurystyczny algorytm nawigacji, co umożliwia bardziej efektywne i inteligentne poruszanie się robota po labiryncie.

# Ten proces ilustruje, jak można zastosować techniki uczenia maszynowego, w szczególności reinforcement learning, do rozwiązywania problemów nawigacyjnych w dynamicznych środowiskach.


