from __future__ import annotations

import os
from datetime import date

import requests
import streamlit as st


API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


def fetch_json(path: str) -> dict | None:
    # Samler fejlvisning ét sted, så frontend reagerer ens på backend-fejl.
    try:
        response = requests.get(f"{API_BASE_URL}{path}", timeout=120)
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


def fetch_image(path: str) -> bytes | None:
    # Hent plotbilleder via backend, så samme kode virker både lokalt og i Docker.
    try:
        response = requests.get(f"{API_BASE_URL}{path}", timeout=120)
        response.raise_for_status()
        return response.content
    except requests.RequestException as exc:
        st.error(f"Kunne ikke hente graf fra backend: {exc}")
        return None


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
    # Hent plotbilleder som bytes, så frontend ikke afhænger af browserens netværksvej.
    st.subheader("Grafer")
    st.markdown(
        "<div class='section-note'>Se udviklingen i distance og gennemsnitshastighed over tid.</div>",
        unsafe_allow_html=True,
    )
    col1, spacer_mid, col2, spacer_right = st.columns([1, 0.18, 0.94, 0.08])
    distance_plot = fetch_image("/plot/distance")
    speed_plot = fetch_image("/plot/speed")

    if distance_plot:
        col1.image(distance_plot, caption="Distance over tid", width=450)
    if speed_plot:
        col2.image(speed_plot, caption="Hastighed over tid", width=450)


def render_feedback() -> None:
    # AI-feedback vises kun, hvis backend returnerer et gyldigt svar.
    feedback = fetch_json("/llm/")
    if feedback and "feedback" in feedback:
        st.subheader("AI-coach feedback")
        st.markdown(
            "<div class='section-note'>Kort opsummering og forslag baseret på dine seneste ture.</div>",
            unsafe_allow_html=True,
        )
        feedback_html = "<br><br>".join(
            line.strip()
            for line in feedback["feedback"].split("\n")
            if line.strip()
        )
        st.markdown(
            f"<div class='feedback-card'><p>{feedback_html}</p></div>",
            unsafe_allow_html=True,
        )


def render_rides_table(rides: list[dict]) -> None:
    # Brug én samlet tabelvisning, så data og handlinger hænger sammen på samme række.
    st.subheader("Registrerede ture")
    st.markdown(
        "<div class='section-note'>Alle registrerede ture med mulighed for hurtig redigering eller sletning.</div>",
        unsafe_allow_html=True,
    )
    if not rides:
        st.info("Der er ingen ture i data/myData.csv endnu.")
        return

    header_cols = st.columns([1.1, 1.45, 0.75, 0.75, 0.85, 0.7, 0.55, 0.55], gap="small")
    header_labels = ["Dato", "Navn", "Km", "Min", "Km/t", "Hm", "", ""]
    for col, label in zip(header_cols, header_labels):
        if label:
            col.markdown(f"<div class='ride-table-header'>{label}</div>", unsafe_allow_html=True)

    for index, ride in enumerate(rides):
        row_class = "ride-table-cell-even" if index % 2 == 0 else "ride-table-cell-odd"
        row_cols = st.columns([1.1, 1.45, 0.75, 0.75, 0.85, 0.7, 0.55, 0.55], gap="small")
        row_cols[0].markdown(
            f"<div class='ride-table-cell {row_class}'>{ride['date']}</div>",
            unsafe_allow_html=True,
        )
        row_cols[1].markdown(
            f"<div class='ride-table-cell {row_class}'>{ride['ride_name']}</div>",
            unsafe_allow_html=True,
        )
        row_cols[2].markdown(
            f"<div class='ride-table-cell {row_class}'>{float(ride['distance_km']):.2f}</div>",
            unsafe_allow_html=True,
        )
        row_cols[3].markdown(
            f"<div class='ride-table-cell {row_class}'>{float(ride['duration_min']):.0f}</div>",
            unsafe_allow_html=True,
        )
        row_cols[4].markdown(
            f"<div class='ride-table-cell {row_class}'>{float(ride['avg_speed_kmh']):.1f}</div>",
            unsafe_allow_html=True,
        )
        row_cols[5].markdown(
            f"<div class='ride-table-cell {row_class}'>{float(ride['elevation_m']):.0f}</div>",
            unsafe_allow_html=True,
        )

        if row_cols[6].button("Ret", key=f"edit_{ride['id']}", type="secondary"):
            st.session_state["edit_ride_id"] = ride["id"]
            st.rerun()

        if row_cols[7].button("Slet", key=f"delete_{ride['id']}", type="primary"):
            try:
                response = requests.delete(f"{API_BASE_URL}/rides/{ride['id']}", timeout=10)
                response.raise_for_status()
                if st.session_state.get("edit_ride_id") == ride["id"]:
                    clear_edit_mode()
                st.success(f"Turen '{ride['ride_name']}' blev slettet.")
                st.rerun()
            except requests.RequestException as exc:
                st.error(f"Kunne ikke slette turen: {exc}")

        st.markdown("<div class='ride-table-separator'></div>", unsafe_allow_html=True)


