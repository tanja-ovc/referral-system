from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from users.api.v1.serializers.open_api_examples import phone_users_profile_404
from users.api.v1.serializers.profile import PhoneUsersProfileSerializer
from users.models import PhoneUser


@extend_schema(
    responses={200: PhoneUsersProfileSerializer,
               404: phone_users_profile_404},
    tags=['Профили пользователей'],
    summary='Получение профиля пользователя'
)
@api_view(('GET',))
def users_profile(request, *args, **kwargs):
    phone_user_id = kwargs['id']
    phone_user = get_object_or_404(PhoneUser, id=phone_user_id)
    serializer = PhoneUsersProfileSerializer(phone_user)
    return Response(serializer.data, status=status.HTTP_200_OK)
