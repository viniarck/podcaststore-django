#!/usr/bin/env python
# -*- coding: utf-8 -*-


from rest_framework.request import Request
from typing import Dict, Any
import rapidjson as json
from rest_framework.exceptions import ParseError, APIException
import rest_framework.status as status


class Http403(APIException):

    status_code = status.HTTP_403_FORBIDDEN

    def __init__(self, msg: str) -> None:
        """Constructor of Http403."""
        super().__init__(msg)


def json_or_raise(request: Request) -> Dict[str, Any]:
    """Either get json data or raise."""
    try:
        data = request.data
        if isinstance(data, dict):
            return data
        return json.loads(data)
    except (json.JSONDecodeError, TypeError) as e:
        raise ParseError(
            detail=f"The body of the request isn't valid JSON. Exception {str(e)}",
            code=status.HTTP_400_BAD_REQUEST,
        )


def has_permission_or_raise(request: Request, podcast_id: str) -> object:
    """Validate requests user permission on a podcast or raise."""
    from podcaststore_api.models.podcast import PodcastUser

    user_id = request.user.id
    podcast_user = PodcastUser.objects.filter(user_id=user_id, podcast_id=podcast_id)
    if not podcast_user:
        raise Http403(
            f"User id {user_id} doesn't have permission on podcast id {podcast_id}"
        )
    return podcast_user[0]


def number_to_month(n: int) -> str:
    "Convert a number to a month string."
    if n == 1:
        return "january"
    elif n == 2:
        return "february"
    elif n == 3:
        return "march"
    elif n == 4:
        return "april"
    elif n == 5:
        return "may"
    elif n == 6:
        return "june"
    elif n == 7:
        return "july"
    elif n == 8:
        return "august"
    elif n == 9:
        return "september"
    elif n == 10:
        return "october"
    elif n == 11:
        return "november"
    elif n == 12:
        return "december"
    raise ValueError(f"Bad value: {n}. It should be >= 1 and <= 12")
