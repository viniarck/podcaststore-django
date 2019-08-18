#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from podcaststore_api.models.podcast import Podcast, PodcastSerializer


class TestPodcastModel:

    """TestPodcastModel."""

    @pytest.mark.django_db
    def test_repr(self, podcast_data) -> None:
        """Test __repr__ method."""
        podcast = Podcast(**podcast_data)
        podcast.save()
        assert repr(podcast) == f"Podcast({podcast.id}, {podcast_data['name']})"


class TestPodcastSerializer:

    """TestPodcastSerializer"""

    @pytest.mark.django_db
    def test_ser_data(self, podcast_data) -> None:
        """Test serialization data."""
        podcast_serd = PodcastSerializer(data=podcast_data)
        assert podcast_serd.is_valid()
        for field in ("name", "title", "start_date"):
            assert field in podcast_serd.data

    @pytest.mark.django_db
    def test_ser_data_save(self, podcast_data) -> None:
        """Test serialization data with save."""
        pod = Podcast(**podcast_data)
        podcast_serd = PodcastSerializer(pod)
        for field in PodcastSerializer.Meta.fields:
            assert field in podcast_serd.data

    @pytest.mark.django_db
    def test_ser_invalid(self, podcast_data) -> None:
        """Test serialization invalid data."""
        del podcast_data["name"]
        podcast_serd = PodcastSerializer(data=podcast_data)
        assert not podcast_serd.is_valid()
        assert "name" in podcast_serd.errors
