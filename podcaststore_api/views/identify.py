from rest_framework.views import APIView
import rest_framework.status as status
from rest_framework.response import Response
from rest_framework.request import Request
from podcaststore_api.utils import json_or_raise
from podcaststore_api.models.user import UserSerializer
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema


class IdentifyView(APIView):

    """IdentifyView."""

    @swagger_auto_schema(request_body=UserSerializer)
    def post(self, request: Request) -> Response:
        """Post a new Login."""
        data = json_or_raise(request)
        user_serd = UserSerializer(data=data)
        if not user_serd.is_valid():
            return Response(user_serd.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.create_user(**user_serd.data)
        except (TypeError, ValidationError) as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return Response(
                {"username": [f"'{user_serd.data['username']}' is already registered"]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"token": str(RefreshToken.for_user(user))}, status=status.HTTP_201_CREATED
        )
