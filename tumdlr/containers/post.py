import logging

import requests
from bs4 import BeautifulSoup


class TumblrPost:

    TYPE_GENERIC = 'Generic'
    TYPE_PHOTO   = 'Photo'
    TYPE_VIDEO   = 'Video'

    def __init__(self, container):
        """
        Args:
            container(bs4.element.Tag): Post container
        """
        self.container = container
        self.log = logging.getLogger('tumdlr.containers.post')

        self.type       = self.TYPE_GENERIC
        self.post_date  = None
        self.tags       = set()
        self.notes      = 0
        self.url        = None

        self._classes = []
        self._parse_container()

    @property
    def is_generic(self):
        """
        Returns:
            bool
        """
        return self.type == self.TYPE_GENERIC

    @property
    def is_photo(self):
        """
        Returns:
            bool
        """
        return self.type == self.TYPE_PHOTO

    @property
    def is_video(self):
        """
        Returns:
            bool
        """
        return self.type == self.TYPE_VIDEO

    def _parse_container(self):
        self._classes = self.container.get('class')

        # Register the post type
        if 'is_video' in self._classes:
            self.type = self.TYPE_VIDEO
        elif 'is_photo' in self._classes:
            self.type = self.TYPE_PHOTO

        # Post date
        try:
            self.post_date = self.container.find('span', {'class': 'post_date'}).text
        except AttributeError:
            self.log.warn('No post date could be matched')

        # Tags
        try:
            tags_str  = self.container.find('span', {'class': 'tags'}).text.strip()  # type: str
            if tags_str:
                self.tags = {tag.strip()[1:] for tag in tags_str.split()}
        except AttributeError:
            self.log.info('No tags could be matched')

        # Notes
        notes_count = None
        try:
            notes_count = self.container.find('span', {'class': 'post_notes'}).get('data-notes')
            self.notes  = int(notes_count)
        except ValueError:
            self.log.warn('Invalid notes count value: %s', notes_count)
        except AttributeError:
            self.log.warn('No notes could be matched')

        # Page URL
        self.url = self.container.find('a').get('href')

    def __repr__(self):
        return "<TumblrPost type='{type}' post_date='{date}' url='{url}'>"\
            .format(type=self.type, date=self.post_date, url=self.url)

    def __str__(self):
        return self.url or ''


class TumblrPhotoSet:

    def __init__(self, url):
        """
        Args:
            url(str):   Link to the Tumblr photo post
        """
        self._photos = []
        self._loaded = False

        self.url  = url
        self._soup = None  # type: BeautifulSoup

        self._photoset_url  = None
        self._photoset_soup = None  # type: BeautifulSoup

        self._single_url    = None
        self._single_soup   = None  # type: BeautifulSoup

        self.post_date = None
        self.caption   = None

        self.session = requests.Session()
        self.session.headers.update({'referer': self.url})

        self.log = logging.getLogger('tumdlr.containers.post')

    def _load(self):
        """
        Load everything
        """
        self._download_post_page()
        self._download_photos_page()
        self._parse_photos()

        self._loaded = True

    def _download_post_page(self):
        """
        (Re-)download the post page
        """
        request = requests.get(self.url)
        request.raise_for_status()

        soup = BeautifulSoup(request.content, 'lxml')
        self._soup = soup.find('div', {'class': 'post'})

        # Post date
        try:
            self.post_date = soup.find('div', {'class': 'date'}).text.strip()
        except AttributeError:
            self.log.info('No post date could be matched')

        # Caption
        try:
            self.caption = soup.find('meta', {'property': 'og:description'}).get('content')
        except AttributeError:
            self.log.info('No caption could be matched')

    def _download_photos_page(self):
        """
        Determine whether or not this is a single image post or a multi-photo set
        """
        # Do we have a photoset?
        try:
            self._photoset_url = self._soup.find('iframe', {'class': 'photoset'}).get('src')

            photoset_request = requests.get(self._photoset_url)
            photoset_request.raise_for_status()

            self._photoset_soup = BeautifulSoup(photoset_request.content, 'lxml')
        except AttributeError:
            self.log.debug('No photoset URL available')

        # Nope, should just have a single image
        self._single_url = self._soup.find('a').get('href')

        single_request = requests.get(self._single_url)
        single_request.raise_for_status()

        self._single_soup = BeautifulSoup(single_request.content, 'lxml')

    def _parse_photos(self):
        # Are we parsing a single photo?
        if self.is_single:
            src = self._single_soup.find('img', {'id': 'content-image'}).get('data-src')
            self._photos.append(TumblrPhoto(src, self))
            return

        photos = self._photoset_soup.find('div', {'class': 'photoset'}).find_all('a', {'class': 'photoset_photo'})
        for photo in photos:
            self._photos.append(TumblrPhoto(photo.get('href'), self))

    @property
    def photos(self):
        """
        Lazily loaded photos

        Returns:
            list[TumblrPhoto]
        """
        if not self._loaded:
            self._load()

        return self._photos

    @property
    def first(self):
        """
        Fetch the first photo in a photoset (or the only photo in a single)

        Returns:
            TumblrPhoto or None
        """
        return self._photos[-1] if self._photos else None

    @property
    def is_single(self):
        """
        Returns:
            bool
        """
        return self._photoset_url is None

    @property
    def is_photoset(self):
        """
        Returns:
            bool
        """
        return self._photoset_url is not None

    def __repr__(self):
        if not self._loaded:
            self._load()

        return "<TumblrPhotoSet count='{count}' caption='{desc}'>".format(count=len(self._photos), desc=self.caption)

    def __str__(self):
        return self.url


class TumblrPhoto:

    def __init__(self, url, photoset):
        """
        Args:
            url(str):                   Photoset / preview URL
            photoset(TumblrPhotoSet):   Parent container object
        """
        self.url = url
        self.photoset = photoset

    def __repr__(self):
        return "<TumblrPhoto url='{url}'>".format(url=self.url)

    def __str__(self):
        return self.url
