import pandas as pd
from typing import Dict, Any


def calculate_stats(df: pd.DataFrame) -> Dict[str, Any]:
    # Returner nulværdier, så frontend og API ikke fejler på en tom CSV.
    if df.empty:
        return {
            "total_distance": 0.0,
            "total_time_min": 0.0,
            "avg_speed": 0.0,
            "num_rides": 0,
            "longest_ride": 0.0,
        }

    # Beregn de centrale nøgletal, som vises i frontend og bruges af LLM-feedback.
    stats = {
        "total_distance": float(df["distance_km"].sum()),
        "total_time_min": float(df["duration_min"].sum()),
        "avg_speed": float(df["avg_speed_kmh"].mean()),
        "num_rides": int(df.shape[0]),
        "longest_ride": float(df["distance_km"].max()),
    }
    return stats
