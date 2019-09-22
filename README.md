[![pipeline status](https://gitlab.com/viniarck/podcaststore-django/badges/master/pipeline.svg)](https://gitlab.com/viniarck/podcaststore-django/commits/master)

# podcaststore-django

This is a back-end API written in Python with Django and DRF to allow users to access a podcast store. In this podcast store, there are podcasts, tracks, users, tags, and users should be able to express a reaction to any track.

## API Docs

Based on [these requirements](./docs/api_requirements.md), the [following endpoints](http://podcaststore.devdaily.org:4000/v1/doc/) are available.

## Demo

You can check a demo running on my VPS [on this URL](http://podcaststore.devdaily.org:8080/) of an Web front-end App which consumes this API.

### Database UML diagram

Based on the [API and back-end requirements](./docs/api_requirements.md), the following UML relational diagram will be implemented:

![uml](./docs/schema.png)


## Running locally

Make sure you have docker-compose installed first.

```
docker-compose -f docker-compose.yml -f docker-compose.dev.yml -f docker-compose.secrets.yml up -d
```
