#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
podcaststore URLs.
"""
from django.urls import path
from podcaststore_api.views.podcast import (
    PodcastDetailView,
    PodcastListView,
    PodcastTrackTagNameListView,
)
from podcaststore_api.views.track import (
    TrackDetailView,
    TrackListView,
    TrackPodcastListView,
    TrackPodcastMonthlyDownloadView,
)
from podcaststore_api.views.identify import IdentifyView
from podcaststore_api.views.auth import AuthView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="podcaststore-django",
        default_version="v1",
        description="podcaststore-django",
        contact=openapi.Contact(email="viniarck@gmail.com"),
        license=openapi.License(name="Apache"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path(
        "doc/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("doc/spec/", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("identify/", IdentifyView.as_view()),
    path("auth/", AuthView.as_view()),
    path("podcast/", PodcastListView.as_view()),
    path("podcast/<str:podcast_id>/", PodcastDetailView.as_view()),
    path("podcast/<str:podcast_id>/tag/", PodcastTrackTagNameListView.as_view()),
    path("track/", TrackListView.as_view()),
    path("track/<str:track_id>/", TrackDetailView.as_view()),
    path("track/podcast/<str:podcast_id>/", TrackPodcastListView.as_view()),
    path(
        "track/podcast/<str:podcast_id>/monthly_download_stats/",
        TrackPodcastMonthlyDownloadView.as_view(),
    ),
]
