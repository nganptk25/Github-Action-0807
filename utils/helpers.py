import json


def load_config_data(file_path):
    with open(file_path) as f:
        return json.load(f)


def parametrize_generator(config_file_path, *keys):
    """
    Generates a list of tuples for parameterized tests based on keys from a JSON config file.

    :param keys_string: Comma-separated string of keys to extract from the config.
    :param config_file_path: Path to the JSON configuration file.
    :return: List of tuples containing the key and its corresponding value.
    """
    config_data = load_config_data(config_file_path)
    value_keys = keys[1:]
    keys_string = ", ".join(keys)
    values_list = []
    for key, values in config_data.items():
        if all([value_name in values for value_name in value_keys]):
            values_list.append(
                (key, *[values[value_name] for value_name in value_keys])
            )

    return keys_string, values_list
