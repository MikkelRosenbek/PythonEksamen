# Projektbeskrivelse

**Navn:** Mikkel Rosenbek  
**Mail:** Miro0002@stud.ek.dk  
**Fag:** Python, Forår 2026

## Projekttitel

**Personlig cykeltræner**

## Beskrivelse af programmet

Jeg har lavet en webapplikation, der fungerer som en simpel personlig cykeltræner. Brugeren indtaster data om sine cykelture direkte i frontend gennem en formular i stedet for at uploade en CSV-fil. Når en ny tur gemmes, bliver den skrevet til `data/myData.csv`.

Programmet viser centrale nøgletal som samlet distance, samlet træningstid, gennemsnitshastighed, antal ture og længste tur. Derudover viser applikationen grafer over udviklingen i træningen over tid, blandt andet distance pr. tur og gennemsnitshastighed pr. tur.

Brugeren kan også få AI-baseret feedback på sin træning. AI-coachen bruger de samlede data fra `myData.csv` og giver et kort, letforståeligt overblik samt forslag til næste træningspas.

## Data

Programmet bruger en lokal CSV-fil, `data/myData.csv`, som internt datalager. Brugeren arbejder ikke direkte med filen, men opretter i stedet nye ture gennem formularfelter i frontend.

CSV-filen indeholder disse kolonner:

- `date`
- `distance_km`
- `duration_min`
- `avg_speed_kmh`
- `elevation_m`

Eksempel:

```csv
date,distance_km,duration_min,avg_speed_kmh,elevation_m
2026-05-09,75.04,169,26.9,422
```

I denne version bruges der ikke Strava-, Garmin- eller andre eksterne API'er. Fokus er på en enkel og lokal løsning, hvor brugeren kan registrere ture manuelt og få analyse, grafer og AI-feedback på baggrund af egne data.
