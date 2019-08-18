#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from conftest import get_endpoint
import rest_framework.status as status
from rest_framework.test import APIClient
import rapidjson as json


class TestIdentifyView(object):
    """TestIdentifyView."""

    @pytest.mark.django_db
    def test_new_user(self) -> None:
        """Test creating a new user."""

        body = {"username": "foo", "password": "3jj2o20d", "email": "foo@bar.com"}
        endpoint = get_endpoint("identify/")
        requests = APIClient()
        res = requests.post(endpoint, json.dumps(body), content_type="application/json")
        assert res.status_code == status.HTTP_201_CREATED
        assert "token" in res.json()
        # try to treate the same user again
        res = requests.post(endpoint, json.dumps(body), content_type="application/json")
        assert res.status_code == status.HTTP_400_BAD_REQUEST
        assert "username" in res.json()

    @pytest.mark.django_db
    def test_new_user_missing_fields(self) -> None:
        """Test creating a new user with missing fields."""

        missing_fiels = ("password", "email")
        body = {"username": "foo"}
        endpoint = get_endpoint("identify/")
        requests = APIClient()
        res = requests.post(endpoint, json.dumps(body), content_type="application/json")
        assert res.status_code == status.HTTP_400_BAD_REQUEST
        data = res.json()
        for missed_field in missing_fiels:
            assert missed_field in data

    @pytest.mark.django_db
    def test_new_user_invalid_json(self) -> None:
        """Test creating a new user with invalid json data."""

        endpoint = get_endpoint("identify/")
        requests = APIClient()
        res = requests.post(endpoint, "foo", content_type="application/json")
        assert res.status_code == status.HTTP_400_BAD_REQUEST
