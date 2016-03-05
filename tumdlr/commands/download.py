import logging

import click
from tumdlr.main import pass_context, Context


@click.command('download', short_help='Download posts from a Tumblr account')
@click.option('--images/--skip-images', help='Toggles the downloading of image posts', default=True, envvar='IMAGES')
@click.option('--videos/--skip-videos', help='Toggles the downloading of video posts', default=True, envvar='VIDEOS')
def cli(ctx, images, videos):
    """
    Download posts from a Tumblr account

    Args:
        ctx(Context)
        images(bool)
        videos(bool)
    """
    log = logging.getLogger('tumdlr.downloader')
