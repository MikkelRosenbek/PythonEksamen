## Python Eksamensprojekt Todo-liste

## Status

Projektet er nu en fungerende MVP, hvor brugeren kan registrere cykelture via frontend, gemme dem i `data/myData.csv` og få statistik, grafer og AI-feedback på baggrund af de gemte ture.

## Det du allerede har lavet

### Projektstruktur
- Oprettet mapper til `backend`, `frontend`, `data` og projektfiler i roden
- Oprettet og opdateret `README.md`, `Projektbeskrivelse.md` og `Kørsel-lokalt.md`

### Datahåndtering
- Oprettet `data/myData.csv` som aktiv datafil
- Fjernet `data/sample.csv`
- Lavet backend-logik til at læse og skrive CSV-data

### Backend
- Oprettet FastAPI-app i `backend/main.py`
- Lavet endpoint til at hente ture: `GET /rides/`
- Lavet endpoint til at oprette ture: `POST /rides/`
- Lavet endpoint til statistik: `GET /analyze/`
- Lavet endpoints til grafer: `GET /plot/distance` og `GET /plot/speed`
- Lavet endpoint til AI-feedback: `GET /llm/`
- Tilføjet inputvalidering med Pydantic for nye ture

### Dataanalyse
- Lavet statistikfunktion i `backend/analysis.py`
- Håndteret tomt datasæt uden fejl

### Grafer
- Lavet graf for distance over tid
- Lavet graf for gennemsnitshastighed over tid
- Håndteret tomt datasæt i graferne

### Frontend
- Fjernet CSV-upload-flowet
- Lavet formularfelter til manuel indtastning af ture
- Viser nøgletal i frontend
- Viser grafer i frontend
- Viser AI-feedback i frontend
- Viser tabel over registrerede ture i frontend

### Oprydning og dokumentation
- Tilføjet `.gitignore`
- Opdateret README til den aktuelle løsning
- Opdateret projektbeskrivelse og kørselsvejledning
- Tilføjet kommentarer i kodefilerne

## Det mangler stadig

### Tests
- Skriv tests til statistikberegning
- Skriv tests til CSV-lagring
- Skriv tests til plotfunktioner
- Skriv tests til API-endpoints

### LLM-integration
- Erstat placeholder-feedback i `backend/llm.py` med et rigtigt API-kald
- Håndter fejl og timeouts fra LLM-tjenesten
- Tilføj konfiguration via miljøvariabler

### Kvalitet og tooling
- Tilføj `pyrightconfig.json`
- Tilføj `pyproject.toml` eller tilsvarende konfiguration til linting
- Kør og ret kode efter lint/type-check

### Funktionelle forbedringer
- Tilføj mulighed for at redigere eksisterende ture
- Tilføj mulighed for at slette ture
- Tilføj flere nøgletal, fx højdemeter-sum eller længste varighed
- Tilføj flere grafer, fx højdemeter over tid

### Brugeroplevelse
- Forbedr layout og visuel præsentation i frontend
- Gør fejlbeskeder tydeligere, hvis backend ikke kører
- Overvej visning af success/error-state tættere på formularen

### Docker
- Opret Dockerfile til backend
- Opret Dockerfile til frontend
- Udfyld `docker-compose.yml`

## Anbefalet næste rækkefølge

1. Skriv tests til `analysis.py`, `data_store.py` og `plots.py`
2. Tilføj rigtig LLM-integration i `llm.py`
3. Tilføj redigering og sletning af ture
4. Tilføj lint/type-check konfiguration
5. Lav Docker-opsætning
