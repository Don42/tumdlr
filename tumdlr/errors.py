class TumdlrException(Exception):
    pass


###############################
# Begin file container errors #
###############################
class TumblrFileError(TumdlrException):
    pass


class TumblrDownloadError(TumblrFileError):
    def __init__(self, *args, **kwargs):
        self.download_url   = kwargs.get('download_url')
        self.error_message  = kwargs.get('error_message')
        super().__init__('An error occurred while downloading a file entry from a post')
