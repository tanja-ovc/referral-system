from django.db import transaction
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from users.api.v1.serializers.open_api_examples import (
    activate_invite_code_examples, activate_invite_code_responses
)
from users.api.v1.serializers.invite import ActivateInviteCodeSerializer
from users.models import InviteCode, PhoneUser


@extend_schema(
    request=ActivateInviteCodeSerializer,
    responses=activate_invite_code_responses,
    examples=activate_invite_code_examples,
    tags=['Инвайты'],
    summary='Активация invite-кода'
)
@api_view(('POST',))
@transaction.atomic
def activate_invite_code(request, *args, **kwargs):
    serializer = ActivateInviteCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    invite_code_db = InviteCode.objects.filter(
        invite_code=serializer.data['invite_code']
    ).first()
    if invite_code_db is None:
        return Response(
            {'detail': 'Такого invite-кода не существует.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    phone_user_id = kwargs['id']
    phone_user = get_object_or_404(PhoneUser, id=phone_user_id)
    if phone_user.activated_invite_code is not None:
        return Response(
            {'detail': 'Данный пользователь уже активировал invite-код.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    if invite_code_db == phone_user.owned_invite_code:
        return Response(
            {'detail': 'Пользователю нельзя активировать собственный invite-код.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    phone_user.activated_invite_code = invite_code_db
    phone_user.save()
    return Response(
        {'detail': 'Invite-код активирован.'},
        status=status.HTTP_200_OK
    )
