#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from model_utils.models import TimeStampedModel
from podcaststore_api.mixins import ValidateOnSaveMixin
from rest_framework.serializers import ModelSerializer


class Podcast(ValidateOnSaveMixin, TimeStampedModel):

    """Podcast active record."""

    id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=32)
    title = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)

    def __repr__(self) -> str:
        """Podcast __repr__."""
        return f"Podcast({self.id}, {self.name})"


class PodcastSerializer(ModelSerializer):

    """PodcastSerializer."""

    class Meta:
        """Meta."""

        model = Podcast
        fields = ("id", "name", "title", "start_date")


class PodcastUser(ValidateOnSaveMixin, TimeStampedModel):

    """PodcastUser active record. Represents if a User manages a Podcast."""

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE)
