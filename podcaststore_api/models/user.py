#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rest_framework.serializers as serializers


class UserSerializer(serializers.Serializer):

    """UserSerializer."""

    username = serializers.CharField(max_length=128, required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(max_length=128, required=True)
    first_name = serializers.CharField(max_length=128, required=False)
    last_name = serializers.CharField(max_length=128, required=False)


class LoginSerializer(serializers.Serializer):

    """LoginSerializer."""

    username = serializers.CharField(max_length=128, required=True)
    password = serializers.CharField(max_length=128, required=True)
