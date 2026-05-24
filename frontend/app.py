from __future__ import annotations

from datetime import date

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


def get_rides() -> list[dict]:
    rides_payload = fetch_json("/rides/")
    if not rides_payload:
        return []
    return rides_payload.get("rides", [])


def get_edit_ride(rides: list[dict]) -> dict | None:
    edit_ride_id = st.session_state.get("edit_ride_id")
    if edit_ride_id is None:
        return None
    return next((ride for ride in rides if ride["id"] == edit_ride_id), None)


def clear_edit_mode() -> None:
    st.session_state["edit_ride_id"] = None


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
    spacer_left, col1, spacer_mid, col2, spacer_right = st.columns([0.2, 1, 0.15, 1, 0.2])
    col1.image(f"{API_BASE_URL}/plot/distance", caption="Distance over tid", width=470)
    col2.image(f"{API_BASE_URL}/plot/speed", caption="Hastighed over tid", width=470)


def render_feedback() -> None:
    # AI-feedback vises kun, hvis backend returnerer et gyldigt svar.
    feedback = fetch_json("/llm/")
    if feedback and "feedback" in feedback:
        st.subheader("AI-coach feedback")
        st.write(feedback["feedback"])


def render_rides_table(rides: list[dict]) -> None:
    # Brug én samlet tabelvisning, så data og handlinger hænger sammen på samme række.
    st.subheader("Registrerede ture")
    if not rides:
        st.info("Der er ingen ture i data/myData.csv endnu.")
        return

    header_cols = st.columns([1.1, 1.4, 0.8, 0.8, 0.9, 0.7, 0.7, 0.7])
    header_labels = ["Dato", "Navn", "Km", "Min", "Km/t", "Hm", "", ""]
    for col, label in zip(header_cols, header_labels):
        col.markdown(f"**{label}**")

    for ride in rides:
        row_cols = st.columns([1.1, 1.4, 0.8, 0.8, 0.9, 0.7, 0.7, 0.7])
        row_cols[0].caption(ride["date"])
        row_cols[1].caption(ride["ride_name"])
        row_cols[2].caption(f"{float(ride['distance_km']):.2f}")
        row_cols[3].caption(f"{float(ride['duration_min']):.0f}")
        row_cols[4].caption(f"{float(ride['avg_speed_kmh']):.1f}")
        row_cols[5].caption(f"{float(ride['elevation_m']):.0f}")

        if row_cols[6].button("Ret", key=f"edit_{ride['id']}"):
            st.session_state["edit_ride_id"] = ride["id"]
            st.rerun()

        if row_cols[7].button("Slet", key=f"delete_{ride['id']}"):
            try:
                response = requests.delete(f"{API_BASE_URL}/rides/{ride['id']}", timeout=10)
                response.raise_for_status()
                if st.session_state.get("edit_ride_id") == ride["id"]:
                    clear_edit_mode()
                st.success(f"Turen '{ride['ride_name']}' blev slettet.")
                st.rerun()
            except requests.RequestException as exc:
                st.error(f"Kunne ikke slette turen: {exc}")

        st.markdown(
            "<div style='height:1px;background-color:rgba(128,128,128,0.18);margin:0.15rem 0 0.35rem 0;'></div>",
            unsafe_allow_html=True,
        )


st.set_page_config(page_title="Personlig cykeltræner", layout="wide")
st.title("Personlig cykeltræner")
#st.write("Registrer dine cykelture direkte i formularen. Data gemmes i `data/myData.csv`.")

rides = get_rides()
edit_ride = get_edit_ride(rides)
is_editing = edit_ride is not None

with st.form("ride_form"):
    # Formularen bruges både til oprettelse og redigering af en tur.
    st.subheader("Redigér tur" if is_editing else "Ny cykeltur")

    default_date = date.fromisoformat(edit_ride["date"]) if is_editing else date.today()
    default_ride_name = edit_ride["ride_name"] if is_editing else ""
    default_distance = float(edit_ride["distance_km"]) if is_editing else 0.1
    default_duration = float(edit_ride["duration_min"]) if is_editing else 1.0
    default_speed = float(edit_ride["avg_speed_kmh"]) if is_editing else 0.1
    default_elevation = float(edit_ride["elevation_m"]) if is_editing else 0.0

    col1, col2 = st.columns(2)
    ride_date = col1.date_input("Dato", value=default_date, format="YYYY-MM-DD")
    ride_name = col2.text_input("Navn på tur", value=default_ride_name)

    col3, col4 = st.columns(2)
    distance_km = col3.number_input("Distance (km)", min_value=0.1, step=0.1, format="%.2f", value=default_distance)
    duration_min = col4.number_input("Varighed (min)", min_value=1.0, step=1.0, format="%.0f", value=default_duration)

    col5, col6 = st.columns(2)
    avg_speed_kmh = col5.number_input("Gns. hastighed (km/t)", min_value=0.1, step=0.1, format="%.1f", value=default_speed)
    elevation_m = col6.number_input("Højdemeter", min_value=0.0, step=1.0, format="%.0f", value=default_elevation)

    save_button_label = "Opdater tur" if is_editing else "Gem tur"
    submitted = st.form_submit_button(save_button_label)

if submitted:
    payload = {
        "date": ride_date.strftime("%Y-%m-%d"),
        "ride_name": ride_name.strip(),
        "distance_km": distance_km,
        "duration_min": duration_min,
        "avg_speed_kmh": avg_speed_kmh,
        "elevation_m": elevation_m,
    }

    if not payload["ride_name"]:
        st.error("Navn på tur skal udfyldes.")
    else:
        try:
            if is_editing:
                response = requests.put(
                    f"{API_BASE_URL}/rides/{edit_ride['id']}",
                    json=payload,
                    timeout=10,
                )
            else:
                response = requests.post(f"{API_BASE_URL}/rides/", json=payload, timeout=10)

            response.raise_for_status()
            clear_edit_mode()
            st.success("Turen blev gemt i data/myData.csv.")
            st.rerun()
        except requests.RequestException as exc:
            st.error(f"Kunne ikke gemme turen: {exc}")

if is_editing and st.button("Annuller redigering"):
    clear_edit_mode()
    st.rerun()

render_stats()
render_plots()
render_feedback()
render_rides_table(rides)
