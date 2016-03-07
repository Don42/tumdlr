import logging
import os

import click
from requests import Session

from tumdlr.main import pass_context
from tumdlr.downloader import download
from tumdlr.scrapers import archives
from tumdlr.containers.archives import TumblrArchives
from tumdlr.containers.post import TumblrPhotoSet


# noinspection PyIncorrectDocstring,PyUnusedLocal
@click.command('download', short_help='Download posts from a Tumblr account')
@click.argument('URL')
@click.option('--images/--skip-images', help='Toggles the downloading of image posts', default=True, envvar='IMAGES')
@click.option('--videos/--skip-videos', help='Toggles the downloading of video posts', default=True, envvar='VIDEOS')
@pass_context
def cli(ctx, url, images, videos):
    """
    Download posts from a Tumblr account.
    """
    log = logging.getLogger('tumdlr.commands.downloader')
    log.info('Starting a new download session for %s', url)

    # Get our post information
    tumblr = TumblrArchives(archives.get(url))

    for post in tumblr.photos:
        progress_data = {
            'Post Date': post.post_date,
            'Tags': post.tags
        }

        if post.is_photo:
            photoset = TumblrPhotoSet(post.url)

            progress_data['Caption'] = photoset.caption

            session = Session()
            session.headers.update({'referer': photoset.url})

            for photo in photoset.photos:
                filepath = ctx.config['Tumdlr']['SavePath']
                if photoset.is_photoset:
                    filepath = os.path.join(filepath, photoset.caption)

                download(photo.url, filepath, progress_data, session)
