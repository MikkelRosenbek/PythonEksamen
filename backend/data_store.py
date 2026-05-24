from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "myData.csv"
CSV_COLUMNS = [
    "id",
    "date",
    "ride_name",
    "distance_km",
    "duration_min",
    "avg_speed_kmh",
    "elevation_m",
]


def _next_id(df: pd.DataFrame) -> int:
    if df.empty or "id" not in df.columns or df["id"].dropna().empty:
        return 1
    return int(df["id"].max()) + 1


def _ensure_schema(df: pd.DataFrame) -> pd.DataFrame:
    normalized_df = df.copy()

    if "id" not in normalized_df.columns:
        normalized_df.insert(0, "id", range(1, len(normalized_df) + 1))
    normalized_df["id"] = pd.to_numeric(normalized_df["id"], errors="coerce")

    missing_id_mask = normalized_df["id"].isna()
    if missing_id_mask.any():
        next_id = _next_id(normalized_df.loc[~missing_id_mask])
        for row_index in normalized_df.index[missing_id_mask]:
            normalized_df.at[row_index, "id"] = next_id
            next_id += 1

    normalized_df["id"] = normalized_df["id"].astype(int)

    if "ride_name" not in normalized_df.columns:
        normalized_df.insert(2, "ride_name", "")

    for row in normalized_df.itertuples():
        if not getattr(row, "ride_name") or pd.isna(getattr(row, "ride_name")):
            normalized_df.at[row.Index, "ride_name"] = f"Tur {getattr(row, 'id')}"

    for column in CSV_COLUMNS:
        if column not in normalized_df.columns:
            normalized_df[column] = 0 if column != "ride_name" else ""

    normalized_df["date"] = pd.to_datetime(normalized_df["date"])
    return normalized_df[CSV_COLUMNS].sort_values("date").reset_index(drop=True)


def load_data() -> pd.DataFrame:
    # Brug en tom DataFrame med kendte kolonner, hvis datafilen endnu ikke findes.
    if not DATA_FILE.exists():
        return pd.DataFrame(columns=CSV_COLUMNS)

    df = pd.read_csv(DATA_FILE, parse_dates=["date"])
    normalized_df = _ensure_schema(df)

    # Gem automatisk, hvis den eksisterende CSV mangler nye kolonner eller orden.
    if list(df.columns) != CSV_COLUMNS:
        save_data(normalized_df)

    return normalized_df


def save_data(df: pd.DataFrame) -> None:
    # Gem data i en stabil kolonnerækkefølge og med datoformat, der er let at læse.
    df_to_save = _ensure_schema(df)
    df_to_save["date"] = pd.to_datetime(df_to_save["date"]).dt.strftime("%Y-%m-%d")
    df_to_save.to_csv(DATA_FILE, index=False)


def append_ride(ride: dict[str, Any]) -> pd.DataFrame:
    # Tildel næste løbenummer og tilføj turen til CSV-filen.
    df = load_data()
    new_ride = ride.copy()
    new_ride["id"] = _next_id(df)
    new_row = pd.DataFrame([new_ride], columns=CSV_COLUMNS)
    new_row["date"] = pd.to_datetime(new_row["date"])
    updated_df = pd.concat([df, new_row], ignore_index=True)
    save_data(updated_df)
    return load_data()


def update_ride(ride_id: int, ride: dict[str, Any]) -> pd.DataFrame:
    df = load_data()
    mask = df["id"] == ride_id
    if not mask.any():
        raise ValueError(f"Ride with id {ride_id} was not found.")

    for key, value in ride.items():
        df.loc[mask, key] = value

    df.loc[mask, "id"] = ride_id
    df.loc[mask, "date"] = pd.to_datetime(df.loc[mask, "date"])
    save_data(df)
    return load_data()


def delete_ride(ride_id: int) -> pd.DataFrame:
    df = load_data()
    filtered_df = df.loc[df["id"] != ride_id].reset_index(drop=True)
    if len(filtered_df) == len(df):
        raise ValueError(f"Ride with id {ride_id} was not found.")

    save_data(filtered_df)
    return load_data()
