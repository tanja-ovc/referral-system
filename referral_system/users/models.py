from django.db import models
from django.db.models import F, Q

from users.api.v1.validators import (
    validate_confirmation_code, validate_invite_code, validate_phone,
)


class InviteCode(models.Model):
    invite_code = models.CharField(
        'invite-код',
        validators=[validate_invite_code],
        max_length=6,
        unique=True,
        help_text=('Формат invite-кода: 6 символов, только цифры или '
                   'латинские буквы (строчные или заглавные).'),
    )

    class Meta:
        verbose_name = 'invite-код'
        verbose_name_plural = 'invite-коды'

    def __str__(self):
        return self.invite_code


class PhoneUser(models.Model):
    phone = models.CharField(
        'номер телефона',
        validators=[validate_phone],
        max_length=12,
        unique=True,
        help_text='Формат номера: 89991112233 либо +79991112233.',
    )
    confirmation_code = models.CharField(
        'код подтверждения',
        validators=[validate_confirmation_code],
        max_length=4,
    )
    is_authenticated = models.BooleanField('аутентифицирован?', default=False)
    owned_invite_code = models.OneToOneField(
        InviteCode,
        on_delete=models.PROTECT,
        related_name='code_owner',
        verbose_name='присвоенный invite-код',
    )
    activated_invite_code = models.ForeignKey(
        InviteCode,
        on_delete=models.PROTECT,
        related_name='code_activators',
        verbose_name='активированный invite-код',
        blank=True,
        null=True,
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=~Q(owned_invite_code=F('activated_invite_code')),
                name='owned_invite_code_activation_constraint',
                violation_error_message='Пользователю нельзя активировать '
                                        'собственный invite-код.'
            ),
        ]
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи (по номерам телефонов)'

    def __str__(self):
        return self.phone
