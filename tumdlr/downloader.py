import os
import re

import click
from requests import Session, Response
from humanize import naturalsize
from yurl import URL


filename_pattern = re.compile('/(tumblr_\w+\.[a-zA-Z0-9]{2,4})$')


def download(url, filepath, progress_data=None, session=None, silent=False):
    """
    Initiate a file download and display the progress

    Args:
        url(str):               Download URL
        filepath(str):          Filepath to save to
        progress_data(dict):    Static information to display above the progress bar
        session(Session):       An optional download session to use
        silent(bool):           Download the file, but don't print any output

    Returns:

    """
    # Set up our requests session and make sure the filepath exists
    session = session or Session()
    os.makedirs(filepath, 0o755, True)

    # Test the connection
    response = session.head(url, allow_redirects=True)  # type: Response
    response.raise_for_status()

    # Get some information about the file we are downloading
    final_url   = URL(response.url)
    filename    = filename_pattern.match(final_url).group(1)
    filesize    = naturalsize(response.headers.get('content-length', 0))
    filetype    = response.headers.get('content-type', 'Unknown')
    save_path   = os.path.join(filepath, filename)

    # Perform a few quick sanity checks
    if not filename:
        raise ValueError('Failed to parse a filename for the download request')

    # Format the information output
    info_lines = [
        click.style('Saving to: ', bold=True) + save_path,
        click.style('File type: ', bold=True) + filetype,
        click.style('File size: ', bold=True) + filesize
    ]

    if progress_data:
        for key, value in progress_data.items():
            info_lines.append('{key} {value}'.format(key=click.style(key + ':', bold=True), value=value))

    # Print the static information now
    for line in info_lines:
        click.echo(line)

    # Now let's make the real download request
    response = session.get(url, allow_redirects=True)  # type: Response

    # Process the download
    with open(save_path, 'wb') as file:
        length = int(response.headers.get('content-length'))

        with click.progressbar(response.iter_content(1024), length) as progress:
            for chunk in progress:
                if chunk:
                    file.write(chunk)
                    file.flush()
