from rest_framework.views import APIView
import rest_framework.status as status
from rest_framework.response import Response
from rest_framework.request import Request
from django.db import transaction
from django.contrib.auth.models import User
from django.core.cache import cache
from drf_yasg.utils import swagger_auto_schema

from podcaststore_api.pagination import CustomLimitOffsetPagination
from podcaststore_api.utils import json_or_raise, has_permission_or_raise
from podcaststore_api.views.auth import JWTAPIView
from podcaststore_api.models.podcast import Podcast, PodcastUser, PodcastSerializer
from podcaststore_api.models.track import Track
from podcaststore_api.models.tag import Tag


class PodcastDetailView(JWTAPIView):

    """PodcastDetailView. """

    @swagger_auto_schema(responses={200: PodcastSerializer()})
    def get(self, request: Request, podcast_id: str) -> Response:
        """Get a Podcast given its id."""
        cache_key = f"{request.get_full_path()}"
        cached = cache.get(cache_key)
        if cached:
            return Response(cached, status=status.HTTP_200_OK)
        pod = Podcast.objects.filter(id=podcast_id)
        if not pod:
            return Response(
                f"Podcast id '{podcast_id}' not found", status=status.HTTP_404_NOT_FOUND
            )
        pod_serd = PodcastSerializer(pod[0])
        response = Response(pod_serd.data, status=status.HTTP_200_OK)
        if not cached:
            cache.set(cache_key, pod_serd.data)
        return response

    @swagger_auto_schema(request_body=PodcastSerializer)
    @transaction.atomic
    def put(self, request: Request, podcast_id: str) -> Response:
        """Update a Podcast."""
        data = json_or_raise(request)
        podcast_user = has_permission_or_raise(request, podcast_id)
        pod_serd = PodcastSerializer(data=data)
        if not pod_serd.is_valid():
            return Response(pod_serd.errors, status=status.HTTP_400_BAD_REQUEST)
        pod = podcast_user.podcast  # type: ignore
        pod.__dict__.update(id=podcast_id, **pod_serd.data)
        pod.save()
        cache_key = f"{request.get_full_path()}"
        cache.set(cache_key, pod_serd.data, timeout=600)
        cache.delete("/".join(cache_key.split("/")[:-2]) + "/")
        return Response(pod_serd.data, status=status.HTTP_200_OK)

    @swagger_auto_schema()
    @transaction.atomic
    def delete(self, request: Request, podcast_id: str) -> Response:
        """Delete a Podcast."""
        podcast_user = has_permission_or_raise(request, podcast_id)
        pod = podcast_user.podcast  # type: ignore
        pod.delete()
        cache_key = f"{request.get_full_path()}"
        cache.delete(cache_key)
        cache.delete("/".join(cache_key.split("/")[:-2]) + "/")
        return Response(status=status.HTTP_200_OK)


class PodcastListView(JWTAPIView):

    """PodcastListView. """

    @swagger_auto_schema(responses={200: PodcastSerializer(many=True)})
    def get(self, request: Request) -> Response:
        """Get a list of Podcasts."""
        cache_key = f"{request.get_full_path()}"
        cached = cache.get(cache_key)
        if cached:
            return Response(cached, status=status.HTTP_200_OK)
        paginator = CustomLimitOffsetPagination()
        results = paginator.paginate_queryset(Podcast.objects.all(), request, view=self)
        pod_serd = PodcastSerializer(results, many=True)
        response = paginator.get_paginated_response(pod_serd.data)
        if not cached:
            cache.set(cache_key, response.data, timeout=600)
        return response

    @swagger_auto_schema(request_body=PodcastSerializer)
    @transaction.atomic
    def post(self, request: Request) -> Response:
        """Post a new Podcast."""
        data = json_or_raise(request)
        pod_serd = PodcastSerializer(data=data)
        if not pod_serd.is_valid():
            return Response(pod_serd.errors, status=status.HTTP_400_BAD_REQUEST)
        pod = Podcast(**pod_serd.data)
        pod.save()
        user = User.objects.filter(id=request.user.id)[0]
        podcast_user = PodcastUser(user=user, podcast=pod)
        podcast_user.save()
        cache_key = f"{request.get_full_path()}"
        cache.delete(cache_key)
        return Response(pod_serd.data, status=status.HTTP_201_CREATED)


class PodcastTrackTagNameListView(APIView):

    """PodcastTrackTagNameListView. """

    @swagger_auto_schema()
    def get(self, request: Request, podcast_id: str) -> Response:
        """Get a list of unique Tags of a Podcast's Tracks."""
        tags_set = set()
        tracks = Track.objects.filter(podcast_id=podcast_id)
        for track in tracks:
            tags = Tag.objects.filter(track_id=track.id)
            for tag in tags:
                tags_set.add(tag.name)
        tags_dict = {"name": tag for tag in tags_set}
        return Response(tags_dict, status=status.HTTP_200_OK)
