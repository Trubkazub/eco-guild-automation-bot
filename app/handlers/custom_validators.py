from urllib.parse import urlparse


class VK_link_validator:
    def __init__(self, url):
        if 'http' not in url:
            self.url = 'https://' + url
        else:
            self.url = url

    def validate_url(self):
        if 'vk.com' not in self.url:
            raise VkLinkException
        result = urlparse(self.url)
        if result.scheme and result.netloc:
            pass
        else:
            raise VkLinkException



class VkLinkException(Exception):
    pass
