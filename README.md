# Zeitreihenanalyse und Vorhersage

## 1. Thematischer Überblick
Im Rahmen dieses Projekts sollen drei verschiedene Zeitreihen, die Temperaturdaten verschiedener Länder enthalten, analysiert werden. Darüber hinaus soll im Rahmen eines Forecasting Engineerings die zukünftige Entwicklung der jährlichen Durchschnittstemperaturen vorhergesagt werden. Dabei wird folgendes Vorgehen angewandt. Zunächst wird für jede einzelne Zeitreihe ein einzelnes passendes Prognosemodell gesucht. Anschließend wird darauf aufbauend ein übergreifender Algorithmus aufgesetzt, der eine passende Temperaturvorhersage für alle drei gewählten Länder liefert. Die Programmierung wird mittels Python durchgeführt. 

## 2. Struktur des Repositories


```text
Zeitreihenanalyse-vorhersage/
│
├── daten/
│   ├── original-daten/                
│   │   ├── zeitreihe_kampala.txt
│   │   ├── zeitreihe_berlin.txt
│   │   └── zeitreihe_guangzhou.txt
│   ├── bereinigte-daten/          
│   │   ├── zeitreihe_kampala_bereinigt.csv
│   │   ├── zeitreihe_berlin_bereinigt.csv
│   │   └── zeitreihe_guangzhou_bereinigt.csv
│   
│
├── module/    
│   ├── datenbereinigung.py                
│   ├── hilfsfunktionen/          
│   │   ├── stationaritätstest.py
│
├── main.py                 
├── config.py                    
│
│
├── ergebnisse/   
│   ├── zeitreihe-kampala/                                 
│   │  
│   ├── zeitreihe_berlin/          
│   │
│   │── zeitreihe_guangzhou/ 
│
├── requirements.txt       
├── setup.py                
├── .gitignore              
└── README.md               

```

**Branch-Struktur**

- Main branch (stabile Version)
- Develop branch (Entwicklungsumgebung)
- Features:
  - Zeitreihe_Kampala
  - Zeitreihe_Berlin
  - Zeitreihe_Guangzhou


## 3. Best Practices
### 3.1 Commit-Messages
Orientierung an allgemeiner Konvention (fix, chore, feat, docs, add)

https://www.conventionalcommits.org/en/v1.0.0/ 

### 3.2 Code Dokumentation

Kurze einzeilige Beschreibung der Funktion.

Ausführlichere Beschreibung der Funktion, die mehrere Zeilen umfassen kann. Hier solltest du den Zweck und die allgemeine Funktionsweise erklären.


*Parameters:*
- param1: typ
- Beschreibung von param1 und seine Rolle


*Returns:*
- rückgabetyp
- Beschreibung dessen, was zurückgegeben wird

*Erklärung spezifischer Funktionsdetails:*
- Stichpunktartige Beschreibung neben entsprechende Codezeile 

### 3.3 Benennungen

- Funktionsnamen: UpperCamelCase
- Hilfsfunktionen: Funktionsnamen
- Modulnamen: Überbegriff in snake_case

### 3.4 Umgang mit merge-Konflikten

Bei signifikanten Unterschieden, Absprache mit entsprechendem Teammitglied

        
    
   
