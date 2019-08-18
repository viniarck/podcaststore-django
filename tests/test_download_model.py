#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from podcaststore_api.models.download import Download, DownloadSerializer


class TestDownloadModel:

    """TestDownloadModel."""

    @pytest.mark.django_db
    def test_repr(self, create_download: Download) -> None:
        """Test __repr__ method."""
        download = create_download
        assert (
            repr(download)
            == f"Download({download.id}, {download.track_id}, {download.date})"
        )


class TestTagSerializer:

    """TestTagSerializer"""

    @pytest.mark.django_db
    def test_ser_data(self, create_download: Download) -> None:
        """Test serialization data."""
        download_serd = DownloadSerializer(create_download)
        for field in ("id", "track_id", "date"):
            assert field in download_serd.data
