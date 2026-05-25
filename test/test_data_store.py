from pathlib import Path
import shutil
import tempfile

import pytest

from backend import data_store


@pytest.fixture()
def temp_data_file(monkeypatch):
    # Testene må ikke røre projektets rigtige datafil.
    # Derfor peger vi midlertidigt data_store.DATA_FILE over på en ny CSV-fil
    # i en midlertidig mappe, som slettes efter hver test.
    temp_dir = Path(tempfile.mkdtemp(prefix="cycling-tests-"))
    temp_file = temp_dir / "myData.csv"
    monkeypatch.setattr(data_store, "DATA_FILE", temp_file)
    try:
        yield temp_file
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def test_load_data_returns_empty_dataframe_when_file_does_not_exist(temp_data_file):
    # Setup:
    # temp_data_file peger på en fil, der ikke findes endnu.
    #
    # Formål:
    # load_data skal stadig returnere et tomt DataFrame med de rigtige kolonner,
    # så resten af appen kan arbejde videre uden speciallogik.
    df = data_store.load_data()

    assert list(df.columns) == data_store.CSV_COLUMNS
    assert df.empty


def test_append_ride_assigns_incrementing_id_and_persists_file(temp_data_file):
    # Setup:
    # Vi opretter to ture uden id.
    #
    # Formål:
    # append_ride skal selv tildele løbende id'er og gemme data til den midlertidige CSV-fil.
    first_ride = {
        "date": "2026-05-10",
        "ride_name": "Morning Ride",
        "distance_km": 25.5,
        "duration_min": 60.0,
        "avg_speed_kmh": 25.5,
        "elevation_m": 100.0,
    }
    second_ride = {
        "date": "2026-05-11",
        "ride_name": "Evening Ride",
        "distance_km": 30.0,
        "duration_min": 75.0,
        "avg_speed_kmh": 24.0,
        "elevation_m": 180.0,
    }

    df_after_first = data_store.append_ride(first_ride)
    df_after_second = data_store.append_ride(second_ride)

    # Forventning:
    # Første tur får id 1.
    # Anden tur får id 2.
    # CSV-filen skal eksistere på disken efter skrivning.
    assert df_after_first.iloc[0]["id"] == 1
    assert list(df_after_second["id"]) == [1, 2]
    assert temp_data_file.exists()


def test_update_ride_changes_existing_row(temp_data_file):
    # Setup:
    # Vi opretter først én tur med id 1.
    #
    # Formål:
    # update_ride skal finde den eksisterende tur via id og erstatte dens værdier.
    data_store.append_ride(
        {
            "date": "2026-05-10",
            "ride_name": "Morning Ride",
            "distance_km": 25.5,
            "duration_min": 60.0,
            "avg_speed_kmh": 25.5,
            "elevation_m": 100.0,
        }
    )

    updated_df = data_store.update_ride(
        1,
        {
            "date": "2026-05-12",
            "ride_name": "Updated Ride",
            "distance_km": 40.0,
            "duration_min": 90.0,
            "avg_speed_kmh": 26.7,
            "elevation_m": 220.0,
        },
    )

    updated_row = updated_df.loc[updated_df["id"] == 1].iloc[0]

    # Forventning:
    # Den opdaterede række skal have de nye værdier og stadig beholde samme id.
    assert updated_row["ride_name"] == "Updated Ride"
    assert updated_row["distance_km"] == 40.0


def test_delete_ride_removes_row(temp_data_file):
    # Setup:
    # Vi opretter to ture, så vi kan slette den ene og kontrollere at den anden bliver bevaret.
    #
    # Formål:
    # delete_ride skal fjerne præcis den tur, der matcher det givne id.
    data_store.append_ride(
        {
            "date": "2026-05-10",
            "ride_name": "Ride 1",
            "distance_km": 20.0,
            "duration_min": 50.0,
            "avg_speed_kmh": 24.0,
            "elevation_m": 100.0,
        }
    )
    data_store.append_ride(
        {
            "date": "2026-05-11",
            "ride_name": "Ride 2",
            "distance_km": 30.0,
            "duration_min": 70.0,
            "avg_speed_kmh": 25.7,
            "elevation_m": 150.0,
        }
    )

    updated_df = data_store.delete_ride(1)

    # Forventning:
    # Kun id 2 skal være tilbage efter sletning af id 1.
    assert list(updated_df["id"]) == [2]


def test_delete_ride_raises_error_for_missing_id(temp_data_file):
    # Formål:
    # Hvis man prøver at slette et id, der ikke findes i datasættet,
    # skal datalaget give en tydelig ValueError i stedet for at fejle lydløst.
    with pytest.raises(ValueError):
        data_store.delete_ride(999)
