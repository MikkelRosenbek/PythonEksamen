# Projektbeskrivelse

**Navn:** Mikkel Rosenbek  
**Mail:** Miro0002@stud.ek.dk  
**Fag:** Python, Forår 2026  

---

## Projekttitel

**Personlig cykeltræner**

---

## Beskrivelse af programmet

Jeg vil lave en webapplikation, der fungerer som en simpel personlig cykeltræner. Brugeren skal kunne uploade en CSV-fil med data fra sine cykelture og derefter få et overblik over sin træning.

Programmet skal vise centrale nøgletal som samlet distance, samlet træningstid, gennemsnitshastighed, antal ture, længste tur og hårdeste tur. Derudover skal applikationen vise grafer, så brugeren kan se udviklingen i sin træning over tid, fx distance pr. tur, gennemsnitshastighed og træningsbelastning.

Brugeren skal også kunne få AI-baseret feedback på sin træning. AI-coachen skal forklare dataene i et letforståeligt sprog og komme med forslag til næste træningspas. Programmet skal ikke erstatte en rigtig træner, men fungere som en prototype, der viser, hvordan dataanalyse og en LLM kan kombineres.

---

## Data

Programmet bruger cykeldata fra en CSV-fil, som brugeren uploader i applikationen. I første version bruger jeg eksempeldata eller manuelt indtastede data baseret på egne cykelture. Jeg bruger ikke Strava eller Garmin API i første version, fordi det vil gøre projektet unødvendigt komplekst.

CSV-filen skal blandt andet indeholde:

- dato
- distance i km
- tid
- gennemsnitshastighed
- højdemeter
- oplevet hårdhed/effort

Eksempel på kolonner:

```csv
date,distance_km,duration_min,avg_speed_kmh,elevation_m,effort