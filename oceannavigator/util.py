import os
import json
import oceannavigator
import re
import json
from oceannavigator import app

_config = None

def get_dataset_config(configFile = app.config['datasetConfig']):
    global _config
    if _config is None:
        cwd = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(cwd, configFile), 'r') as f:
            _config = json.load(f)

    return _config

def __get_dataset_attribute(dataset, key):
    return get_dataset_config()[dataset].get(key) if not None else ""

def get_datasets():
    config = get_dataset_config()

    # Only return "enabled" datasets
    return [key for key in config.keys() if config[key].get("enabled")]

def get_dataset_url(dataset):
    return __get_dataset_attribute(dataset, "url")

def get_dataset_climatology(dataset):
    return __get_dataset_attribute(dataset, "climatology")

def get_dataset_name(dataset):
    return __get_dataset_attribute(dataset, "name")

def get_dataset_help(dataset):
    return __get_dataset_attribute(dataset, "help")

def get_dataset_quantum(dataset):
    return __get_dataset_attribute(dataset, "quantum")

def get_dataset_attribution(dataset):
    # Strip any HTML from this
    try:
        return re.sub(
            r"<[^>]*>",
            "",
            get_dataset_config()[dataset].get("attribution")
        )
    except:
        return ""

def get_dataset_cache(dataset):
    cache = get_dataset_config()[dataset].get("cache")
    if cache is not None and isinstance(cache, str):
        cache = int(cache)

    return cache

def get_variables(dataset):
    variable_keys = get_dataset_config()[dataset]["variables"].keys()

    variables = []
    for key in variable_keys:
        is_hidden = get_dataset_config()[dataset]["variables"][key].get("hide")

        if is_hidden is None or is_hidden in ['false', 'False']:
            variables.append(key)
    return variables


def get_variable_name(dataset, variable):
    ds_vars = get_variables(dataset)

    key = variable.key.lower()
    if key in ds_vars:
        return get_dataset_config()[dataset]["variables"][key]["name"]
    elif variable.name is not None:
        return variable.name
    else:
        return str(variable.key).title()


def get_variable_unit(dataset, variable):
    ds_vars = get_variables(dataset)

    key = variable.key.lower()
    if key in ds_vars:
        return get_dataset_config()[dataset]["variables"][key]["unit"]
    elif variable.unit is not None:
        return variable.unit
    else:
        return "Unknown"


def get_variable_scale(dataset, variable):
    ds_vars = get_variables(dataset)

    key = variable.key.lower()
    if key in ds_vars:
        scale = get_dataset_config()[dataset]["variables"][key].get("scale")
        if scale is not None:
            return scale
    if variable.valid_min is not None and variable.valid_max is not None:
        return [variable.valid_min, variable.valid_max]

    return [0, 100]


def get_variable_scale_factor(dataset, variable):
    ds_vars = get_variables(dataset)

    key = variable.key.lower()
    if key in ds_vars:
        factor = get_dataset_config()[dataset]["variables"][key].get("scale_factor")
        if factor is not None:
            return factor

    return 1.0


def is_variable_hidden(dataset, variable):
    try:
        from_config = get_dataset_config()[dataset]["variables"][variable.key.lower()].get("hide")
    except KeyError:
        return True

    if from_config in ['true', 'True'] or from_config == True:
        return True

    return False
    