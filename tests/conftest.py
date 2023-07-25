import pytest
import json


@pytest.fixture(name="mock_entities")
def mock_entities():
    entities_json = """ [
    {
        "model": "person",
        "properties": [
            {
                "slug": "first_name",
                "type": "string",
                "value": "elise"
            },
            {
                "slug": "last_name",
                "type": "string",
                "value": "barnes"
            },
            {
                "slug": "age",
                "type": "integer",
                "value": 32
            },
            {
                "slug": "hair_color",
                "type": "string",
                "value": "grey"
            },
            {
                "slug": "eye_color",
                "type": "string",
                "value": "green"
            }
        ]
    },
    {
        "model": "vehicle",
        "properties": [
            {
                "slug": "make",
                "type": "string",
                "value": "toyota"
            },
            {
                "slug": "stolen",
                "type": "boolean",
                "value": false
            },
            {
                "slug": "impounded",
                "type": "boolean",
                "value": false
            },
            {
                "slug": "year",
                "type": "integer",
                "value": 2011
            }
        ]
    },
    {
        "model": "case",
        "properties": [
            {
                "slug": "incident_type",
                "type": "string",
                "value": "petty theft"
            },
            {
                "slug": "status",
                "type": "string",
                "value": "open"
            },
            {
                "slug": "city",
                "type": "string",
                "value": "fremont"
            },
            {
                "slug": "year",
                "type": "integer",
                "value": 2016
            }
        ]
    },
    {
        "model": "person",
        "properties": [
            {
                "slug": "first_name",
                "type": "string",
                "value": "george"
            },
            {
                "slug": "last_name",
                "type": "string",
                "value": "gray"
            },
            {
                "slug": "age",
                "type": "integer",
                "value": 22
            },
            {
                "slug": "hair_color",
                "type": "string",
                "value": "black"
            },
            {
                "slug": "eye_color",
                "type": "string",
                "value": "brown"
            }
        ]
    },
    {
        "model": "vehicle",
        "properties": [
            {
                "slug": "make",
                "type": "string",
                "value": "honda"
            },
            {
                "slug": "stolen",
                "type": "boolean",
                "value": false
            },
            {
                "slug": "impounded",
                "type": "boolean",
                "value": false
            },
            {
                "slug": "year",
                "type": "integer",
                "value": 2014
            }
        ]
    },
    {
        "model": "case",
        "properties": [
            {
                "slug": "incident_type",
                "type": "string",
                "value": "battery"
            },
            {
                "slug": "status",
                "type": "string",
                "value": "referred to da"
            },
            {
                "slug": "city",
                "type": "string",
                "value": "vallejo"
            },
            {
                "slug": "year",
                "type": "integer",
                "value": 1995
            }
        ]
    },
    {
        "model": "person",
        "properties": [
            {
                "slug": "first_name",
                "type": "string",
                "value": "sarah"
            },
            {
                "slug": "last_name",
                "type": "string",
                "value": "cravero"
            },
            {
                "slug": "age",
                "type": "integer",
                "value": 43
            },
            {
                "slug": "hair_color",
                "type": "string",
                "value": "brown"
            }
        ]
    },
    {
        "model": "vehicle",
        "properties": [
            {
                "slug": "make",
                "type": "string",
                "value": "chevrolet"
            },
            {
                "slug": "stolen",
                "type": "boolean",
                "value": true
            },
            {
                "slug": "impounded",
                "type": "boolean",
                "value": false
            },
            {
                "slug": "year",
                "type": "integer",
                "value": 1982
            }
        ]
    },
    {
        "model": "case",
        "properties": [
            {
                "slug": "incident_type",
                "type": "string",
                "value": "vehicle theft"
            },
            {
                "slug": "status",
                "type": "string",
                "value": "inactive"
            },
            {
                "slug": "city",
                "type": "string",
                "value": null
            },
            {
                "slug": "year",
                "type": "integer",
                "value": 2004
            }
        ]
    },
    {
        "model": "person",
        "properties": [
            {
                "slug": "first_name",
                "type": "string",
                "value": "victor"
            },
            {
                "slug": "last_name",
                "type": "string",
                "value": "hernandez"
            },
            {
                "slug": "age",
                "type": "integer",
                "value": 47
            },
            {
                "slug": "hair_color",
                "type": "string",
                "value": "green"
            },
            {
                "slug": "eye_color",
                "type": "string",
                "value": "green"
            }
        ]
    }
    ]
    """

    yield json.loads(entities_json)


@pytest.fixture
def expected_intersection():
    yield {
        "first_name": [("elise", 1)],
        "last_name": [("barnes", 1)],
        "age": [(32, 1)],
        "hair_color": [("grey", 1)],
        "eye_color": [("green", 1)],
    }
