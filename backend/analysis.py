from typing import Dict, Any

import numpy as np
import pandas as pd


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
    distances = df["distance_km"].to_numpy(dtype=float)
    durations = df["duration_min"].to_numpy(dtype=float)
    speeds = df["avg_speed_kmh"].to_numpy(dtype=float)

    stats = {
        "total_distance": float(np.sum(distances)),
        "total_time_min": float(np.sum(durations)),
        "avg_speed": float(np.mean(speeds)),
        "num_rides": int(df.shape[0]),
        "longest_ride": float(np.max(distances)),
    }
    return stats
