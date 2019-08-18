#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import rest_framework.status as status
from rest_framework.test import APIClient
from podcaststore_api.models import Podcast, Track

from conftest import get_endpoint


class TestTrackListView(object):
    """TestTrackListView."""

    @pytest.mark.django_db
    def test_empty_list(self) -> None:
        """Test get empty list view."""

        endpoint = get_endpoint(f"track/")
        requests = APIClient()
        res = requests.get(endpoint, content_type="application/json")
        assert res.status_code == status.HTTP_200_OK
        data = res.json()["results"]
        assert data == []

    @pytest.mark.django_db
    def test_multiple_elements(self) -> None:
        """Test get list with multiple elements."""

        pod_names = ("first_pod", "second_pod")
        podcasts = []
        tracks = []
        for pod_name in pod_names:
            pod = Podcast(name=pod_name)
            pod.save()
            podcasts.append(pod)
        track_titles = ("first_track", "second_track")
        for track_title, podcast in zip(track_titles, podcasts):
            track = Track(podcast=podcast, title=track_title)
            track.save()
            tracks.append(track)
        endpoint = get_endpoint(f"track/")
        requests = APIClient()
        res = requests.get(endpoint, content_type="application/json")
        assert res.status_code == status.HTTP_200_OK
        data = res.json()["results"]
        for elem, track in zip(data, tracks):
            assert elem["title"] == track.title

        endpoint = get_endpoint(f"track/podcast/{podcasts[0].id}/")
        res = requests.get(endpoint, content_type="application/json")
        assert res.status_code == status.HTTP_200_OK
        data = res.json()["results"]
        assert len(data) == 1
        assert data[0]["title"] == tracks[0].title


class TestPodcastDetailedView(object):
    """TestPodcastDetailedView."""

    @pytest.mark.django_db
    def test_not_found(self) -> None:
        """Test id not found."""

        id = "9383837272"
        endpoint = get_endpoint(f"track/{id}/")
        requests = APIClient()
        res = requests.get(endpoint, content_type="application/json")
        assert res.status_code == status.HTTP_404_NOT_FOUND
        data = res.json()
        assert id in data

    @pytest.mark.django_db
    def test_id(self, create_track: Track) -> None:
        """Test id."""

        track = create_track
        endpoint = get_endpoint(f"track/{track.id}/")
        requests = APIClient()
        res = requests.get(endpoint, content_type="application/json")
        assert res.status_code == status.HTTP_200_OK
        data = res.json()
        assert data["id"] == track.id
