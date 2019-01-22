from api.models import DataOrigin, DataAuthor
from dbas.validators.lib import add_error, to_int


def valid_optional_origin(request):
    """
    Look up origin in json_body and validate it.

    :param request:
    :return:
    """
    origin: dict = request.json_body.get("origin")
    if not origin:
        # Since it is optional, an empty origin is also valid
        request.validated["origin"] = None
        return True

    entity_id: str = origin.get("entity-id")
    aggregate_id: str = origin.get("aggregate-id")
    author: dict = origin.get("author")
    version: int = to_int(origin.get("version"))

    if entity_id is None or aggregate_id is None or author is None or version is None:
        # If there is an origin, it should be well-formed
        received_keys = ", ".join(k for k in origin.keys())
        add_error(request,
                  "Origin malformed. Needs dictionary with keys \"entity-id (str)\", \"aggregate-id (str)\", "
                  "\"author (object)\" and \"version (int)\". Received these keys: {}".format(received_keys))
        return False

    # Extract author and create native object
    data_author: DataAuthor = DataAuthor(is_dgep_native=author.get("dgep-native"), nickname=author.get("name"),
                                         uid=author.get("id"))

    request.validated["origin"] = DataOrigin(entity_id, aggregate_id, data_author, version)
    return True
