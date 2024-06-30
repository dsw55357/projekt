Poniżej przedstawiam dokumentację kodu źródłowego w języku Python, który wykorzystuje bibliotekę Pygame do symulacji robota oraz uczenia się przy użyciu algorytmu Deep Q-Learning (DQN).

## Dokumentacja kodu

### Wykorzystywane moduły
- `pygame`: Biblioteka do tworzenia gier 2D i symulacji.
- `os`: Obsługa operacji systemowych.
- `datetime`: Operacje na datach i czasie.
- `math`: Funkcje matematyczne.
- `numpy`: Biblioteka do obliczeń numerycznych i operacji na tablicach.
- `random`: Generowanie liczb losowych.
- `csv`: Obsługa plików CSV.
- `json`: Operacje na danych w formacie JSON.
- `tensorflow`: Biblioteka do uczenia maszynowego.
- `tensorflow.keras`: Wysokopoziomowe API dla TensorFlow, używane do budowy i trenowania modeli.

### Stałe i parametry
- **DQN**: Parametry związane z algorytmem Deep Q-Learning:
  - `GAMMA`: Współczynnik dyskontowania.
  - `EPSILON`, `EPSILON_DECAY`, `MIN_EPSILON`: Parametry eksploracji.
  - `BATCH_SIZE`: Rozmiar partii do trenowania modelu.
  - `LEARNING_RATE`: Wskaźnik uczenia.
  - `MEMORY_SIZE`: Rozmiar pamięci replay.

- **Parametry okna**:
  - `WIDTH`, `HEIGHT`: Wymiary okna symulacji.
  
- **Kolory**:
  - `WHITE`, `BLACK`, `RED`, `GREEN`: Definicje kolorów w formacie RGB.

- **Parametry robota**:
  - `SENSOR_RANGE`, `SPEED`, `ROBOT_RADIUS`, `TURN_RATE`: Parametry związane z ruchem i sensoryką robota.

### Klasy
- `PozycjaMenu`: Klasa reprezentująca pozycję w menu symulacji.
  - `__init__(self, id, nazwa, status=True)`: Inicjalizacja pozycji menu.
  - `zmien_status(self)`: Zmiana statusu pozycji menu (aktywne/nieaktywne).

### Funkcje
- **Inicjalizacja Pygame**:
  - `pygame.init()`: Inicjalizacja modułów Pygame.
  - `WIN`: Utworzenie okna symulacji.
  - `pygame.display.set_caption("Symulator Robota")`: Ustawienie tytułu okna.

- **Funkcje rysujące**:
  - `draw_frame()`: Rysowanie ramki wokół okna gry.
  - `draw_spiral()`: Rysowanie spirali na planszy.
  - `draw_robot(x, y, angle)`: Rysowanie robota w zadanej pozycji.
  - `draw_sensors(front_sensor, left_sensor, right_sensor)`: Rysowanie odczytów sensorów robota.
  - `hex_to_rgb(hex_color)`: Konwersja koloru HEX do formatu RGB.

- **Funkcje obsługi sensorów**:
  - `check_sensor(x, y, angle, offset_angle=0)`: Sprawdzanie odległości do przeszkód za pomocą sensora.
  - `get_state(x, y, angle)`: Przekształcanie stanu robota do formatu wykorzystywanego przez DQN.

- **Funkcje ruchu robota**:
  - `move_robot(x, y, angle)`: Ruch robota zgodnie z zasadami symulacji.
  - `move_robot_tf(x, y, angle, action)`: Ruch robota w zależności od akcji wybranej przez model.

- **Funkcje związane z DQN**:
  - `create_q_model()`: Tworzenie modelu Q-network.
  - `train_dqn_from_path()`: Trenowanie modelu DQN na podstawie zapisanych danych.

- **Funkcje zapisu i odczytu ścieżki**:
  - `save_path_to_file(path_data, filename="path_data.json")`: Zapisywanie ścieżki do pliku JSON.
  - `load_path_from_file(filename="path_data.json")`: Odczytywanie ścieżki z pliku JSON.

- **Główna funkcja symulacji**:
  - `main()`: Główna funkcja odpowiedzialna za uruchomienie symulacji, obsługę zdarzeń i interakcji z użytkownikiem.

### Problemy i uwagi
Podczas pracy z wyuczonym modelem robota zauważono, że robot nie radzi sobie z rozpoznaniem ściany labiryntu. Może to wynikać z kilku powodów:
- **Zbyt mała ilość danych treningowych**: Model może nie mieć wystarczającej ilości danych, aby nauczyć się prawidłowego rozpoznawania ścian.
- **Niewystarczająca złożoność modelu**: Prosty model może nie być w stanie uchwycić skomplikowanych wzorców wymaganych do prawidłowego rozpoznania przeszkód.
- **Zbyt wysoki współczynnik eksploracji**: Robot może zbyt często wybierać losowe akcje, zamiast korzystać z wyuczonych wzorców.

Na co zwrócić uwagę:
- **Zwiększenie liczby epok treningowych**: Więcej epok może poprawić zdolność modelu do rozpoznawania ścian.
- **Eksperymentowanie z hiperparametrami**: Zmiana wartości takich jak `LEARNING_RATE`, `BATCH_SIZE` może wpłynąć na efektywność uczenia.
- **Rozszerzenie danych treningowych**: Zwiększenie różnorodności i liczby danych może pomóc w lepszym generalizowaniu przez model.