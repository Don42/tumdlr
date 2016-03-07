import logging
import random
from time import sleep

import requests
from bs4 import BeautifulSoup
from yurl import URL


def get(url):
    """
    Scrape archive links and associated metadata

    Args:
        url(str): The Tumblr profile URL

    Returns:
        list[BeautifulSoup]
    """
    log = logging.getLogger('tumdlr.scrapers.archives')

    raw_url     = URL(url)
    archive_url = URL(scheme='http', host=raw_url.host, path='/archive')
    log.info('Archive page parsed: %s', archive_url)

    # Download the first archive page
    pages = []
    first_page = requests.get(archive_url.as_string())
    first_page.raise_for_status()
    pages.append(BeautifulSoup(first_page.content, 'lxml'))
    log.info('First page downloaded')

    session = requests.Session()
    session.headers.update({'referer': archive_url.as_string()})

    # Do we have another page?
    while True:
        try:
            # Get the link to the next page, this is probably a relative URL so we need to parse it
            log.debug('Checking whether or not the next archive page exists')
            next_page_href = URL(pages[-1].find('a', id='next_page_link').get('href'))
            next_page_url  = URL(scheme='http', host=archive_url.host, path=next_page_href.path,
                                 query=next_page_href.query)
            log.debug('Next archive page found: %s [%r]', next_page_href, next_page_url)

            next_page = session.get(next_page_url.as_string())
            next_page.raise_for_status()

            pages.append(BeautifulSoup(next_page.content, 'lxml'))
            log.info('Page %d loaded', len(pages))

        except AttributeError:
            # Normal exception, no more pages to process
            log.info('No more archive pages left to process')
            break
        except requests.exceptions.HTTPError:
            # An HTTP error occurred, maybe we've been blocked?
            log.exception('A HTTP error occurred trying to fetch the next archive page')
            break

        wait = random.uniform(0.1, 0.5)
        log.debug('Pausing for %f seconds', wait)
        sleep(wait)

    return pages
