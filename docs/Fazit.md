# Fazit und Lessons Learned

## Projektresümee

Unser Zeitreihenanalyse-Projekt für drei klimatisch unterschiedliche Städte war erfolgreich: Die entwickelten SARIMA-Modelle erreichen RMSE-Werte von 0,7°C für Angeles, 2,6°C für Berlin und 3,0°C für Abakan. Neben den fachlichen Ergebnissen brachte der Entwicklungsprozess wichtige Erkenntnisse über Projektorganisation und methodisches Vorgehen mit sich.

## Organisatorische Learnings

Die geplante Feature-Branch-Strategie mit separaten Branches für jede Zeitreihe erwies sich bei unserem dreiköpfigen Team als zu komplex. Ein pragmatischer Ansatz mit Haupt-Feature-Branch und Refactor-Branch war effizienter.

Die nachträgliche Umstrukturierung von einer monolithischen zu einer modularen Code-Organisation war zeitaufwendig, aber essentiell. Technische Hindernisse wie Python-Versionskonflikte und Package-Abhängigkeiten verstärkten die Herausforderung zusätzlich.

**Erkenntnis**: Eine durchdachte Projektarchitektur von Beginn an und Branching-Strategien, die zur realen Teamdynamik passen, sparen erheblichen Aufwand.

## Fachliche Erkenntnisse

Drei methodische Entscheidungen prägten den Projekterfolg: Der modulare Pipeline-Ansatz (Datenvorbereitung → Analyse → Modellierung → Bewertung) ermöglichte saubere Entwicklung und gezieltes Debugging. Auto-ARIMA automatisierte die komplexe Parameteroptimierung und war besonders wertvoll für unseren universellen Modellansatz. Der Dual-Ansatz mit individuellen und universellen Modellen demonstrierte sowohl optimale Performance pro Stadt als auch praktische Anwendbarkeit über verschiedene Klimazonen hinweg.

## Schlussbetrachtung

Das Projekt verdeutlichte, dass erfolgreiche Datenanalyseprojekte über reine Statistik hinausgehen. Projektorganisation und methodische Planung sind ebenso kritisch wie fachliche Expertise. Unsere strukturellen Herausforderungen führten letztendlich zu einem robusteren Endprodukt mit modularen Workflows, die eine solide Grundlage für zukünftige Erweiterungen schaffen.