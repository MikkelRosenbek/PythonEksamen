
import streamlit as st
import requests

st.title("Personlig cykeltræner")
st.write("Upload din cykeldata-CSV for at få analyse, grafer og AI-feedback.")

uploaded_file = st.file_uploader("Vælg CSV-fil", type=["csv"])

if uploaded_file:
	files = {"file": uploaded_file.getvalue()}
	# Analyse
	resp = requests.post("http://localhost:8000/analyze/", files={"file": uploaded_file})
	if resp.ok:
		stats = resp.json()
		st.subheader("Nøgletal")
		st.write(stats)
	# Grafer
	for plot_type, label in zip(["distance", "speed", "effort"], ["Distance", "Hastighed", "Effort"]):
		resp = requests.post(f"http://localhost:8000/plot/{plot_type}", files={"file": uploaded_file})
		if resp.ok:
			st.subheader(f"{label} over tid")
			st.image(resp.content)
	# LLM-feedback
	resp = requests.post("http://localhost:8000/llm/", files={"file": uploaded_file})
	if resp.ok:
		feedback = resp.json()["feedback"]
		st.subheader("AI-coach feedback")
		st.write(feedback)
