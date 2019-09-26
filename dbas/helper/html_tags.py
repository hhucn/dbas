def wrap_in_tag(tag: str, content: str, attributes: str = ""):
    """
    Wraps some content in HTML tags with specific attributes.
    :param tag: The tag that wraps the content
    :param content: The content being wrapped
    :param attributes: Optional attributes that can be assigned to the opening tag
    :return: The wrapped content with the correct attributes.
    """
    return f"<{tag} {attributes}>{content}</{tag}>"
