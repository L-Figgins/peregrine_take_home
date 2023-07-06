import argparse
import json
import pprint
from collections import defaultdict
from typing import Dict, List, Tuple

Aggregation = Tuple[str, int]


def str_to_type(value, type_str):
    type_dict = {"integer": int, "boolean": bool, "string": str}

    return type_dict[type_str](value)


def normalize_data(data: List[dict]):
    table = []

    for row in data:
        property_obj = {}
        for prop in row["properties"]:
            property_obj[prop["slug"]] = (
                str_to_type(prop["value"], prop["type"])
                if prop["value"] is not None
                else None
            )
        table.append({"model": row["model"], "properties": property_obj})

    return table


def filter_data(data, models: list, properties: dict):
    filtered_data = []
    for entity in data:
        # Filter by model
        if not models or entity.get("model") in models:
            # Filter by properties
            include = True
            for key, values in properties.items():
                if not str(entity["properties"].get(key)) in values:
                    include = False
                    break
            if include:
                filtered_data.append(entity)
    return filtered_data


def aggregate_data(data: List[dict]):
    aggregate_data = defaultdict(lambda: defaultdict(int))

    for row in data:
        for k, v in row["properties"].items():
            aggregate_data[k][v] += 1

    # sort
    sorted_data = {}

    for k, value_counts in aggregate_data.items():
        sorted_data[k] = sorted(
            [(value, count) for value, count in value_counts.items()],
            key=lambda x: x[1],
            reverse=True,
        )

    return sorted_data


def run(
    data: List[dict], models: List[str], properties: List[str]
) -> Dict[str, List[Aggregation]]:
    """
    Takes a list of entity objects, filters data matching the `models` and `properties` specifications,
    and then aggregates the data returning a sorted list of aggregations.

    :param data: The list entity data
    :param models: A list of models to filter the aggregation on
    :param properties: A list of property keys and values to filter the aggregation on. Format:
        key:value1,value2
    """

    normalized = normalize_data(data)
    # Parse properties to a dictionary
    prop_dict = {}

    for prop in properties:
        key, values = prop.split(":")
        prop_dict[key] = values.split(",")

    # Filter data by models and properties
    filtered = filter_data(normalized, models, prop_dict)

    agg = aggregate_data(filtered)
    return agg


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # support `extend` action for python versions less than 3.8
    class ExtendAction(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            items = getattr(namespace, self.dest) or []
            items.extend(values)
            setattr(namespace, self.dest, items)

    parser.register("action", "extend", ExtendAction)
    parser.add_argument(
        "-i",
        "--input-file",
        default="entities.json",
        help="The data file to be processed.",
    )
    parser.add_argument(
        "-m",
        "--models",
        # stores a list, and extends each argument value to the list
        action="extend",
        default=list(),
        nargs="*",
        help="Model(s) to include.",
    )
    parser.add_argument(
        "-p",
        "--properties",
        # stores a list, and extends each argument value to the list
        action="extend",
        default=list(),
        nargs="*",
        help="""
        Properties to filter on.
        Assumes no key has ':' or ' ' and no property has ','. Format key:value1,value2
        """,
    )
    args = parser.parse_args()

    with open(args.input_file, "r") as f:
        data = json.load(f)

    pprint.pprint(run(data, args.models, args.properties))
