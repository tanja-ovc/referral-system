import random
import secrets
import string

from django.db import transaction
from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers

from users.api.v1.serializers.open_api_examples import (
    phone_sign_in_examples
)
from users.api.v1.validators import validate_confirmation_code, validate_phone
from users.models import InviteCode, PhoneUser


@extend_schema_serializer(examples=phone_sign_in_examples)
class PhoneSignInSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(validators=[validate_phone])

    class Meta:
        model = PhoneUser
        fields = ('phone',)

    @transaction.atomic
    def create(self, validated_data):
        phone_user, created = PhoneUser.objects.get_or_create(
            phone=validated_data['phone']
        )
        if created:
            characters = string.digits + string.ascii_letters
            generated_invite_code = ''.join(
                secrets.choice(characters) for _ in range(6)
            )
            while InviteCode.objects.filter(
                    invite_code=generated_invite_code
            ).exists():
                generated_invite_code = ''.join(
                    secrets.choice(characters) for _ in range(6)
                )
            phone_user.owned_invite_code = InviteCode.objects.create(
                invite_code=generated_invite_code
            )
            phone_user.save()
        generated_confirmation_code = random.randint(1000, 9999)
        while PhoneUser.objects.filter(
                confirmation_code=generated_confirmation_code
        ).exists():
            generated_confirmation_code = random.randint(1000, 9999)
        phone_user.confirmation_code = generated_confirmation_code
        phone_user.save()
        return phone_user

    def to_representation(self, instance):
        return {
            'detail': 'Код подтверждения отправлен по указанному номеру.',
            'confirmation_code': instance.confirmation_code
        }


class ConfirmCodeSerializer(serializers.Serializer):
    confirmation_code = serializers.CharField(
        validators=[validate_confirmation_code]
    )
