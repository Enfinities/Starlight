import json


def read_json(filename):
    """Read all data from a JSON file.

    :param filename: (str) the JSON file where the data is stored (ends with .json)
    :return: (dict) all the data that was in the JSON file
    """
    with open(filename, 'r') as file:
        json_data = json.load(file)

    return json_data


def edit_value(filename: str, user: str, field: str, new_value):
    """Edit a value for a particular user in the JSON file.

    Raises:
        ValueError: If the session name is not found in the JSON file.
    """
    with open(filename, 'r') as file:
        json_data = json.load(file)

    json_data[user][field] = new_value

    with open(filename, 'w') as file:
        json.dump(json_data, file, indent=4)
