import re
from html import unescape


def unhtmlify(html):
    """
    Remove html-tags and unescape encoded html-entities.

    :param html: Evil-string containing html
    :return:
    """
    return unescape(re.sub(r'\s*<.*?>\s*', ' ', html))


class Item:
    """
    Entity to construct items-dict.
    """

    def __init__(self, html, url):
        """
        Construct item for items-dict.

        :param html: May contain html, which is also converted to plain text
        :param url: URL to next step in the discussion
        """
        self.url = url if url != '' else None
        self.html = html
        self.text = unhtmlify(self.html)

    def __json__(self, _request):
        """
        Convert entity to JSON.

        :param _request: Request
        :return:
        """
        return {
            'html': self.html,
            'text': self.text,
            'url': self.url
        }


class Bubble:
    """
    Converted bubble which is returned by the API.
    """

    @staticmethod
    def __demultiplex_bubbletype(bubble):
        """
        Use a single field to dispatch the type and resolve BubbleTypes-Enum.

        :param bubble: Constructed bubble
        :return:
        """
        if bubble['is_user']:
            t = 'user'
        elif bubble['is_system']:
            t = 'system'
        elif bubble['is_info']:
            t = 'info'
        else:
            t = 'status'
        return t

    def __init__(self, bubble):
        """
        Convert given bubble to reduced bubble holding only the core values.

        :param bubble:
        """
        self.bubble_type = self.__demultiplex_bubbletype(bubble)
        self.html = bubble['message']
        self.url = bubble['url'] if bubble['url'] != '' else None
        self.text = unhtmlify(bubble['message'])

    def __json__(self, _request):
        """
        Convert entity to JSON.

        :param _request: Request
        :return:
        """
        return {
            'type': self.bubble_type,
            'html': self.html,
            'text': self.text,
            'url': self.url
        }
