from configparser import ConfigParser

from appdirs import user_config_dir


def load_config(name, container=None, default=True):
    """
    Load a configuration file and optionally merge it with another default configuration file

    Args:
        name(str): The name of the configuration file to load without any file extensions
        container(Optional[str]): An optional container for the configuration file
        default(Optional[bool or ConfigParser]): Merge with a default configuration file. Valid values are False for
            no default, True to use an installed default configuration file, or a ConfigParser instance to use as the
            default configuration

    Returns:
        ConfigParser
    """
    pass



