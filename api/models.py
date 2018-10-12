from typing import List

from dbas.database.discussion_model import StatementReferences, Issue, Statement, TextVersion, User
from dbas.helper.url import url_to_statement
from dbas.lib import unhtmlify


class DataItem:
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


class DataBubble:
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
        self.url = bubble['bubble_url'] if bubble['bubble_url'] != '' else None
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


class DataReference:
    def __init__(self, statement_reference: StatementReferences):
        self.uid: int = statement_reference.uid
        self.reference: str = statement_reference.reference
        self.issue: Issue = statement_reference.issue
        self.statement: Statement = statement_reference.statement
        self.url: str = url_to_statement(self.issue, self.statement)

    def __json__(self, _request):
        return {
            "uid": self.uid,
            "text": self.reference,
            "url": self.url
        }


class DataAuthor:
    """
    This class models a Author as it is required for the results by searching with Levensthein.
    """

    def __init__(self, author: User):
        self.uid: int = author.uid
        self.nickname: str = author.nickname

    def __json__(self):
        return {
            "uid": self.uid,
            "nickname": self.nickname
        }


class DataIssue:
    """
    This class models a Issue as it is required for the results by searching with Levensthein.
    """

    def __init__(self, issue: Issue):
        self.uid: int = issue.uid
        self.slug: str = issue.slug
        self.language: str = issue.lang
        self.title: str = issue.title
        self.info: str = issue.info

    def __json__(self):
        return {
            "uid": self.uid,
            "slug": self.slug,
            "lang": self.language,
            "title": self.title,
            "info": self.info
        }


class DataStatement(object):
    """
    This class models a Statement as it is required for the results by searching with Levensthein.
    """

    def __init__(self, statement: Statement, textversion: TextVersion):
        self.isPosition: bool = statement.is_position
        self.uid: int = statement.uid
        self.text: str = textversion.content

    def __json__(self):
        return {
            "isPosition": self.isPosition,
            "uid": self.uid,
            "text": self.text
        }


def transform_levensthein_search_results(statement: DataStatement, author: DataAuthor, issue: DataIssue) -> dict:
    """
    This is the json format of the results by searching with Levensthein.

    :param statement: See ApiStatement
    :param author: See ApiAuthor
    :param issue: See ApiIssue
    :return: The data-structure which is used for the results in the searching interface.
    """
    return {
        "isPosition": statement.__json__().get("isPosition"),
        "uid": statement.__json__().get("uid"),
        "text": statement.__json__().get("text"),
        "author": author.__json__(),
        "issue": issue.__json__()
    }
