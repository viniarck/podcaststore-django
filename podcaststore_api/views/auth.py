#!/usr/bin/env python
# -*- coding: utf-8 -*-


import rest_framework.status as status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from podcaststore_api.utils import json_or_raise

from django.contrib.auth.models import User
from podcaststore_api.models.user import LoginSerializer
from drf_yasg.utils import swagger_auto_schema


class JWTAPIView(APIView):
    """Base APIView class for JWT authentication."""

    authentication_classes = (JWTTokenUserAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    @classmethod
    def get_token(cls, login: User) -> str:
        """Get a JWT token for a Login object."""
        refresh = RefreshToken.for_user(login)
        return str(refresh.access_token)


class AuthView(APIView):

    """AuthView."""

    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request: Request) -> Response:
        """Authenticate or Re-authtenticate a User."""
        data = json_or_raise(request)
        user_serd = LoginSerializer(data=data)
        if not user_serd.is_valid():
            return Response(user_serd.errors, status=status.HTTP_400_BAD_REQUEST)
        user_data = user_serd.data
        user_query = User.objects.filter(username=user_data["username"])
        if not user_query:
            return Response(
                "Either the user or the password doesn't match",
                status=status.HTTP_400_BAD_REQUEST,
            )
        user: User = user_query[0]
        if not user.check_password(user_data["password"]):
            return Response(
                "Either the user or the password doesn't match",
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"token": str(RefreshToken.for_user(user).access_token)},
            status=status.HTTP_201_CREATED,
        )
