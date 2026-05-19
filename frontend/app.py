import streamlit as st
import requests

st.title("Personlig cykeltræner")
st.write("Upload din cykeldata-CSV for at få analyse, grafer og AI-feedback.")

uploaded_file = st.file_uploader("Vælg CSV-fil", type=["csv"])

if uploaded_file:
    file_bytes = uploaded_file.read()
    files = {"file": (uploaded_file.name, file_bytes, "text/csv")}
    # Analyse
    resp = requests.post("http://localhost:8000/analyze/", files=files)
    if resp.ok:
        stats = resp.json()
        st.subheader("Nøgletal")
        st.write(stats)
    # Grafer
    for plot_type, label in zip(["distance", "speed"], ["Distance", "Hastighed"]):
        resp = requests.post(f"http://localhost:8000/plot/{plot_type}", files=files)
        if resp.ok:
            st.subheader(f"{label} over tid")
            st.image(resp.content)
    # LLM-feedback
    resp = requests.post("http://localhost:8000/llm/", files=files)
    if resp.ok:
        feedback = resp.json()["feedback"]
        st.subheader("AI-coach feedback")
        st.write(feedback)