PAGE_STYLE = """
<style>
div[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(circle at top left, rgba(110, 168, 254, 0.18), transparent 22rem),
        linear-gradient(180deg, #f8fbff 0%, #eef4f7 100%);
}

div.block-container {
    max-width: 1180px;
    padding-top: 1.4rem;
    padding-bottom: 2rem;
}

h1 {
    font-size: 2.2rem;
    margin-bottom: 0.25rem;
    color: #12324a;
}

h3 {
    color: #163852;
    font-size: 1.45rem;
    margin-top: 1.4rem;
    margin-bottom: 0.75rem;
}

div[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.92);
    border: 1px solid rgba(18, 50, 74, 0.08);
    border-radius: 14px;
    padding: 0.55rem 0.8rem;
    box-shadow: 0 10px 24px rgba(18, 50, 74, 0.06);
}

div[data-testid="stForm"] {
    background: rgba(255, 255, 255, 0.94);
    border: 1px solid rgba(18, 50, 74, 0.08);
    border-radius: 18px;
    padding: 1rem 1rem 0.45rem 1rem;
    box-shadow: 0 12px 28px rgba(18, 50, 74, 0.06);
}

div[data-testid="stImage"] img {
    border-radius: 14px;
    border: 1px solid rgba(18, 50, 74, 0.08);
    box-shadow: 0 12px 28px rgba(18, 50, 74, 0.08);
}

div[data-testid="stButton"] > button {
    min-height: 1.8rem;
    padding: 0.1rem 0.5rem;
    border-radius: 999px;
}

div[data-testid="stForm"] div[data-testid="stButton"] > button {
    min-height: 2.3rem;
    padding: 0.3rem 0.95rem;
    box-shadow: 0 10px 22px rgba(18, 50, 74, 0.08);
}

div[data-testid="stForm"] label {
    font-weight: 600;
    color: #31536d;
}

.ride-table-header {
    font-size: 0.82rem;
    font-weight: 600;
    margin-bottom: 0.15rem;
    color: #4d6476;
    background: rgba(58, 123, 213, 0.08);
    border-radius: 10px;
    padding: 0.32rem 0.45rem;
}

.ride-table-cell {
    font-size: 0.8rem;
    line-height: 1.1;
    margin: 0;
    padding: 0.38rem 0.45rem;
    color: #17364e;
    border-radius: 10px;
}

.ride-table-cell-even {
    background: rgba(255, 255, 255, 0.74);
}

.ride-table-cell-odd {
    background: rgba(242, 247, 251, 0.94);
}

.ride-table-separator {
    height: 1px;
    background-color: transparent;
    margin: 0.05rem 0 0.16rem 0;
}

.page-intro {
    color: #476176;
    font-size: 0.98rem;
    margin-bottom: 1rem;
}

.feedback-card {
    background: linear-gradient(180deg, rgba(255, 255, 255, 0.96), rgba(243, 248, 252, 0.96));
    border: 1px solid rgba(18, 50, 74, 0.08);
    border-left: 5px solid #3a7bd5;
    border-radius: 18px;
    padding: 1rem 1.1rem 0.85rem 1.1rem;
    box-shadow: 0 12px 28px rgba(18, 50, 74, 0.06);
}

.feedback-card p {
    color: #17364e;
    line-height: 1.55;
    margin: 0 0 0.75rem 0;
}

.feedback-card p:last-child {
    margin-bottom: 0;
}

.form-intro {
    color: #5a7387;
    font-size: 0.92rem;
    margin-bottom: 0.7rem;
}

.section-note {
    color: #60798c;
    font-size: 0.9rem;
    margin-top: -0.2rem;
    margin-bottom: 0.7rem;
}
</style>
"""


st.set_page_config(page_title="Personlig cykeltræner", layout="wide")
st.markdown(PAGE_STYLE, unsafe_allow_html=True)
st.title("Personlig cykeltræner")
st.markdown(
    (
        "<div class='page-intro'>Registrer dine cykelture, følg udviklingen i dine "
        "nøgletal, og få AI-feedback på din træning.</div>"
    ),
    unsafe_allow_html=True,
)


rides = get_rides()
edit_ride = get_edit_ride(rides)
is_editing = edit_ride is not None

with st.form("ride_form"):
    # Formularen bruges både til oprettelse og redigering af en tur.
    st.subheader("Redigér tur" if is_editing else "Ny cykeltur")
    st.markdown(
        "<div class='form-intro'>Indtast turens vigtigste data. Du kan altid rette eller slette den senere.</div>",
        unsafe_allow_html=True,
    )

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
    avg_speed_kmh = col5.number_input(
        "Gns. hastighed (km/t)",
        min_value=0.1,
        step=0.1,
        format="%.1f",
        value=default_speed,
    )
    elevation_m = col6.number_input("Højdemeter", min_value=0.0, step=1.0, format="%.0f", value=default_elevation)

    save_button_label = "Opdater tur" if is_editing else "Gem tur"
    if is_editing:
        action_col1, action_col2 = st.columns([1, 1])
        submitted = action_col1.form_submit_button(save_button_label, type="secondary")
        cancel_edit = action_col2.form_submit_button("Annuller redigering", type="secondary")
    else:
        submitted = st.form_submit_button(save_button_label, type="secondary")
        cancel_edit = False

if cancel_edit:
    clear_edit_mode()
    st.rerun()

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

render_stats()
render_plots()
render_feedback()
render_rides_table(rides)
