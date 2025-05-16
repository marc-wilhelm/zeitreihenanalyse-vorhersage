# SARIMA-Prognose: Funktionsweise und Interpretation

## Funktionsweise des Codes

Der Code `sarima_prognose_einfach.py` führt folgende Schritte aus:

1. **Laden der SARIMA-Parameter** aus zuvor optimierten Modellen.

2. **SARIMA-Modellierung**: Für jede Stadt wird ein SARIMA-Modell mit den optimalen Parametern aufgebaut und an die differenzierten Daten angepasst.

3. **Differenzierte Prognosen**: Es werden Prognosen und Konfidenzintervalle für die nächsten 10 Perioden im differenzierten Raum berechnet.

4. **Rücktransformation**: Die differenzierten Prognosen werden zu absoluten Temperaturwerten zurückgerechnet. Dies geschieht nach folgenden Formeln:
- Bei regulärer und saisonaler Differenzierung (d=1, D=1):
```
y_t = y_{t-1} + y_{t-m} - y_{t-m-1} + Δ²_m y_t
```
- Bei nur saisonaler Differenzierung (d=0, D=1):
```
y_t = y_{t-m} + Δ_m y_t
```

5. **Datumserweiterung**: Den Prognosen werden fortlaufende Datumsangaben zugewiesen.

6. **Ausgabe und Speicherung**: Ergebnisse werden in der Konsole ausgegeben und als CSV-Dateien und Grafiken gespeichert.

## Interpretation des Outputs

### Angeles (SARIMA(2,1,2)x(1,1,1,12))

- **Temperaturwerte**: Die Prognosen zeigen einen stabilen Bereich von 25.9°C bis 27.1°C.
- **Saisonalität**: Es gibt leichte saisonale Schwankungen mit höheren Werten im Januar (27.1°C) und März (26.9°C).
- **Konfidenzintervalle**: Mit etwa ±1°C sind sie relativ eng, was auf eine gute Vorhersagegenauigkeit hindeutet.
- **Fazit**: Angeles zeigt ein typisches, stabiles Klima mit geringer saisonaler Variabilität.

### Abakan (SARIMA(0,0,2)x(1,1,1,12))

- **Temperaturwerte**: Deutliche saisonale Schwankungen von -21.8°C im Januar bis 17.1°C im Juni.
- **Saisonalität**: Sehr ausgeprägter Jahreszyklus mit kalten Wintern (Dezember bis Februar unter -19°C) und warmen Sommern.
- **Konfidenzintervalle**: Mit etwa ±6°C deutlich breiter als bei Angeles, was die höhere Klimavariabilität widerspiegelt.
- **Fazit**: Abakan zeigt ein extremes kontinentales Klima mit sehr deutlichen Jahreszeiten.

### Berlin (SARIMA(2,0,2)x(1,1,1,12))

- **Temperaturwerte**: Moderate Schwankungen von -1.9°C im Februar bis 16.2°C im Juni.
- **Saisonalität**: Klarer Jahreszyklus, aber weniger extrem als Abakan.
- **Konfidenzintervalle**: Mit etwa ±5°C zeigen sie eine mittlere Prognoseunsicherheit.
- **Fazit**: Berlin weist ein typisches mitteleuropäisches Klima mit deutlichen, aber nicht extremen saisonalen Schwankungen auf.

### Vergleichende Interpretation

Die Prognosen spiegeln die unterschiedlichen Klimazonen der drei Städte wider:

1. **Klimatypen**:
- Angeles: Warmes, stabiles Klima mit geringen Schwankungen (maritim/mediterran)
- Abakan: Extremes Kontinentalklima mit starken Temperaturschwankungen
- Berlin: Gemäßigtes mitteleuropäisches Klima

2. **Prognosesicherheit**: Die Breite der Konfidenzintervalle korreliert mit der klimatischen Variabilität: Je variabler das Klima, desto breiter die Intervalle.

3. **Jahreszeitliche Muster**: Alle drei Städte zeigen unterschiedlich ausgeprägte saisonale Muster, die mit ihren geografischen Lagen übereinstimmen.

Die SARIMA-Modelle erfassen die saisonalen Muster und Trends der Temperaturdaten und liefern plausible Prognosen für die kommenden 10 Monate. Die Konfidenzintervalle geben ein realistisches Bild der Prognoseunsicherheit in den jeweiligen Klimazonen.