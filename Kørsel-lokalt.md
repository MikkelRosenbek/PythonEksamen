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
uvicorn backend.main:app --reload
```

4. Start frontend (Streamlit):
```
streamlit run frontend/app.py
```

5. Åbn Streamlit i din browser (typisk på http://localhost:8501), upload sample.csv og se resultaterne.

Hvis du senere vil køre med Docker Compose, kan du nemt tilføje Dockerfiles og docker-compose.yml.
