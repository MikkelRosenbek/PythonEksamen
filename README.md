# Personlig cykeltræner

En webapplikation til manuel registrering og analyse af cykelture. Brugeren indtaster ture i en Streamlit-frontend, data gemmes i `data/myData.csv`, og en FastAPI-backend leverer statistik, grafer og AI-feedback.

## Projektstatus

Projektet fungerer som en kørende MVP:

- Frontend med formular til indtastning af cykelture
- Lagring af ture i `data/myData.csv`
- Backend-endpoints til ture, statistik, grafer og AI-feedback
- Statistik for samlet distance, samlet tid, gennemsnitshastighed, antal ture og længste tur
- Grafer for distance og gennemsnitshastighed over tid
- Simpel placeholder til AI-coach feedback

Det, der stadig mangler før projektet er mere færdigt:

- Rigtige tests
- Rigtig LLM-integration i stedet for placeholder-tekst
- Type checking- og lint-konfiguration
- Docker-opsætning
- Eventuelt redigering og sletning af ture

## Funktioner

### Frontend

- Formular til registrering af:
  - dato
  - distance i km
  - varighed i minutter
  - gennemsnitshastighed i km/t
  - højdemeter
- Visning af:
  - nøgletal
  - grafer
  - AI-feedback
  - tabel med registrerede ture

### Backend

- `GET /rides/` returnerer alle registrerede ture
- `POST /rides/` gemmer en ny tur i `data/myData.csv`
- `GET /analyze/` returnerer beregnede nøgletal
- `GET /plot/distance` returnerer distancegraf
- `GET /plot/speed` returnerer hastighedsgraf
- `GET /llm/` returnerer AI-feedback

## Projektstruktur

```text
backend/
  analysis.py
  data_store.py
  llm.py
  main.py
  plots.py
frontend/
  app.py
data/
  myData.csv
README.md
Kørsel-lokalt.md
Projektbeskrivelse.md
requirements.txt
todo.md
```

## Dataformat

Data gemmes i `data/myData.csv` med disse kolonner:

```csv
date,distance_km,duration_min,avg_speed_kmh,elevation_m
2026-05-09,75.04,169,26.9,422
```

### Felter

- `date`: dato i formatet `YYYY-MM-DD`
- `distance_km`: distance i kilometer
- `duration_min`: varighed i minutter
- `avg_speed_kmh`: gennemsnitshastighed i kilometer i timen
- `elevation_m`: højdemeter

## Krav

Afhængighederne er listet i `requirements.txt`:

- `fastapi`
- `uvicorn`
- `pandas`
- `numpy`
- `matplotlib`
- `requests`
- `streamlit`

## Installation

### 1. Opret virtuelt miljø

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Installer pakker

```powershell
pip install -r requirements.txt
```

## Kørsel

### Start backend

```powershell
python -m uvicorn backend.main:app --reload
```

Backend kører typisk på:

```text
http://localhost:8000
```

### Start frontend

Åbn en ny terminal i projektmappen:

```powershell
.\venv\Scripts\Activate.ps1
python -m streamlit run frontend/app.py
```

Frontend kører typisk på:

```text
http://localhost:8501
```

## Brug

1. Start backend
2. Start frontend
3. Åbn Streamlit i browseren
4. Udfyld formularen med en ny cykeltur
5. Tryk på `Gem tur`
6. Se opdaterede nøgletal, grafer og AI-feedback

## Kodeoversigt

### `backend/main.py`

API-lag med endpoints til:

- hente ture
- oprette tur
- beregne statistik
- generere grafer
- hente AI-feedback

### `backend/data_store.py`

Ansvarlig for:

- læsning af `data/myData.csv`
- skrivning til `data/myData.csv`
- tilføjelse af nye ture

### `backend/analysis.py`

Beregner centrale nøgletal ud fra et pandas-dataframe.

### `backend/plots.py`

Genererer grafer som PNG-billeder via Matplotlib.

### `backend/llm.py`

Indeholder den nuværende placeholder til AI-feedback. Den er klar til at blive udskiftet med et rigtigt API-kald.

### `frontend/app.py`

Streamlit-brugerflade, som:

- viser formular
- sender nye ture til backend
- henter statistik
- viser grafer
- viser AI-feedback

## Hvad mangler

### Høj prioritet

- Skriv tests for backend-logik og plotfunktioner
- Implementer rigtig LLM-integration
- Tilføj bedre validering og fejlbeskeder

### Mellem prioritet

- Tilføj mulighed for at redigere eller slette ture
- Tilføj flere nøgletal og grafer
- Gør frontend mere poleret

### Lav prioritet

- Dockerfiles og `docker-compose.yml`
- `pyrightconfig.json`
- `pyproject.toml` med lint/type-check setup

## Kendte begrænsninger

- AI-feedback er i øjeblikket hardcoded placeholder-tekst
- Der er ingen automatiske tests endnu
- `docker-compose.yml` er endnu ikke sat op
- Projektet bruger lokal CSV-fil i stedet for database

## Verifikation

Koden er senest verificeret med:

```powershell
venv\Scripts\python.exe -m compileall backend frontend
```

## Mulige næste skridt

- skrive tests
- koble en rigtig LLM på
- tilføje CRUD for ture
- lave en rigtig containeropsætning
