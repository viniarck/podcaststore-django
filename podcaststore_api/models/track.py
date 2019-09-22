#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from model_utils.models import TimeStampedModel
from podcaststore_api.mixins import ValidateOnSaveMixin
from podcaststore_api.models.podcast import Podcast
import rest_framework.serializers as serializers


class Track(ValidateOnSaveMixin, TimeStampedModel):

    """Track active record."""

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE)
    media_url = models.URLField(blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    duration = models.TimeField(blank=True, null=True)

    @property
    def downloaded(self) -> int:
        from podcaststore_api.models.download import Download
        return len(Download.objects.filter(track_id=self.id))

    def __repr__(self) -> str:
        """Track __repr__."""
        return f"Track({self.id}, {self.title})"


class TrackSerializer(serializers.ModelSerializer):

    """TrackSerializer."""

    class Meta:
        """Meta."""

        model = Track
        fields = (
            "id",
            "title",
            "podcast_id",
            "media_url",
            "release_date",
            "duration",
            "downloaded",
        )


class TrackPodcastMonthlySerializer(serializers.Serializer):

    """TrackPodcastMonthlySerializer."""
    january = serializers.IntegerField(required=True)
    february = serializers.IntegerField(required=True)
    march = serializers.IntegerField(required=True)
    april = serializers.IntegerField(required=True)
    may = serializers.IntegerField(required=True)
    june = serializers.IntegerField(required=True)
    july = serializers.IntegerField(required=True)
    august = serializers.IntegerField(required=True)
    september = serializers.IntegerField(required=True)
    october = serializers.IntegerField(required=True)
    novemeber = serializers.IntegerField(required=True)
    december = serializers.IntegerField(required=True)
