import argparse
import ijson
import pprint
from collections import defaultdict
from typing import Dict, List, Tuple, Any, Union, Literal, Iterator


Aggregation = Tuple[str, int]
TypeStr = Literal["string", "integer", "boolean"]
ValueType = Union[int, str, bool, None]


def json_generator(filename, field="item"):
    """
    Yields json array data entities
    """
    with open(filename, "r", encoding="utf-8") as file:
        for entity in ijson.items(file, field):
            yield entity


# private
def _str_to_type(value: ValueType, type_str: TypeStr):
    """
    Converts a given value to a new type, as specified by a string input.
    Supported type strings are "integer", "boolean", and "string".

    :param value: the value to be converted
    :param typ_str: A string indicating the type to which the value should be converted.

    :return: The input value converted to the requested type. If the input value is None,
             then None is returned without any conversion.

    :raises KeyError: If the type_str is not one of the supported types.
    :raises ValueError: If the value can't be converted to the desired type.

    """
    if value is None:
        return value

    type_dict = {"integer": int, "boolean": bool, "string": str}
    return type_dict[type_str](value)


def _flatten_data(data: Iterator[dict]) -> Iterator[dict]:
    """
    Lazily flattens entity properities

    :param data: List of data entities
    :return: List of data entites with flattened properties
    """

    def process(row):
        property_obj = {
            prop["slug"]: _str_to_type(prop["value"], prop["type"])
            for prop in row["properties"]
        }
        return {"model": row["model"], "properties": property_obj}

    flattened = map(process, data)

    return flattened


def _filter_data(
    data: Iterator[dict], models: List[str], properties: dict
) -> List[Dict[str, Any]]:
    """
    Filter the data based on specified models and properties.

    :param data: list of data entities to biltered
    :param models: The list of models to match against.
    :param properties: The properties to match against.

    :return: The filtered data, containing dictionaries of entities that match the specified
    models and properties.

    """

    filtered_data = filter(
        lambda entity: _match_model(entity, models)
        and _match_properties(entity, properties),
        data,
    )

    return filtered_data


def _match_model(entity: Dict[str, Any], models: List[str]) -> bool:
    """
    Checks if data entity matches model

    :param entity: data entity
    :param models: models to match (Union)

    :return: returns true if entity matches any of the models provided
    """
    return not models or entity.get("model") in models


def _match_properties(entity: Dict[str, Any], properties: Dict[str, List[str]]) -> bool:
    """
    Check if the entity matches the specified properties. Multiple key/value paris are treated
    as AND (intersection)

    :param entity: data entity
    :param properties: properties dictionary containing the key value pairs

    :return: True if matched
    """
    for key, values in properties.items():
        if str(entity["properties"].get(key)) not in values:
            return False
    return True


def _aggregate_data(data: Iterator[dict]) -> Dict[str, Aggregation]:
    """
    Aggregates the data contained within the 'properties' key of each dictionary
    in the provided list. The aggregation involves counting the occurrences
    of each unique property and its corresponding value.

    :param data: List of data entities

    :return: Dictionary containing aggregated data. Lists are sorted
    in descending order
    """
    aggregated_data = defaultdict(lambda: defaultdict(int))

    for row in data:
        for key, value in row.get("properties", {}).items():
            aggregated_data[key][value] += 1

    # sort
    sorted_data = {
        key: sorted(list(value_counts.items()), key=lambda x: x[1], reverse=True)
        for key, value_counts in aggregated_data.items()
    }

    return sorted_data


# public
def run(
    data_gen: Iterator[dict], models: List[str], properties: List[str]
) -> Dict[str, List[Aggregation]]:
    """
    Takes a list of entity objects, filters data matching the `models` and `properties`
    specifications and then aggregates the data returning a sorted list of aggregations.

    :param data: The list entity data
    :param models: A list of models to filter the aggregation on
    :param properties: A list of property keys and values to filter the aggregation on. Format:
        key:value1,value2
    """

    # Parse properties to a dictionary
    prop_dict = {}
    for prop in properties:
        key, values = prop.split(":")
        prop_dict[key] = values.split(",")

    # Filter data by models and properties
    flattened = _flatten_data(data_gen)
    filtered = _filter_data(flattened, models, prop_dict)

    result = _aggregate_data(filtered)
    return result


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

    d = json_generator(args.input_file)

    pprint.pprint(run(d, args.models, args.properties))
