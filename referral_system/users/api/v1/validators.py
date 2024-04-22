import re

from django.core.exceptions import ValidationError


def validate_phone(value):
    """Валидирует российский мобильный номер."""
    pattern = re.compile(r'^\+?\d{11}$')
    if re.fullmatch(pattern, value) is None:
        raise ValidationError(
            ('Некорректный номер. Допустимые форматы: '
             '89991112233 либо +79991112233.'),
            params={'value': value},
        )


def validate_confirmation_code(value):
    pattern = re.compile(r'^[0-9]{4}$')
    if re.fullmatch(pattern, value) is None:
        raise ValidationError(
            ('Некорректный код подтверждения. Проверьте, что вводите '
             '4-значный код, содержащий только цифры.'),
            params={'value': value},
        )


def validate_invite_code(value):
    pattern = re.compile(r'^[0-9a-zA-Z]{6}$')
    if re.fullmatch(pattern, value) is None:
        raise ValidationError(
            ('Некорректный invite-код. Проверьте, что вводите 6-значный '
             'код, содержащий только цифры или латинские буквы (строчные '
             'или заглавные).'),
            params={'value': value},
        )
