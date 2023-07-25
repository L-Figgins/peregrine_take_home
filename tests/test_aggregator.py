import pytest
import json
from aggregator import run


def _save_test_artifact(filename: str, data: dict) -> None:
    """
    Helper function to save json test artifacts

    :param filename: name of file to save
    :param data: a jsonable python dictionary
    """
    with open(f"./test_artifacts/{filename}", "w+") as file:
        json.dump(data, file, indent=2)


def test_aggregate_model(
    mock_entities,
):
    aggregated_person_model = run(mock_entities, ["person"], [])
    _save_test_artifact("aggregated_person.json", data=aggregated_person_model)

    aggregated_vehicle_model = run(mock_entities, ["vehicle"], [])
    _save_test_artifact("aggregated_vehicle.json", data=aggregated_vehicle_model)

    aggregated_case_model = run(mock_entities, ["case"], [])
    _save_test_artifact("aggregated_case.json", data=aggregated_case_model)

    assert aggregated_person_model == {
        "first_name": [("elise", 1), ("george", 1), ("sarah", 1), ("victor", 1)],
        "last_name": [("barnes", 1), ("gray", 1), ("cravero", 1), ("hernandez", 1)],
        "age": [(32, 1), (22, 1), (43, 1), (47, 1)],
        "hair_color": [("grey", 1), ("black", 1), ("brown", 1), ("green", 1)],
        "eye_color": [("green", 2), ("brown", 1)],
    }
    assert aggregated_vehicle_model == {
        "make": [("toyota", 1), ("honda", 1), ("chevrolet", 1)],
        "stolen": [(False, 2), (True, 1)],
        "impounded": [(False, 3)],
        "year": [(2011, 1), (2014, 1), (1982, 1)],
    }
    assert aggregated_case_model == {
        "incident_type": [("petty theft", 1), ("battery", 1), ("vehicle theft", 1)],
        "status": [("open", 1), ("referred to da", 1), ("inactive", 1)],
        "city": [("fremont", 1), ("vallejo", 1), (None, 1)],
        "year": [(2016, 1), (1995, 1), (2004, 1)],
    }


def test_aggregate_properties(mock_entities):
    aggregated = run(mock_entities, [], ["year:2011"])
    _save_test_artifact("aggregated_year_properties.json", data=aggregated)
    assert aggregated == {
        "make": [("toyota", 1)],
        "stolen": [(False, 1)],
        "impounded": [(False, 1)],
        "year": [(2011, 1)],
    }


def test_aggregate_properties_union(mock_entities):
    aggregated = run(mock_entities, [], ["year:2011,2004"])
    _save_test_artifact("aggregated_year_properties_union.json", data=aggregated)
    assert aggregated == {
        "make": [("toyota", 1)],
        "stolen": [(False, 1)],
        "impounded": [(False, 1)],
        "year": [(2011, 1), (2004, 1)],
        "incident_type": [("vehicle theft", 1)],
        "status": [("inactive", 1)],
        "city": [(None, 1)],
    }


def test_aggregate_properties_intersect(mock_entities, expected_intersection):
    aggregated = run(mock_entities, [], ["first_name:elise", "hair_color:grey"])
    _save_test_artifact("aggregated_properties_intersect.json", data=aggregated)
    assert aggregated == expected_intersection


def test_aggregate_properties_intersect_w_model(mock_entities, expected_intersection):
    aggregated = run(mock_entities, ["person"], ["first_name:elise", "hair_color:grey"])
    _save_test_artifact("aggregated_properties_intersect.json", data=aggregated)
    assert aggregated == expected_intersection
