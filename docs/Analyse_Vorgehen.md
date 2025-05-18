# Analytisches Vorgehen: Temperatur-Zeitreihenanalyse

## Projektüberblick

Das Ziel dieses Projekts bestand darin, historische Temperaturdaten von drei klimatisch unterschiedlichen Städten (Angeles, Abakan und Berlin) zu analysieren und präzise Vorhersagen für die kommenden 10 Monate zu erstellen. Die Herangehensweise folgte einem systematischen, methodischen Ansatz der modernen Zeitreihenanalyse.

## 1. Projektstruktur und Versionskontrolle

Der erste Schritt konzentrierte sich auf die Etablierung einer professionellen Arbeitsumgebung. Es wurde ein strukturiertes Git-Repository erstellt, das nicht nur die Zusammenarbeit ermöglicht, sondern auch die Reproduzierbarkeit der Ergebnisse sicherstellt. Diese Grundlage ist entscheidend für jedes datenwissenschaftliche Projekt, da sie Transparenz und Nachvollziehbarkeit gewährleistet.

## 2. Datenbereinigung und -aufbereitung

### Grundlegende Datenvalidierung
Die Datenbereinigung bildete das Fundament der gesamten Analyse. Zunächst wurden die rohen Temperaturdaten aus einer [Kaggle-Quelle](https://www.kaggle.com/datasets/berkeleyearth/climate-change-earth-surface-temperature-data) importiert, wobei besondere 
Aufmerksamkeit auf korrekte Trenn- und Dezimalzeichen gelegt wurde. Diese scheinbar einfachen Details können erhebliche Auswirkungen auf die gesamte nachfolgende Analyse haben.

### Standardisierung der Zeitperioden
Um eine vergleichbare Analysebasis zu schaffen, wurden alle drei Zeitreihen auf einen einheitlichen Startzeitpunkt (Januar 1880) harmonisiert. Dies war notwendig, da die Aufzeichnungen für jede Stadt zu unterschiedlichen Zeitpunkten begannen. Eine solche Standardisierung ist fundamental für multivariate Zeitreihenanalysen.

### Behandlung fehlender Werte
Ein kritischer Aspekt der Datenqualität ist der Umgang mit NaN-Werten. Fehlende Werte am Anfang oder Ende der Zeitreihen wurden entfernt, während für Lücken in der Mitte Warnungen ausgegeben wurden. In unserem Fall konzentrierten sich die fehlenden Werte auf die letzten Datenpunkte, was eine einfache Lösung ermöglichte.

## 3. Deskriptive Statistische Analyse

### Klimatische Charakterisierung
Für jede Stadt wurden umfassende statistische Kennzahlen berechnet, die fundamentale Einblicke in die klimatischen Unterschiede lieferten:

- **Abakan** zeigte extreme Temperaturschwankungen (-31°C bis +21°C) mit einer hohen Standardabweichung von 13,9°C, typisch für kontinentales Klima
- **Angeles** wies die stabilsten Temperaturen auf (22°C bis 30°C, Standardabweichung 1,3°C), charakteristisch für tropisches Klima
- **Berlin** lag zwischen den Extremen (-10°C bis 24°C, Standardabweichung 7°C), repräsentativ für gemäßigtes ozeanisches Klima

### Normalverteilungstests
Die Überprüfung der Normalverteilung mittels 70%- und 95%-Regeln lieferte wichtige Erkenntnisse über die Datenverteilung. Während Angeles eine nahezu perfekte Normalverteilung aufwies, zeigten Abakan und Berlin Abweichungen.

## 4. Stationaritätsanalyse

### Augmented Dickey-Fuller Test (ADF)
Der ADF-Test bildete das Herzstück der Stationaritätsanalyse. Stationarität ist eine fundamentale Voraussetzung für die meisten Zeitreihenmodelle, da sie konstante statistische Eigenschaften über die Zeit impliziert.

Die Ergebnisse zeigten unterschiedliche Stationaritätseigenschaften:
- Abakan und Berlin waren bereits von Natur aus stationär (`p < 0,05`)
- Angeles wies einen Trend auf und erforderte eine erste Differenzierung (`d = 1`)

### Saisonalitätstest (Kruskal-Wallis)
Der Kruskal-Wallis-Test identifizierte signifikante saisonale Muster in allen drei Zeitreihen. Diese Erkenntnis führte zur Anwendung saisonaler Differenzierung (`D = 1` für alle Städte), um stabile statistische Eigenschaften zu erreichen.

### Strukturbruchanalyse (CUSUM-Test)
Der CUSUM-Test untersuchte die Stabilität der Regressionsbeziehungen über die Zeit. Obwohl gelegentliche Ausschläge auftraten, zeigten alle Zeitreihen keine dauerhaften Strukturbrüche, was die Robustheit der verfügbaren Daten bestätigte.

## 5. Visuelle Datenexploration

### Zeitreihenvisualisierung
Die zeitreihenvisualisierung sowohl der ursprünglichen als auch der stationären Zeitreihen veranschaulichte erfolgreich die Effekte der Transformationen. Besonders deutlich wurde der eliminierte Trend in Angeles und die um null schwankenden differenzierten Werte aller stationären Reihen.

### Autokorrelations- und partielle Autokorrelationsanalyse
Die ACF- und PACF-Plots lieferten erste Hinweise auf die Modellstruktur. Signifikante Ausschläge bei Lag 1 und Lag 12 deuteten auf sowohl kurzfristige als auch saisonale Abhängigkeiten hin, was für SARIMA-Modelle spricht.

## 6. Modellidentifikation und -optimierung

### Automatisierte Modellselektion
Der Einsatz von Auto-ARIMA ermöglichte eine systematische Suche nach optimalen Modellparametern. Dieser Ansatz durchsucht automatisch den Parameterraum und identifiziert das beste Modell basierend auf Informationskriterien wie AIC (Akaike Information Criterion).

### Universelle Modellparameter
Ein besonders wertvoller Aspekt war die Entwicklung eines einheitlichen Modells für alle drei Zeitreihen. Die Parameter SARIMA(2,0,1)(1,0,1,12) erwiesen sich als optimal:
- `p = 2`: Aktuelle Temperatur hängt von den beiden Vormonaten ab
- `q = 1`: Berücksichtigung des Prognosefehlers vom Vormonat
- `P = 1`: Saisonale Abhängigkeit vom Vorjahresmonat
- `Q = 1`: Saisonaler Prognosefehler fließt in aktuelle Vorhersage ein

## 7. Modellvalidierung und -test

### Expanding Window Cross-Validation
Die Anwendung einer robusten Validierungsstrategie mit expandierenden Zeitfenstern simulierte reale Prognosebedingungen. Diese Methode beginnt mit 800 Datenpunkten für das Training und erweitert das Trainingsset kontinuierlich um 160 Punkte, wobei auf die nächsten 160 Punkte getestet wird.

### Residuenanalyse
Die Ljung-Box-Tests bestätigten, dass die Modellresiduen keine signifikante Autokorrelation aufwiesen (`p > 0,05` für alle Städte), was auf eine angemessene Modellspezifikation hindeutet. Die RMSE-Werte zeigten unterschiedliche Vorhersagegenauigkeiten:
- Angeles: 0,7°C (sehr präzise)
- Berlin: 2,6°C (moderat)
- Abakan: 3,0°C (akzeptabel für extreme Klimabedingungen)

## 8. Prognose und Rücktransformation

### Zukunftsprognosen
Das finale Modell generierte Vorhersagen für die nächsten 10 Monate, einschließlich 95%-Prognoseintervallen. Diese Intervalle liefern wichtige Informationen über die 
Unsicherheit der Prognosen.

### Inverse Transformation
Ein kritischer Schritt war die Rücktransformation der differenzierten Prognosen in interpretierbare Temperaturwerte. Dieser Prozess berücksichtigt sowohl die einfache als auch die saisonale Differenzierung und liefert schlussendlich Temperaturprognosen in Grad Celsius.

### Validierung mit realen Daten
Die Überprüfung der ersten Prognosewerte mit tatsächlichen historischen Daten bestätigte die Modellqualität:
- **Abakan**: Prognose 9°C vs. Realität 9°C
- **Angeles**: Prognose 26,9°C vs. Realität 26°C
- **Berlin**: Prognose 15°C vs. Realität 13°C

## Methodische Erkenntnisse

Diese systematische Herangehensweise demonstriert die Bedeutung einer strukturierten Zeitreihenanalyse. Jeder Schritt baut auf dem vorherigen auf und trägt zur Gesamtqualität der Prognosen bei. Die Kombination aus rigoroser statistischer Analyse, sorgfältiger Modellvalidierung und transparenter Dokumentation bildet das Fundament für verlässliche und interpretierbare Vorhersagemodelle.

Die Universalität des entwickelten Ansatzes zeigt, dass trotz unterschiedlicher klimatischer Bedingungen ein einheitliches Modell erfolgreich auf verschiedene Zeitreihen angewendet werden kann, was die Robustheit und Generalisierbarkeit der gewählten Methodik unterstreicht.