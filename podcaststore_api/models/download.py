#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.db import models

from model_utils.models import TimeStampedModel
from podcaststore_api.mixins import ValidateOnSaveMixin
from podcaststore_api.models import Track
from rest_framework.serializers import ModelSerializer
from django.utils.timezone import now


class Download(ValidateOnSaveMixin, TimeStampedModel):

    """Download active record."""

    id = models.AutoField(primary_key=True)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    date = models.DateTimeField(default=now)

    def __repr__(self) -> str:
        """Download __repr__."""
        return f"Download({self.id}, {self.track.id}, {self.date})"


class DownloadSerializer(ModelSerializer):

    """DownloadSerializer."""

    class Meta:
        """Meta."""

        model = Download
        fields = ("id", "track_id", "date")
