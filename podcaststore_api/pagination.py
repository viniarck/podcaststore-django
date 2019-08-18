#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Custom pagination View.
"""

from collections import OrderedDict

import rest_framework.status as status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class CustomLimitOffsetPagination(LimitOffsetPagination):
    """Custom LimitOffsetPagination view."""

    offset = 0
    default_limit = 1000
    limit = 1000
    limit_query_param = "limit"
    offset_query_param = "offset"

    def get_paginated_response(self, data: object):
        return Response(
            OrderedDict(
                [
                    ("count", self.count),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("results", data),
                ]
            ),
            status=status.HTTP_200_OK,
        )
