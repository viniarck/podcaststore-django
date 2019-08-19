#!/usr/bin/env python
# -*- coding: utf-8 -*-

import django
import os
import random
from django.db import transaction

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "podcaststore_site.settings")
django.setup()
from podcaststore_api.models import Podcast
from podcaststore_api.models import Track
from podcaststore_api.models import Download
from podcaststore_api.models import Tag
import datetime


def gen_podcasts(n=100) -> None:
    for i in range(n):
        p = Podcast(name=f"pod_{i+1}")
        p.save()


def gen_tracks(max_track_per_pod=10) -> None:
    podcasts = Podcast.objects.all()
    tag_names = {0: "guitar", 1: "bass", 2: "drum", 3: "vocal", 4: "hot"}
    with transaction.atomic():
        for podcast in podcasts:
            for n in range(random.randint(1, 10)):
                dt = datetime.datetime.now()
                track_title = f"track{n}_{podcast.name}"
                media_url = f"http://xyz.cdn.com/{track_title}"
                release_date = datetime.datetime(
                    year=dt.year, month=random.randint(1, 12), day=random.randint(1, 28)
                )
                duration = str(
                    datetime.timedelta(
                        minutes=random.randint(1, 5), seconds=random.randint(1, 60)
                    )
                )
                t = Track(
                    title=track_title,
                    podcast=podcast,
                    media_url=media_url,
                    release_date=release_date,
                    duration=duration,
                )
                t.save()
                for m in range(1, 3):
                    tag = Tag(name=tag_names[random.randint(0, 4)], track=t)
                    tag.save()
                for k in range(random.randint(1, 10)):
                    new_dt = datetime.datetime(
                        year=dt.year, month=random.randint(1, 12), day=dt.day
                    )
                    d = Download(track=t, date=new_dt)
                    d.save()


def main() -> None:
    gen_podcasts()
    gen_tracks()


if __name__ == "__main__":
    main()
