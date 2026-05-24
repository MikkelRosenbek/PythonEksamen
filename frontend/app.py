from __future__ import annotations

from datetime import date

import pandas as pd
import requests
import streamlit as st


API_BASE_URL = "http://localhost:8000"


def fetch_json(path: str) -> dict | None:
    # Saml fejlvisning ét sted, så frontend reagerer ens på backend-fejl.
    try:
        response = requests.get(f"{API_BASE_URL}{path}", timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        st.error(f"Kunne ikke hente data fra backend: {exc}")
        return None


def render_stats() -> None:
    # Hent og vis de vigtigste nøgletal øverst på siden.
    stats = fetch_json("/analyze/")
    if not stats:
        return

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Samlet distance", f"{stats['total_distance']:.2f} km")
    col2.metric("Samlet tid", f"{stats['total_time_min']:.0f} min")
    col3.metric("Gns. hastighed", f"{stats['avg_speed']:.1f} km/t")
    col4.metric("Antal ture", stats["num_rides"])
    st.metric("Længste tur", f"{stats['longest_ride']:.2f} km")


def render_plots() -> None:
    # Streamlit kan vise billeder direkte fra backendens plot-endpoints.
    st.subheader("Grafer")
    st.image(f"{API_BASE_URL}/plot/distance", caption="Distance over tid")
    st.image(f"{API_BASE_URL}/plot/speed", caption="Hastighed over tid")


def render_feedback() -> None:
    # AI-feedback vises kun, hvis backend returnerer et gyldigt svar.
    feedback = fetch_json("/llm/")
    if feedback and "feedback" in feedback:
        st.subheader("AI-coach feedback")
        st.write(feedback["feedback"])


def render_rides_table() -> None:
    # Tabellen giver brugeren et direkte overblik over indholdet i myData.csv.
    rides_payload = fetch_json("/rides/")
    if not rides_payload:
        return

    rides = rides_payload.get("rides", [])
    st.subheader("Registrerede ture")
    if not rides:
        st.info("Der er ingen ture i data/myData.csv endnu.")
        return

    df = pd.DataFrame(rides)
    st.dataframe(df, use_container_width=True, hide_index=True)


st.set_page_config(page_title="Personlig cykeltræner", layout="wide")
st.title("Personlig cykeltræner")
st.write("Registrer dine cykelture direkte i formularen. Data gemmes i `data/myData.csv`.")

with st.form("ride_form", clear_on_submit=True):
    # Formularen opretter én ny tur ad gangen og sender den til backend som JSON.
    st.subheader("Ny cykeltur")
    col1, col2 = st.columns(2)
    ride_date = col1.date_input("Dato", value=date.today(), format="YYYY-MM-DD")
    distance_km = col2.number_input("Distance (km)", min_value=0.1, step=0.1, format="%.2f")

    col3, col4, col5 = st.columns(3)
    duration_min = col3.number_input("Varighed (min)", min_value=1.0, step=1.0, format="%.0f")
    avg_speed_kmh = col4.number_input("Gns. hastighed (km/t)", min_value=0.1, step=0.1, format="%.1f")
    elevation_m = col5.number_input("Højdemeter", min_value=0.0, step=1.0, format="%.0f")

    submitted = st.form_submit_button("Gem tur")

if submitted:
    # Payload matcher Pydantic-modellen i backend.
    payload = {
        "date": ride_date.strftime("%Y-%m-%d"),
        "distance_km": distance_km,
        "duration_min": duration_min,
        "avg_speed_kmh": avg_speed_kmh,
        "elevation_m": elevation_m,
    }
    try:
        response = requests.post(f"{API_BASE_URL}/rides/", json=payload, timeout=10)
        response.raise_for_status()
        # Genindlæs siden efter succes, så statistik, grafer og tabel opdateres samlet.
        st.success("Turen blev gemt i data/myData.csv.")
        st.rerun()
    except requests.RequestException as exc:
        st.error(f"Kunne ikke gemme turen: {exc}")

render_stats()
render_plots()
render_feedback()
render_rides_table()
