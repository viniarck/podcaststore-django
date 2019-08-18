from rest_framework.views import APIView
import rest_framework.status as status
from rest_framework.response import Response
from rest_framework.request import Request
from podcaststore_api.models import Podcast
from podcaststore_api.models.track import (
    Track,
    TrackSerializer,
    TrackPodcastMonthlySerializer,
)
from podcaststore_api.pagination import CustomLimitOffsetPagination
from podcaststore_api.models import Tag
from podcaststore_api.models.download import Download
from drf_yasg.utils import swagger_auto_schema
from podcaststore_api.utils import number_to_month


class TrackDetailView(APIView):

    """TrackDetailView. """

    @swagger_auto_schema(responses={200: TrackSerializer()})
    def get(self, request: Request, track_id: str) -> Response:
        """Get a Track given its id."""
        track = Track.objects.filter(id=track_id)
        if not track:
            return Response(
                f"Track id '{track_id}' not found", status=status.HTTP_404_NOT_FOUND
            )
        track_serd = TrackSerializer(track[0])
        return Response(track_serd.data, status=status.HTTP_200_OK)


class TrackPodcastListView(APIView):

    """TrackPodcastListView. """

    @swagger_auto_schema(responses={200: TrackSerializer()})
    def get(self, request: Request, podcast_id: str) -> Response:
        """Get a list of Tracks of a Podcast."""
        if not Podcast.objects.filter(id=podcast_id):
            return Response(status=status.HTTP_404_NOT_FOUND)
        paginator = CustomLimitOffsetPagination()
        results = paginator.paginate_queryset(
            Track.objects.filter(podcast_id=podcast_id), request, view=self
        )
        track_serd = TrackSerializer(results, many=True)
        return paginator.get_paginated_response(track_serd.data)


class TrackPodcastTagNameListView(APIView):

    """TrackPodcastTagNameListView. """

    @swagger_auto_schema(responses={200})
    def get(self, request: Request, podcast_id: str) -> Response:
        """Get a list of unique Tags of a Podcast's Tracks."""
        tags_set = set()
        tracks = Track.objects.filter(podcast_id=podcast_id)
        for track in tracks:
            tags = Tag.objects.filter(track_id=track.id)
            for tag in tags:
                tags_set.add({"name": tag.name})
        return Response(tags_set, status=status.HTTP_200_OK)


class TrackPodcastMonthlyDownloadView(APIView):

    """TrackPodcastListView. """

    @swagger_auto_schema(responses={200: TrackPodcastMonthlySerializer()})
    def get(self, request: Request, podcast_id: str) -> Response:
        """Get the total number of track downloads per month of a Podcast."""

        month_counter = {
            "january": 0,
            "february": 0,
            "march": 0,
            "april": 0,
            "may": 0,
            "june": 0,
            "july": 0,
            "august": 0,
            "september": 0,
            "october": 0,
            "november": 0,
            "december": 0,
        }
        tracks = Track.objects.filter(podcast_id=podcast_id)
        for track in tracks:
            downloads = Download.objects.filter(track_id=track.id)
            for download in downloads:
                month_counter[number_to_month(download.date.month)] += 1
        track_serd = TrackPodcastMonthlySerializer(data=month_counter)
        return Response(track_serd.initial_data, status=status.HTTP_200_OK)


class TrackListView(APIView):

    """TrackListView. """

    @swagger_auto_schema(responses={200: TrackSerializer(many=True)})
    def get(self, request: Request) -> Response:
        """Get a list of Tracks."""
        paginator = CustomLimitOffsetPagination()
        results = paginator.paginate_queryset(Track.objects.all(), request, view=self)
        track_serd = TrackSerializer(results, many=True)
        return paginator.get_paginated_response(track_serd.data)
