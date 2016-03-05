import logging

from tumdlr.containers.post import TumblrPost


class TumblrArchives:

    def __init__(self, pages=None):
        self.pages = []
        self.posts = []  # type: list[TumblrPost]

        self.photo_count    = 0
        self.video_count    = 0
        self.generic_count  = 0

        self.log = logging.getLogger('tumdlr.containers.archives')

        if pages:
            for page in pages:
                self.add_page(page)

    def add_page(self, page):
        """
        Add and parse an archive page

        Args:
            page(bs4.element.Tag): The page to add
        """
        self.log.debug('Adding page %d', len(self.pages) + 1)
        self.pages.append(page)

        posts = page.find_all('div', {'class': 'post'})
        for post in posts:
            self._parse_post(post)

    @property
    def photos(self):
        """
        Returns:
            list[TumblrPost]
        """
        self.log.debug('Fetching all photo posts')
        return [post for post in self.posts if post.is_photo]

    @property
    def videos(self):
        """
        Returns:
            list[TumblrPost]
        """
        self.log.debug('Fetching all video posts')
        return [post for post in self.posts if post.is_video]

    @property
    def generic(self):
        """
        Returns:
            list[TumblrPost]
        """
        self.log.debug('Fetching all generic posts')
        return [post for post in self.posts if post.is_generic]

    @property
    def post_count(self):
        """
        Returns:
            int
        """
        return self.generic_count + self.photo_count + self.video_count

    def _parse_post(self, post):
        """
        Parse a single archive post block

        Args:
            post(bs4.element.Tag): The posts div container
        """
        post = TumblrPost(post)
        self.posts.append(post)

        # Update post counts
        if post.is_photo:
            self.log.debug('Photo page parsed')
            self.photo_count += 1
        elif post.is_video:
            self.log.debug('Video page parsed')
            self.video_count += 1
        else:
            self.log.debug('Generic page parsed')
            self.generic_count += 1

