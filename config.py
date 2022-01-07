"""
Appliation Configure Tools by Colinxu2020

Used Application:
    SVG Generator
    PyWallpaper(https://github.com/colinxu2020/pywallpaper)
Author:
    Colinxu2020
Version:2021.8.30
Last Update: 2021.8.30 21:37(UTC+8)
FilePath: /config.py
Version Change:
    2021.8.30: Add this docs string.
    2021.8.26: Create this file, Manymany change...
"""

import sys
from inspect import stack as call_stack
from os import sep as path_sep

import toml

from logger import logger

config_enable = None
__version__ = "20210830"
__author__ = ["Colinxu2020"]


def _get_module_name(name=None):
    for frameinfo in call_stack():
        filename = frameinfo.filename
        if not filename.endswith("config.py"):
            modulename = filename.replace(".py", "")
            try:
                modulename = path_sep.join(
                    modulename.split(path_sep)[
                        modulename.index(f"{path_sep}{name}{path_sep}") :
                    ]
                )
            except ValueError:
                modulename = modulename.split(path_sep)[-1]
            return modulename


def check_is_enable(name, module_name=None):
    if module_name is None:
        module_name = _get_module_name()
    config = get_config(name, check_enable=False)["enable_modules"]
    if not config.get(module_name, False):
        raise RuntimeError(
            f"This module {name}.{module_name} is been called but is not enable in config"
        )


def _parse_key(key):
    if "=" in key:
        return key.split("=")
    elif "no-" in key:
        return key[3:], "False"
    else:
        return key, "True"


def read_config_from_commandline():
    config = {}
    for arg in sys.argv[1:]:
        key, value = _parse_key(arg[2:])
        key = key.replace("-", "_")
        config[key] = value
    return config


def read_config_from_input(nargs):
    config = {}
    for n in nargs:
        config[n] = input(f'Please enter {n.replace("_", " ")}:')
    return config


def read_config_from_config_file(name):
    with open("config.toml") as fp:
        all_config = toml.load(fp)
        config = all_config[name]
    return config


def get_config(name, nargs=[], check_enable=True):
    global config_enable
    if check_enable and config_enable != True:
        try:
            check_is_enable("global", "config")
            config_enable = True
        finally:
            pass
    logger.info(f"Reading config from config.toml tab {name}")
    try:
        config = read_config_from_config_file(name)
    except (KeyError, FileNotFoundError):
        all_config = {}
        logger.info(
            "Because the configuration file does not exist, you are now running the configurator"
        )
        config = read_config_from_input(nargs)
        all_config[name] = config
        with open("config.toml", "w") as fp:
            toml.dump(all_config, fp)
        logger.info("You have successfully configured the application!")
    else:
        logger.info(
            f"If you need to return the configurator, remove the tab {name} in configuration file or delete the configuration file"
        )
    logger.debug("Reading config from commandline...")
    commandline_config = read_config_from_commandline()
    config |= commandline_config
    logger.debug("Done!")
    return config
