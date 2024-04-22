from rest_framework import serializers

from users.api.v1.validators import validate_invite_code
from users.models import InviteCode


class ActivateInviteCodeSerializer(serializers.ModelSerializer):
    invite_code = serializers.CharField(validators=[validate_invite_code])

    class Meta:
        model = InviteCode
        fields = ('invite_code',)


class InviteCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InviteCode
        fields = '__all__'
