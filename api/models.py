from dataclasses import dataclass
from typing import List

from dbas.database.discussion_model import StatementReferences, Issue, Statement, TextVersion, User
from dbas.helper.url import url_to_statement
from dbas.lib import unhtmlify


class JSONBase:
    def __json__(self):
        return vars(self)


class DataItem(JSONBase):
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


class DataBubble(JSONBase):
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
        self.type = self.__demultiplex_bubbletype(bubble)
        self.html = bubble['message']
        self.url = bubble['bubble_url'] if bubble['bubble_url'] != '' else None
        self.text = unhtmlify(bubble['message'])


class DataReference(JSONBase):
    def __init__(self, statement_reference: StatementReferences):
        self.uid: int = statement_reference.uid
        self.reference: str = statement_reference.reference
        issue: Issue = statement_reference.issue
        statement: Statement = statement_reference.statement
        self.url: str = url_to_statement(issue, statement)


class DataAuthor(JSONBase):
    """
    This class models a Author as it is required for the results by searching with Levensthein.
    """

    def __init__(self, author: User):
        self.uid: int = author.uid
        self.nickname: str = author.nickname


class DataIssue(JSONBase):
    """
    This class models a Issue as it is required for the results by searching with Levensthein.
    """

    def __init__(self, issue: Issue):
        self.uid: int = issue.uid
        self.slug: str = issue.slug
        self.language: str = issue.lang
        self.title: str = issue.title
        self.info: str = issue.info


class DataStatement(JSONBase):
    """
    This class models a Statement as it is required for the results by searching with Levensthein.
    """

    def __init__(self, statement: Statement, textversion: TextVersion):
        self.isPosition: bool = statement.is_position
        self.uid: int = statement.uid
        self.text: str = textversion.content


@dataclass
class DataOrigin:
    """
    Store an origin from the API.
    """
    entity_id: str
    aggregate_id: str
    author: str
    version: int
