#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from conftest import get_endpoint
import rest_framework.status as status
from rest_framework.test import APIClient
import rapidjson as json


class TestAuthView(object):
    """TestAuthView."""

    @pytest.mark.django_db
    def test_new_user_auth(self) -> None:
        """Test creating a new user and re-auth."""

        body = {"username": "foo", "password": "3jj2o20d", "email": "foo@bar.com"}
        endpoint = get_endpoint("identify/")
        requests = APIClient()
        res = requests.post(endpoint, json.dumps(body), content_type="application/json")
        assert res.status_code == status.HTTP_201_CREATED
        data = res.json()
        assert "token" in data
        token = data["token"]
        endpoint = get_endpoint("auth/")
        res = requests.post(endpoint, json.dumps(body), content_type="application/json")
        assert res.status_code == status.HTTP_201_CREATED
        assert token.split(".")[:1] == res.data["token"].split(".")[:1]
        # missing user
        body2 = dict(body)
        del body2["username"]
        res = requests.post(
            endpoint, json.dumps(body2), content_type="application/json"
        )
        assert res.status_code == status.HTTP_400_BAD_REQUEST
        # test wrong password
        body["password"] = "wrong"
        res = requests.post(endpoint, json.dumps(body), content_type="application/json")
        assert res.status_code == status.HTTP_400_BAD_REQUEST
