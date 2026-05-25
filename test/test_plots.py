import pandas as pd

from backend.plots import plot_avg_speed_over_time, plot_distance_over_time


def test_plot_distance_over_time_returns_png_bytes_for_empty_dataframe():
    # Setup:
    # Vi sender et tomt DataFrame med de kolonner plotfunktionen forventer.
    #
    # Formål:
    # Plotfunktionen skal stadig kunne lave et billede, selv når der ikke er ture endnu.
    df = pd.DataFrame(columns=["date", "distance_km", "avg_speed_kmh"])

    image_bytes = plot_distance_over_time(df)

    # Forventning:
    # Returnerede bytes skal starte med PNG-signaturen.
    assert image_bytes.startswith(b"\x89PNG")


def test_plot_avg_speed_over_time_returns_png_bytes_for_dataframe_with_data():
    # Setup:
    # Vi opretter et lille datasæt med to ture og deres gennemsnitshastighed.
    #
    # Formål:
    # Plotfunktionen skal returnere et rigtigt PNG-billede, som frontend kan vise direkte.
    df = pd.DataFrame(
        [
            {"date": pd.Timestamp("2026-05-10"), "distance_km": 20.0, "avg_speed_kmh": 24.0},
            {"date": pd.Timestamp("2026-05-11"), "distance_km": 30.0, "avg_speed_kmh": 26.0},
        ]
    )

    image_bytes = plot_avg_speed_over_time(df)

    # Forventning:
    # Returnerede bytes skal starte med PNG-signaturen.
    assert image_bytes.startswith(b"\x89PNG")
