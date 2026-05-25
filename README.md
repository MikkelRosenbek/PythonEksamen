# Personlig cykeltræner

En webapplikation til registrering og analyse af cykelture. Brugeren indtaster ture i en Streamlit-frontend, data gemmes i `data/myData.csv`, og en FastAPI-backend leverer statistik, grafer og AI-feedback via en lokal Ollama-model.

## Sådan starter du programmet

Den nemmeste måde er at bruge Docker Compose. Alternativt kan du køre backend og frontend lokalt uden Docker.

### Mulighed 1: Docker Compose

Denne løsning starter frontend og backend i containere. Ollama kører stadig lokalt på din egen maskine.

#### Krav

- Docker Desktop installeret og kørende
- Ollama installeret og kørende
- modellen `llama3.2:3b` installeret i Ollama

Kontrollér fx Ollama sådan:

```bash
ollama list
```

Start hele applikationen:

```bash
docker compose up -d
```

Åbn derefter:

```text
http://localhost:8501
```

Stop applikationen igen:

```bash
docker compose down
```

Se logs:

```bash
docker compose logs -f
```

### Mulighed 2: Kør projektet lokalt på Windows

#### 1. Opret og aktivér virtuelt miljø

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

#### 2. Installer afhængigheder

```powershell
pip install -r requirements.txt
```

#### 3. Start Ollama

Kontrollér at modellen findes:

```powershell
ollama list
```

Hvis `llama3.2:3b` mangler:

```powershell
ollama pull llama3.2:3b
```

#### 4. Start backend

```powershell
python -m uvicorn backend.main:app --reload
```

#### 5. Start frontend i en ny terminal

```powershell
.\venv\Scripts\Activate.ps1
python -m streamlit run frontend/app.py
```

Åbn derefter:

```text
http://localhost:8501
```

### Mulighed 3: Kør projektet lokalt på macOS

#### 1. Opret og aktivér virtuelt miljø

```bash
python3 -m venv venv
source venv/bin/activate
```

#### 2. Installer afhængigheder

```bash
pip install -r requirements.txt
```

#### 3. Start Ollama

Kontrollér at modellen findes:

```bash
ollama list
```

Hvis `llama3.2:3b` mangler:

```bash
ollama pull llama3.2:3b
```

#### 4. Start backend

```bash
python -m uvicorn backend.main:app --reload
```

#### 5. Start frontend i en ny terminal

```bash
source venv/bin/activate
python -m streamlit run frontend/app.py
```

Åbn derefter:

```text
http://localhost:8501
```

## Hvad programmet kan

- oprette nye cykelture via formular
- gemme ture i `data/myData.csv`
- vise registrerede ture i en samlet oversigt
- redigere eksisterende ture
- slette ture
- beregne nøgletal
- vise grafer for distance og hastighed
- generere AI-feedback ud fra træningsdata via Ollama

## Projektstatus

Projektet fungerer som en sammenhængende MVP med:

- Streamlit-frontend
- FastAPI-backend
- CSV-baseret datalagring
- CRUD for ture
- lokale grafer
- lokal LLM-integration via Ollama
- tests
- `ruff` og `pyright`
- Docker Compose



## Funktioner

### Frontend

- formular til oprettelse og redigering af cykelture
- kompakt tabelvisning af registrerede ture
- knapper til `Ret` og `Slet`
- visning af nøgletal
- visning af grafer
- visning af AI-feedback

### Backend

- `GET /rides/` returnerer alle ture
- `POST /rides/` opretter en ny tur
- `PUT /rides/{ride_id}` opdaterer en tur
- `DELETE /rides/{ride_id}` sletter en tur
- `GET /analyze/` returnerer statistik
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
test/
  test_analysis.py
  test_data_store.py
  test_plots.py
backend/Dockerfile
frontend/Dockerfile
docker-compose.yml
pyproject.toml
pytest.ini
requirements.txt
README.md
```

## Dataformat

Data gemmes i `data/myData.csv` med disse kolonner:

```csv
id,date,ride_name,distance_km,duration_min,avg_speed_kmh,elevation_m
1,2026-05-24,Morgentur,42.50,95,26.8,210
```

### Felter

- `id`: løbende heltal genereret af backend
- `date`: dato i formatet `YYYY-MM-DD`
- `ride_name`: navn på turen
- `distance_km`: distance i kilometer
- `duration_min`: varighed i minutter
- `avg_speed_kmh`: gennemsnitshastighed i kilometer i timen
- `elevation_m`: højdemeter

## AI-feedback

AI-feedbacken kører gennem Ollama og bruger som standard modellen:

```text
llama3.2:3b
```

Backend forventer som udgangspunkt:

- `OLLAMA_API_URL=http://localhost:11434/api/generate` ved lokal kørsel
- `OLLAMA_API_URL=http://host.docker.internal:11434/api/generate` i Docker Compose

Hvis Ollama ikke kører, vises en fallback-besked i frontend i stedet for at appen crasher.

## Kvalitetssikring

Projektet kan verificeres med:

```bash
python -m pytest test -q
python -m ruff check backend frontend test
python -m pyright
```

På Windows kan du også køre dem eksplicit via projektets venv:

```powershell
.\venv\Scripts\python.exe -m pytest test -q
.\venv\Scripts\python.exe -m ruff check backend frontend test
.\venv\Scripts\python.exe -m pyright
```

## Teknologier

- Python
- FastAPI
- Streamlit
- Pandas
- NumPy
- Matplotlib
- Requests
- Ollama
- Pytest
- Ruff
- Pyright
- Docker Compose

## Kendte begrænsninger

- projektet bruger CSV i stedet for database
- AI-feedbackens kvalitet afhænger af den lokale Ollama-model
- Ollama er ikke containeriseret i denne opsætning, men kører lokalt ved siden af Docker
