import time

from django.db import transaction
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from users.api.v1.serializers.open_api_examples import (
    confirm_code_examples, confirm_code_response_200,
    confirm_code_response_400, phone_sign_in_responses
)
from users.api.v1.serializers.auth import (
    ConfirmCodeSerializer, PhoneSignInSerializer
)
from users.models import PhoneUser


@extend_schema(
    request=PhoneSignInSerializer,
    responses=phone_sign_in_responses,
    tags=['Авторизация'],
    summary='Отправка номера телефона для получения кода подтверждения '
            'для авторизации'
)
@api_view(('POST',))
def phone_signin(request):
    serializer = PhoneSignInSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    time.sleep(2)
    return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    request=ConfirmCodeSerializer,
    responses={200: confirm_code_response_200,
               400: confirm_code_response_400},
    examples=confirm_code_examples,
    tags=['Авторизация'],
    summary='Отправка полученного кода подтверждения для авторизации'
)
@api_view(('POST',))
@transaction.atomic
def confirm_code(request):
    serializer = ConfirmCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    phone_user = PhoneUser.objects.filter(
        confirmation_code=serializer.data['confirmation_code'],
    ).first()
    if phone_user is None:
        return Response({
            'detail': 'Такого кода подтверждения не существует.'
        }, status=status.HTTP_400_BAD_REQUEST)
    phone_user.is_authenticated = True
    phone_user.save()
    return Response({
        'detail': 'Вы успешно вошли в систему.'
    }, status=status.HTTP_200_OK)
