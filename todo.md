## Python Eksamensprojekt Todo-liste

### 1. Projektstruktur
- Opret mappestruktur:
  - `/backend`, `/frontend`, `/tests`, `/data`, `docker-compose.yml`, `README.md`
  - **Filer:** backend/, frontend/, tests/, data/, docker-compose.yml, README.md
  - **Hvorfor:** Giver klar adskillelse af frontend, backend, tests og data, og forbereder til Docker Compose.

### 2. Data og CSV-format
- Lav eksempel-CSV med myData-data (fx fiktive målinger):
  - **Fil:** data/myData.csv
  - **Hvorfor:** Giver grundlag for dataanalyse og test af hele flowet.
- Beskriv CSV-formatet i README:
  - **Fil:** README.md
  - **Hvorfor:** Gør det tydeligt for brugeren, hvordan data skal struktureres.

### 3. Backend med FastAPI
- Initialiser FastAPI-app:
  - **Fil:** backend/main.py
  - **Hvorfor:** Krav om FastAPI-backend.
- Endpoint til upload/indlæsning af CSV:
  - **Fil:** backend/main.py
  - **Hvorfor:** Muliggør dataanalyse på brugerens data.
- Endpoint til at returnere analyseresultater og grafer:
  - **Fil:** backend/main.py
  - **Hvorfor:** Gør det muligt for frontend at hente analyser og grafer.

### 4. Dataanalyse med Pandas/NumPy
- Funktion til at læse og analysere CSV-data:
  - **Fil:** backend/analysis.py
  - **Hvorfor:** Krav om brug af Pandas og NumPy til dataanalyse.
- Returnér simple statistikker (fx gennemsnit, sum):
  - **Fil:** backend/analysis.py
  - **Hvorfor:** Viser anvendelse af NumPy/Pandas.

### 5. Grafer med Matplotlib
- Funktion til at generere grafer (fx linjeplot):
  - **Fil:** backend/plots.py
  - **Hvorfor:** Krav om brug af Matplotlib.
- Endpoint til at returnere grafer som billeder:
  - **Fil:** backend/main.py
  - **Hvorfor:** Gør det muligt for frontend at vise grafer.

### 6. Frontend med Streamlit
- Initialiser Streamlit-app:
  - **Fil:** frontend/app.py
  - **Hvorfor:** Krav om Streamlit frontend.
- Upload-knap til CSV og visning af analyser/grafer:
  - **Fil:** frontend/app.py
  - **Hvorfor:** Giver brugeren adgang til hele flowet.
- Kald backend via HTTP (requests):
  - **Fil:** frontend/app.py
  - **Hvorfor:** Forbinder frontend og backend.

### 7. LLM-integration
- Funktion til at sende prompt til LLM API (fx Mistral):
  - **Fil:** backend/llm.py
  - **Hvorfor:** Krav om LLM-integration.
- Endpoint til at returnere LLM-svar baseret på analyseresultater:
  - **Fil:** backend/main.py
  - **Hvorfor:** Gør det muligt at vise LLM-output i frontend.
- Vis LLM-svar i Streamlit:
  - **Fil:** frontend/app.py
  - **Hvorfor:** Fuldender LLM-kravet.

### 8. Tests
- Skriv unit tests for analyse- og plotfunktioner:
  - **Fil:** tests/test_analysis.py, tests/test_plots.py
  - **Hvorfor:** Krav om pytest tests.

### 9. Type checking og linting
- Tilføj type hints til alle funktioner:
  - **Fil:** backend/analysis.py, backend/plots.py, backend/llm.py, backend/main.py, frontend/app.py
  - **Hvorfor:** Krav om type checking med pyright.
- Konfigurer pyright og ruff:
  - **Fil:** pyrightconfig.json, pyproject.toml
  - **Hvorfor:** Krav om type checking og linting.

### 10. Docker Compose
- Skriv Dockerfile til backend og frontend:
  - **Fil:** backend/Dockerfile, frontend/Dockerfile
  - **Hvorfor:** Gør det muligt at køre begge services i containere.
- Skriv docker-compose.yml til at starte begge services:
  - **Fil:** docker-compose.yml
  - **Hvorfor:** Krav om Docker Compose.

### 11. README og aflevering
- Skriv README med:
  - Projektbeskrivelse
  - Installations- og kørselsvejledning
  - Beskrivelse af CSV-format
  - Hvordan man kører tests, type checks og linting
  - **Fil:** README.md
  - **Hvorfor:** Gør det nemt for censor/eksaminator at forstå og afprøve projektet.

**Bemærk:**
- Ingen Strava API, login, database eller avancerede features.
- Fokus på MVP: upload, analyse, graf, LLM, tests, type checks, linting, Docker Compose.
- Hold alle funktioner simple og veldokumenterede.
