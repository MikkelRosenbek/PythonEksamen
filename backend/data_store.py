from __future__ import annotations

from pathlib import Path

import pandas as pd


DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "myData.csv"
CSV_COLUMNS = ["date", "distance_km", "duration_min", "avg_speed_kmh", "elevation_m"]


def load_data() -> pd.DataFrame:
    # Brug en tom DataFrame med kendte kolonner, hvis datafilen endnu ikke findes.
    if not DATA_FILE.exists():
        return pd.DataFrame(columns=CSV_COLUMNS)
    return pd.read_csv(DATA_FILE, parse_dates=["date"])


def save_data(df: pd.DataFrame) -> None:
    # Gem datoer i et stabilt CSV-format, så filen er læsbar og konsistent.
    df_to_save = df.copy()
    if "date" in df_to_save.columns:
        df_to_save["date"] = pd.to_datetime(df_to_save["date"]).dt.strftime("%Y-%m-%d")
    df_to_save.to_csv(DATA_FILE, index=False)


def append_ride(ride: dict) -> pd.DataFrame:
    # Tilføj en ny tur, sorter på dato og skriv hele datasættet tilbage til CSV.
    df = load_data()
    new_row = pd.DataFrame([ride], columns=CSV_COLUMNS)
    new_row["date"] = pd.to_datetime(new_row["date"])
    updated_df = pd.concat([df, new_row], ignore_index=True)
    updated_df = updated_df.sort_values("date").reset_index(drop=True)
    save_data(updated_df)
    return updated_df
