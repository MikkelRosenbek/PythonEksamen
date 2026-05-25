from __future__ import annotations
import os
from typing import Any
import pandas as pd
import requests


OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
OLLAMA_TIMEOUT_SECONDS = int(os.getenv("OLLAMA_TIMEOUT_SECONDS", "60"))
FALLBACK_MESSAGE = (
    "AI-feedback er midlertidigt utilgængeligt. "
    "Sørg for at Ollama kører lokalt og at den valgte model er installeret."
)


def _format_recent_rides(rides_df: pd.DataFrame, limit: int = 5) -> str:
    if rides_df.empty:
        return "Ingen registrerede ture endnu."

    recent_rides = rides_df.sort_values("date", ascending=False).head(limit)
    lines: list[str] = []
    for ride in recent_rides.itertuples():
        ride_date = pd.to_datetime(ride.date).strftime("%Y-%m-%d")
        lines.append(
            f"- {ride_date}: {ride.ride_name}, {ride.distance_km:.2f} km, "
            f"{ride.duration_min:.0f} min, {ride.avg_speed_kmh:.1f} km/t, "
            f"{ride.elevation_m:.0f} hm"
        )
    return "\n".join(lines)


def build_prompt(stats: dict[str, Any], rides_df: pd.DataFrame) -> str:
    recent_rides = _format_recent_rides(rides_df)
    return f"""
    You are an AI cycling coach.

    Use the training data below to give the user short and easy-to-understand feedback.
    Write in clear English.
    Keep the answer short, practical, and specific.
    Do not invent facts that are not supported by the data.

    Structure:
    1. A short summary of the training
    2. What looks good
    3. One concrete suggestion for the next training session

    Training statistics:
    - Number of rides: {stats['num_rides']}
    - Total distance: {stats['total_distance']:.2f} km
    - Total time: {stats['total_time_min']:.0f} min
    - Average speed: {stats['avg_speed']:.1f} km/h
    - Longest ride: {stats['longest_ride']:.2f} km

    Recent rides:
    {recent_rides}
    """.strip()


def call_ollama(prompt: str) -> str:
    response = requests.post(
        OLLAMA_API_URL,
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
        },
        timeout=OLLAMA_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    data = response.json()

    if "response" not in data or not data["response"]:
        raise ValueError("Ollama returnerede ikke et gyldigt svar.")

    return str(data["response"]).strip()


def get_llm_feedback(stats: dict[str, Any], rides_df: pd.DataFrame) -> str:
    if stats["num_rides"] == 0:
        return "Der er endnu ikke nok data til at give AI-feedback. Registrer mindst en tur."

    prompt = build_prompt(stats, rides_df)
    try:
        return call_ollama(prompt)
    except (requests.RequestException, ValueError):
        return FALLBACK_MESSAGE
