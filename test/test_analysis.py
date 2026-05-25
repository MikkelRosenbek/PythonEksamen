import pandas as pd

from backend.analysis import calculate_stats


def test_calculate_stats_returns_zero_values_for_empty_dataframe():
    # Setup:
    # Vi opretter et tomt DataFrame med de samme kolonner som appen normalt arbejder med.
    #
    # Formål:
    # Funktionen skal ikke fejle på tomme data, men returnere sikre nulværdier,
    # så frontend og API stadig kan vise et gyldigt resultat.
    df = pd.DataFrame(
        columns=["id", "date", "ride_name", "distance_km", "duration_min", "avg_speed_kmh", "elevation_m"]
    )

    stats = calculate_stats(df)

    assert stats == {
        "total_distance": 0.0,
        "total_time_min": 0.0,
        "avg_speed": 0.0,
        "num_rides": 0,
        "longest_ride": 0.0,
    }


def test_calculate_stats_returns_expected_values():
    # Setup:
    # Vi laver to kendte ture med simple tal, så det er let at regne facit ud på forhånd.
    #
    # Formål:
    # Verificer at calculate_stats beregner sum, gennemsnit, antal og længste tur korrekt.
    df = pd.DataFrame(
        [
            {
                "id": 1,
                "date": "2026-05-01",
                "ride_name": "Tur 1",
                "distance_km": 20.0,
                "duration_min": 50.0,
                "avg_speed_kmh": 24.0,
                "elevation_m": 120.0,
            },
            {
                "id": 2,
                "date": "2026-05-02",
                "ride_name": "Tur 2",
                "distance_km": 40.0,
                "duration_min": 100.0,
                "avg_speed_kmh": 30.0,
                "elevation_m": 300.0,
            },
        ]
    )

    stats = calculate_stats(df)

    # Forventning:
    # 20 + 40 = 60 km
    # 50 + 100 = 150 min
    # (24 + 30) / 2 = 27 km/t
    # 2 ture
    # længste tur = 40 km
    assert stats["total_distance"] == 60.0
    assert stats["total_time_min"] == 150.0
    assert stats["avg_speed"] == 27.0
    assert stats["num_rides"] == 2
    assert stats["longest_ride"] == 40.0
