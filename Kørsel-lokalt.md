# Sådan kører du projektet lokalt

1. Opret og aktiver et virtuelt miljø (venv):

Windows PowerShell:
```
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. Installer alle afhængigheder:
```
pip install -r requirements.txt
```

3. Start backend (FastAPI):
```
python -m uvicorn backend.main:app --reload
```

4. Start frontend (Streamlit):
```
python -m streamlit run frontend/app.py
```

5. Åbn Streamlit i din browser (typisk på http://localhost:8501).

6. Indtast en cykeltur i formularen i frontend og tryk på `Gem tur`.

7. Data gemmes automatisk i `data/myData.csv`, og nøgletal, grafer og AI-feedback opdateres på baggrund af den samlede fil.

CSV-formatet i `data/myData.csv` er:
```csv
date,distance_km,duration_min,avg_speed_kmh,elevation_m
2026-05-09,75.04,169,26.9,422
```

Hvis du senere vil køre med Docker Compose, kan du nemt tilføje Dockerfiles og docker-compose.yml.
