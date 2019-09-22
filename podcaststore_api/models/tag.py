#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from model_utils.models import TimeStampedModel
from podcaststore_api.mixins import ValidateOnSaveMixin
from podcaststore_api.models import Track
from rest_framework.serializers import ModelSerializer


class Tag(ValidateOnSaveMixin, TimeStampedModel):

    """Tag active record."""

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)

    def __repr__(self) -> str:
        """Tag __repr__."""
        return f"Tag({self.id}, {self.name})"


class TagSerializer(ModelSerializer):

    """TagSerializer."""

    class Meta:
        """Meta."""

        model = Tag
        fields = ("id", "name", "track_id")


class TagNameSerializer(ModelSerializer):

    """TagNameSerializer."""

    class Meta:
        """Meta."""

        model = Tag
        fields = ("name",)
