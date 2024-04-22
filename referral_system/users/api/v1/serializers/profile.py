from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers

from users.api.v1.serializers.invite import InviteCodeSerializer
from users.api.v1.serializers.open_api_examples import (
    phone_users_profile_examples
)
from users.models import PhoneUser


class PhoneUsersLiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneUser
        fields = ('phone',)


@extend_schema_serializer(examples=phone_users_profile_examples)
class PhoneUsersProfileSerializer(serializers.ModelSerializer):
    owned_invite_code = InviteCodeSerializer(read_only=True)
    activated_invite_code = InviteCodeSerializer(read_only=True)
    invite_code_activators = serializers.SerializerMethodField()

    class Meta:
        model = PhoneUser
        fields = ('id', 'phone', 'confirmation_code', 'is_authenticated',
                  'owned_invite_code', 'activated_invite_code',
                  'invite_code_activators')

    def get_invite_code_activators(self, obj):
        phone_user_obj = get_object_or_404(PhoneUser, id=obj.id)
        phone_users = PhoneUser.objects.filter(
            activated_invite_code=phone_user_obj.owned_invite_code
        )
        serializer = PhoneUsersLiteSerializer(phone_users, many=True)
        return serializer.data
