import os
import re
from configparser import ConfigParser

from tumdlr import DATA_DIR, USER_CONFIG_DIR, SITE_CONFIG_DIR


def load_config(name, container=None, default=True):
    """
    Load a configuration file and optionally merge it with another default configuration file

    Args:
        name(str): The name of the configuration file to load without any file extensions
        container(Optional[str]): An optional container for the configuration file
        default(Optional[bool or str]): Merge with a default configuration file. Valid values are False for
            no default, True to use an installed default configuration file, or a path to a config file to use as the
            default configuration

    Returns:
        ConfigParser
    """
    paths = []

    def slugify(string):
        """
        Convert a string to a safe format for file/dir names

        Args:
            string(str)

        Returns:
            str
        """
        string = string.lower().strip()
        string = re.sub('[^\w\s]', '', string)  # Strip non-word characters
        string = re.sub('\s+', '_', string)  # Replace space characters with underscores

        return string

    filename = slugify(name) + '.cfg'
    if container:
        filename = os.path.join(slugify(container), filename)

    # Load the default configuration (if enabled)
    if default:
        paths.append(os.path.join(DATA_DIR, 'config', filename) if default is True else default)

    # Load the site configuration first, then the user configuration
    paths.append(os.path.join(SITE_CONFIG_DIR, filename))
    paths.append(os.path.join(USER_CONFIG_DIR, filename))

    config = ConfigParser()
    config.read(paths)

    return config
