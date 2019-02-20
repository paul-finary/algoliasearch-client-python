import json
import sys

from typing import Optional, Iterable, List, Union, Iterator

from algoliasearch.exceptions import MissingObjectIdException

if sys.version_info >= (3, 0):
    from urllib.parse import quote
else:
    from urllib import quote


def endpoint(path, *args):
    # type: (str, Optional[*str,*int]) -> str

    arguments = []
    for arg in args:
        if not sys.version_info >= (3, 0) and isinstance(arg, unicode):
            arguments.append(quote(arg.encode('utf-8'), safe=''))
        else:
            arguments.append(quote(str(arg), safe=''))

    return path % tuple(arguments)


def get_items(dictionary=None):
    # type: (Optional[dict]) -> Iterable

    if dictionary is None:
        items = []  # type: Iterable
    elif sys.version_info >= (3, 0):
        items = dictionary.items()
    else:
        items = dictionary.iteritems()  # pragma: no cover

    return items


def assert_object_id(objects):
    # type: (Iterable[dict]) -> None

    for obj in objects:
        if 'objectID' not in obj:
            raise MissingObjectIdException(
                'Missing `objectID` in: ' + json.dumps(obj), obj)


def build_raw_response_batch(action, objects):
    # type: (str, Union[List[dict], Iterator[dict]]) -> List[dict]

    requests = []
    for obj in objects:
        requests.append({
            'action': action,
            'body': obj
        })

    return requests
