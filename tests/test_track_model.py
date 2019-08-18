#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from podcaststore_api.models.track import Track, TrackSerializer
from typing import Dict, Any


class TestTrackModel:

    """TestTrackModel."""

    @pytest.mark.django_db
    def test_repr(self, create_track: Track, track_data: Dict[str, Any]) -> None:
        """Test __repr__ method."""
        track = create_track
        assert repr(track) == f"Track({track.id}, {track_data['title']})"


class TestTrackSerializer:

    """TestTrackSerializer"""

    @pytest.mark.django_db
    def test_ser_data(self, track_data: Dict[str, Any]) -> None:
        """Test serialization data."""
        podcast_serd = TrackSerializer(data=track_data)
        assert podcast_serd.is_valid()
        for field in (
            "title",
            "media_url",
            "release_date",
            "duration",
        ):
            assert field in podcast_serd.data

    @pytest.mark.django_db
    def test_ser_data_save(
        self, create_track: Track, podcast_data: Dict[str, Any]
    ) -> None:
        """Test serialization data with save."""
        track = create_track
        podcast_serd = TrackSerializer(track)
        for field in TrackSerializer.Meta.fields:
            assert field in podcast_serd.data

    @pytest.mark.django_db
    def test_ser_invalid(self, track_data: Dict[str, Any]) -> None:
        """Test serialization invalid data."""
        del track_data["title"]
        track_serd = TrackSerializer(data=track_data)
        assert not track_serd.is_valid()
        assert "title" in track_serd.errors
