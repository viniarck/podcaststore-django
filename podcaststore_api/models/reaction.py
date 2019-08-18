#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.db import models

from django.contrib.auth.models import User
from model_utils.models import TimeStampedModel
from podcaststore_api.mixins import ValidateOnSaveMixin
from podcaststore_api.models import Track
from rest_framework.serializers import ModelSerializer
from model_utils import Choices


class Reaction(ValidateOnSaveMixin, TimeStampedModel):

    """Reaction active record."""

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    CODE_CHOICES = Choices("like", "love", "amazing", "dislike")
    deleted_on = models.DateTimeField(blank=True, null=True)
    code = models.CharField(max_length=16, choices=CODE_CHOICES)

    def __repr__(self) -> str:
        """Podcast __repr__."""
        return f"Reaction({self.id}, {self.code})"


class ReactionSerializer(ModelSerializer):

    """ReactionSerializer."""

    class Meta:
        """Meta."""

        model = Reaction
        fields = ("id", "user_id", "track_id", "code")
