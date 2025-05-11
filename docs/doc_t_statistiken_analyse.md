# T-Statistiken-Analyse für Zeitreihenmodelle

## 1. Code-Erklärung

### Datenherkunft und Struktur
- Der Code nutzt die Temperaturdaten für drei Städte: Angeles, Abakan und Berlin
- Die Daten werden aus der `config.py` geladen (z.B. `config.seasonal_diff_angeles`)
- Es handelt sich um differenzierte Zeitreihen, die bereits für die Modellierung vorbereitet wurden

### Parameter-Import
```python
from parameter.sarima_params_angeles import order as angeles_order, seasonal_order as angeles_seasonal_order
from parameter.sarima_params_abakan import order as abakan_order, seasonal_order as abakan_seasonal_order
from parameter.sarima_params_berlin import order as berlin_order, seasonal_order as berlin_seasonal_order
```
- Die optimalen SARIMA-Parameter wurden bereits zuvor berechnet und in Dateien im `parameter`-Ordner gespeichert
- Diese werden automatisch importiert und für die Analyse verwendet
- Für die ARIMA-Modelle werden die nicht-saisonalen Komponenten (p, d, q) der SARIMA-Parameter verwendet

### Kernfunktionen
1. `analyse_arima_koeffizienten()`: Fitted ein ARIMA-Modell und gibt die Koeffizientenstatistiken aus
2. `analyse_sarima_koeffizienten()`: Fitted ein SARIMA-Modell und gibt die Koeffizientenstatistiken aus
3. `main()`: Führt die Analyse für alle drei Städte durch

## 2. Output-Interpretation

### ARIMA und SARIMA Parameter

**ARIMA(p,d,q)** besteht aus:
- **p**: Anzahl der autoregressiven Terme (AR)
- **d**: Grad der Differenzierung
- **q**: Anzahl der Moving-Average-Terme (MA)

**SARIMA(p,d,q)(P,D,Q,m)** erweitert ARIMA um saisonale Komponenten:
- **P**: Anzahl der saisonalen AR-Terme
- **D**: Grad der saisonalen Differenzierung
- **Q**: Anzahl der saisonalen MA-Terme
- **m**: Länge der Saison (hier 12 für Monate)

### Statistiken im Output

Für jeden Koeffizienten werden folgende Statistiken ausgegeben:
- **Koeffizient**: Der geschätzte Wert des Parameters
- **Std. Fehler**: Standardfehler der Schätzung
- **t-Wert**: Koeffizient geteilt durch Standardfehler (misst Signifikanz)
- **p-Wert**: Wahrscheinlichkeit, dass der Koeffizient zufällig von Null verschieden ist
- **Signifikant (p<0.05)**: Ob der Parameter statistisch signifikant ist (p < 0.05)

### Parameter-Bezeichnungen

- **ar.L1, ar.L2**: Autoregressive Parameter (Lag 1, Lag 2)
- **ma.L1, ma.L2**: Moving-Average Parameter (Lag 1, Lag 2)
- **ar.S.L12**: Saisonaler autoregressiver Parameter (Lag 12)
- **ma.S.L12**: Saisonaler Moving-Average Parameter (Lag 12)
- **const**: Konstante/Intercept
- **sigma2**: Varianz der Residuen

## 3. Interpretation der Koeffizienten

### Autoregressive Parameter (ar.L1, ar.L2)
- **Positive Werte**: Der aktuelle Wert folgt dem Trend des Vorgängerwerts
- **Negative Werte**: Der aktuelle Wert tendiert in die entgegengesetzte Richtung des Vorgängerwerts
- **Beispiel**: ar.L1 = -0.8 bedeutet, dass ein 1°C höherer Vormonatswert zu einer Verringerung um 0.8°C im aktuellen Monat führt

### Moving-Average Parameter (ma.L1, ma.L2)
- Zeigen, wie stark vergangene Fehler/Überraschungen den aktuellen Wert beeinflussen
- **Beispiel**: ma.L1 = -0.9 bedeutet, dass eine 1°C Überschätzung im Vormonat zu einer 0.9°C niedrigeren Prognose im aktuellen Monat führt

### Saisonale Parameter (ar.S.L12, ma.S.L12)
- Zeigen den Einfluss von Werten aus dem Vorjahr (gleicher Monat)
- **Beispiel**: ar.S.L12 = -0.5 bedeutet, dass ein 1°C wärmerer Januar im Vorjahr zu einem 0.5°C kühleren Januar im aktuellen Jahr führt

## 4. Beispielhafte Interpretation der Ergebnisse

### Angeles
- **ARIMA(2,1,2)**:
    - Stark negative AR-Parameter (ar.L1 = -1.39, ar.L2 = -0.45) zeigen eine schnelle Umkehrung von Temperaturtrends
    - Der ma.L1 ist nicht signifikant, aber ma.L2 hat einen starken negativen Einfluss

- **SARIMA(2,1,2)x(0,1,1,12)**:
    - Positive AR-Parameter (ar.L1 = 0.32, ar.L2 = 0.19) zeigen eine gewisse Persistenz von Temperaturtrends
    - Starke MA-Komponenten mit unterschiedlichen Vorzeichen
    - Starker saisonaler MA-Effekt (ma.S.L12 = -0.98) deutet auf eine ausgeprägte Korrektur von Fehlern des Vorjahres hin

### Abakan
- **ARIMA(0,1,2)**:
    - Keine AR-Komponenten, starke MA-Komponenten (ma.L1 = -0.82, ma.L2 = -0.18)
    - Deutet auf ein stärkeres Gewicht der jüngsten Fehler als auf vergangene Werte hin

- **SARIMA(0,1,2)x(1,1,1,12)**:
    - Ähnliche MA-Struktur wie ARIMA
    - Starke saisonale Komponenten (ar.S.L12 = -0.52, ma.S.L12 = -1.00)
    - Zeigt ausgeprägte jährliche Muster mit schneller Rückkehr zum Mittelwert nach saisonalen Abweichungen

### Berlin
- **ARIMA(2,0,2)**:
    - Konstante nicht signifikant
    - Nur AR-Parameter sind signifikant (ar.L1 = -0.74, ar.L2 = 0.17)
    - MA-Parameter und Varianz (sigma2) nicht signifikant - mögliches Anzeichen für ein ungeeignetes Modell

- **SARIMA(2,0,2)x(1,1,1,12)**:
    - ar.L2 nicht signifikant (p = 0.057), alle anderen Parameter signifikant
    - Starke gegensätzliche MA-Effekte (ma.L1 = -1.53, ma.L2 = 0.53)
    - Starke saisonale Komponenten (ar.S.L12 = -0.50, ma.S.L12 = -1.00)
    - Deutet auf ein besseres Modell als ARIMA hin

## 5. Fazit und nächste Schritte

- Die SARIMA-Modelle haben tendenziell mehr signifikante Parameter als die ARIMA-Modelle, was auf ihre bessere Eignung für Temperaturdaten hindeutet
- Für alle drei Städte zeigen sich starke saisonale Komponenten, insbesondere saisonale MA-Terme nahe -1
- Die Unterschiede in den Koeffizienten zwischen den Städten spiegeln verschiedene klimatische Charakteristika wider
