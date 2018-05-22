from typing import List

from dbas.lib import unhtmlify


class Item:
    """
    Entity to construct items-dict.
    """

    def __init__(self, htmls: List[str], url: str):
        """
        Construct item for items-dict.

        :param htmls: List of strings containing html, which is also converted to plain text
        :param url: URL to next step in the discussion
        """
        self.url = url if url != '' else None
        self.htmls = htmls
        self.texts = [unhtmlify(html) for html in htmls]

    def __json__(self, _request):
        """
        Convert entity to JSON.

        :param _request: Request
        :return:
        """
        return {
            'htmls': self.htmls,
            'texts': self.texts,
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
