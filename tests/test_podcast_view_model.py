#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import pytest
import rest_framework.status as status
from rest_framework.test import APIClient
from podcaststore_api.models import Podcast

from conftest import get_endpoint


class TestPodcastListView(object):
    """TestPodcastListView."""

    @pytest.mark.django_db
    def test_empty_list(self) -> None:
        """Test get empty list view."""

        endpoint = get_endpoint(f"podcast/")
        requests = APIClient()
        res = requests.get(endpoint, content_type="application/json")
        assert res.status_code == status.HTTP_200_OK
        data = res.json()["results"]
        assert data == []

    @pytest.mark.django_db
    def test_multiple_elements(self) -> None:
        """Test get list with multiple elements."""

        pod_names = ("first_pod", "second_pod")
        for pod_name in pod_names:
            Podcast(name=pod_name).save()
        endpoint = get_endpoint(f"podcast/")
        requests = APIClient()
        res = requests.get(endpoint, content_type="application/json")
        assert res.status_code == status.HTTP_200_OK
        data = res.json()["results"]
        for elem, name in zip(data, pod_names):
            assert name == elem["name"]

    @pytest.mark.django_db
    def test_create_podcast(self, create_user_auth, podcast_data) -> None:
        """Test create a new podcast."""

        res = create_user_auth
        token = res.json()["token"]
        endpoint = get_endpoint(f"podcast/")
        requests = APIClient()
        requests.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        res = requests.post(
            endpoint, json.dumps(podcast_data), content_type="application/json"
        )
        assert res.status_code == status.HTTP_201_CREATED
        res = requests.get(endpoint, content_type="application/json")
        assert podcast_data["name"] == res.data["results"][0]["name"]


class TestPodcastDetailedView(object):
    """TestPodcastDetailedView."""

    @pytest.mark.django_db
    def test_not_found(self) -> None:
        """Test id not found."""

        id = "9383837272"
        endpoint = get_endpoint(f"podcast/{id}/")
        requests = APIClient()
        res = requests.get(endpoint, content_type="application/json")
        assert res.status_code == status.HTTP_404_NOT_FOUND
        data = res.json()
        assert id in data

    @pytest.mark.django_db
    def test_id(self, podcast_data, create_podcast) -> None:
        """Test id."""

        pod = create_podcast
        endpoint = get_endpoint(f"podcast/{pod.id}/")
        requests = APIClient()
        res = requests.get(endpoint, content_type="application/json")
        assert res.status_code == status.HTTP_200_OK
        data = res.json()
        assert pod.id == data["id"]

    @pytest.mark.django_db
    def test_create_update_podcast(self, create_user_auth, podcast_data) -> None:
        """Test create a new podcast and update it."""

        res = create_user_auth
        token = res.json()["token"]
        endpoint = get_endpoint(f"podcast/")
        requests = APIClient()
        requests.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        res = requests.post(
            endpoint, json.dumps(podcast_data), content_type="application/json"
        )
        assert res.status_code == status.HTTP_201_CREATED
        res = requests.get(endpoint, content_type="application/json")
        assert podcast_data["name"] == res.data["results"][0]["name"]

        podcast_id = res.data["results"][0]["id"]
        endpoint = get_endpoint(f"podcast/{podcast_id}/")
        new_name = "foobar"
        podcast_data["name"] = new_name
        requests.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        res = requests.put(
            endpoint, json.dumps(podcast_data), content_type="application/json"
        )
        assert res.status_code == status.HTTP_200_OK

        res = requests.get(endpoint, content_type="application/json")
        assert res.status_code == status.HTTP_200_OK
        assert res.data["name"] == new_name

    @pytest.mark.django_db
    def test_create_delete(self, create_user_auth, podcast_data) -> None:
        """Test create a new podcast and delete it."""

        res = create_user_auth
        token = res.json()["token"]
        endpoint = get_endpoint(f"podcast/")
        requests = APIClient()
        requests.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        res = requests.post(
            endpoint, json.dumps(podcast_data), content_type="application/json"
        )
        assert res.status_code == status.HTTP_201_CREATED
        res = requests.get(endpoint, content_type="application/json")
        assert res.data["results"][0]["name"] == podcast_data["name"]

        podcast_id = res.data["results"][0]["id"]
        endpoint = get_endpoint(f"podcast/{podcast_id}/")
        new_name = "foobar"
        podcast_data["name"] = new_name
        requests.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        res = requests.delete(endpoint, content_type="application/json")
        assert res.status_code == status.HTTP_200_OK

        res = requests.get(endpoint, content_type="application/json")
        assert res.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.django_db
    def test_create_update_permission_podcast(
        self, create_user_auth, podcast_data
    ) -> None:
        """Test create a new podcast and update it with wrong permissions."""

        res = create_user_auth
        token = res.json()["token"]
        endpoint = get_endpoint(f"podcast/")
        requests = APIClient()
        requests.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        res = requests.post(
            endpoint, json.dumps(podcast_data), content_type="application/json"
        )
        assert res.status_code == status.HTTP_201_CREATED
        res = requests.get(endpoint, content_type="application/json")
        assert podcast_data["name"] == res.data["results"][0]["name"]

        pod = Podcast(name="second")
        pod.save()

        endpoint = get_endpoint(f"podcast/{pod.id}/")
        new_name = "foobar"
        podcast_data["name"] = new_name
        requests.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        res = requests.put(
            endpoint, json.dumps(podcast_data), content_type="application/json"
        )
        assert res.status_code == status.HTTP_403_FORBIDDEN
