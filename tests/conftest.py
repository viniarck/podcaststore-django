#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import pytest
import os
from typing import Dict, Any
import rest_framework.status as status
from rest_framework.test import APIClient
from podcaststore_api.models import Podcast, Track, Tag, Reaction, Download
from django.contrib.auth.models import User
from django.core.cache import cache


def base_url(
    host=os.environ.get("API_HOST", "localhost"),
    port=os.environ.get("API_HTTP_PORT", 8000),
    base_path="v1/",
) -> str:
    """base URL for testing."""
    return f"http://{host}:{port}/{base_path}"


def get_endpoint(endpoint: str, **kwargs) -> str:
    """Get a full endpoint on top of the base URL."""
    return f"{base_url(**kwargs)}{endpoint}"


def clear_all_cache_keys() -> None:
    """Clear all cache keys."""
    keys = cache.keys("*") or []
    for key in keys:
        cache.delete(key)


@pytest.fixture(scope="function", autouse=True)
def tear_down_cache(request):
    """Cache tear down clean up for every test case."""
    request.addfinalizer(clear_all_cache_keys)


@pytest.fixture(scope="function")
def track_data() -> Dict[str, Any]:
    """Get track data to instantiate a Track."""
    return dict(
        title="Python 3.8 new features", release_date="2016-07-30", podcast_id=1
    )


@pytest.fixture(scope="function")
def track_obj(track_data: Dict[str, Any], create_podcast: Podcast) -> Track:
    """Get a Track object."""
    return Track(podcast=create_podcast, **track_data)


@pytest.fixture(scope="function")
def create_track(track_obj: Track, create_podcast: Podcast) -> Track:
    """Create Get a Track object."""
    podcast = create_podcast
    track = track_obj
    track.podcast = podcast
    track.save()
    return track


@pytest.fixture(scope="function")
def user_data() -> Dict[str, Any]:
    """Get user data to instantiate a User."""
    return dict(
        username="viniarck",
        first_name="Vinicius",
        last_name="Arcanjo",
        email="viniarck@gmail.com",
        password="sup3rs3cr3t!",
    )


@pytest.fixture(scope="function")
def create_user(user_data: Dict[str, Any]) -> User:
    """Create User object."""
    user = User.objects.create_user(**user_data)
    return user


@pytest.fixture(scope="function")
def create_user_auth(user_data: Dict[str, Any]) -> User:
    """Create a new User object."""
    User.objects.create_user(**user_data)
    endpoint = get_endpoint(f"auth/")
    requests = APIClient()
    res = requests.post(
        endpoint,
        json.dumps(
            {"username": user_data["username"], "password": user_data["password"]}
        ),
        content_type="application/json",
    )
    assert res.status_code == status.HTTP_201_CREATED
    return res


@pytest.fixture(scope="function")
def podcast_data() -> Dict[str, Any]:
    """Get podcast data to instantiate a Podcast."""
    return dict(
        name="talkpythontome", title="Talk Python to Me", start_date="2016-07-30"
    )


@pytest.fixture(scope="function")
def podcast_obj(podcast_data: Dict[str, Any]) -> Podcast:
    """Get a Podcast object."""
    return Podcast(**podcast_data)


@pytest.fixture(scope="function")
def create_podcast(podcast_obj: Podcast) -> Podcast:
    """Create a Podcast object."""
    podcast = podcast_obj
    podcast.save()
    return podcast


@pytest.fixture(scope="function")
def tag_data() -> Dict[str, Any]:
    """Get tag_data to instantiate a Tag."""
    return dict(name="python", track_id=1)


@pytest.fixture(scope="function")
def tag_object(tag_data: Dict[str, Any]) -> Tag:
    """Get a Tag object."""
    return Tag(**tag_data)


@pytest.fixture(scope="function")
def create_tag(create_track: Track, tag_data: Dict[str, Any]) -> Tag:
    """Create a Tag object."""
    track = create_track
    tag_data["track_id"] = track.id
    tag = Tag(track=track, **tag_data)
    tag.save()
    return tag


@pytest.fixture(scope="function")
def reaction_data() -> Dict[str, Any]:
    """Get reaction_data to instantiate a Reaction."""
    return dict(code="like")


@pytest.fixture(scope="function")
def reaction_object(
    reaction_data: Dict[str, Any], create_user: User, create_track: Track
) -> Reaction:
    """Get a Reaction object."""
    return Reaction(user=create_user, track=create_track, **reaction_data)


@pytest.fixture(scope="function")
def create_reaction(reaction_object: Reaction) -> Reaction:
    """Create a Reaction object."""
    reaction_object.save()
    return reaction_object


@pytest.fixture(scope="function")
def download_object(create_track: Track) -> Download:
    """Get a Download object."""
    return Download(track=create_track)


@pytest.fixture(scope="function")
def create_download(download_object: Download) -> Download:
    """Create a Download object."""
    download_object.save()
    return download_object
