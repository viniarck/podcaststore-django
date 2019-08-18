#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from podcaststore_api.models.tag import Tag, TagSerializer
from podcaststore_api.models.track import Track
from typing import Dict, Any


class TestTagModel:

    """TestTagModel."""

    @pytest.mark.django_db
    def test_repr(self, create_tag: Tag, tag_data: Dict[str, Any]) -> None:
        """Test __repr__ method."""
        tag = create_tag
        assert repr(tag) == f"Tag({tag.id}, {tag_data['name']})"


class TestTagSerializer:

    """TestTagSerializer"""

    @pytest.mark.django_db
    def test_ser_data(self, tag_data: Dict[str, Any]) -> None:
        """Test serialization data."""
        tag_serd = TagSerializer(data=tag_data)
        assert tag_serd.is_valid()
        for field in ("name", ):
            assert field in tag_serd.data

    @pytest.mark.django_db
    def test_ser_data_save(self, create_track: Track, tag_data: Dict[str, Any]) -> None:
        """Test serialization data with save."""
        tag_data["track_id"] = create_track.id
        tag = Tag(track=create_track, **tag_data)
        tag.save()
        tag_serd = TagSerializer(tag)
        for field in TagSerializer.Meta.fields:
            assert field in tag_serd.data

    @pytest.mark.django_db
    def test_ser_invalid(self, tag_data: Dict[str, Any]) -> None:
        """Test serialization invalid data."""
        del tag_data["name"]
        tag_serd = TagSerializer(data=tag_data)
        assert not tag_serd.is_valid()
        assert "name" in tag_serd.errors
