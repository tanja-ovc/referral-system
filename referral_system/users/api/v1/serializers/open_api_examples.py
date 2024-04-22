from drf_spectacular.utils import inline_serializer, OpenApiExample
from rest_framework import serializers

phone_sign_in_responses = {
    200: inline_serializer(
        name='PhoneNumberSent',
        fields={
            'detail': serializers.CharField(
                default='Код подтверждения отправлен по указанному номеру.'
            ),
            'confirmation_code': serializers.CharField(default='1111')
        }
    ),
    400: inline_serializer(
        name='IncorrectPhoneNumber',
        fields={
            'phone': serializers.ListField(
                default=['Некорректный номер. Допустимые форматы: 89991112233 '
                         'либо +79991112233.'],
            )
        },
    ),
}

phone_sign_in_examples = [
    OpenApiExample(
        'Ввод номера телефона',
        value={
            'phone': '+79991112233',
        },
        request_only=True,
    ),
    OpenApiExample(
        'Номер телефона отправлен',
        status_codes=[200],
        value={
            'detail': 'Код подтверждения отправлен по указанному номеру.',
            'confirmation_code': '1111'
        },
        response_only=True,
    ),
    OpenApiExample(
        'Некорректный номер',
        status_codes=[400],
        value={
            'phone': [
                'Некорректный номер. Допустимые форматы: 89991112233 '
                'либо +79991112233.'
            ]
        },
        response_only=True,
    ),
]

confirm_code_response_200 = inline_serializer(
        name='LoginSuccessful',
        fields={
            'detail': serializers.CharField(
                default='Вы успешно вошли в систему.'
            )
        }
    )

confirm_code_response_400 = inline_serializer(
        name='Error',
        fields={
            'detail': serializers.CharField(
                default='Текст ошибки.'
            )
        },
    )

confirm_code_examples = [
    OpenApiExample(
        'Ввод кода подтверждения',
        value={
            'confirmation_code': '1111',
        },
        request_only=True,
    ),
    OpenApiExample(
        'Успешный вход',
        status_codes=[200],
        value={
            'detail': 'Вы успешно вошли в систему.',
        },
        response_only=True,
    ),
    OpenApiExample(
        'Некорректный код подтверждения',
        status_codes=[400],
        value={
            'confirmation_code': [
                'Некорректный код подтверждения. Проверьте, что вводите '
                '4-значный код, содержащий только цифры.'
            ]
        },
        response_only=True,
    ),
    OpenApiExample(
        'Код подтверждения не существует',
        status_codes=[400],
        value={
            'detail': 'Такого кода подтверждения не существует.'
        },
        response_only=True,
    ),
]

activate_invite_code_responses = {
    200: inline_serializer(
        name='InviteCodeActivated',
        fields={
            'detail': serializers.CharField(
                default='Invite-код активирован.'
            )
        }
    ),
    404: inline_serializer(
        name='PhoneUserDoesNotExist',
        fields={
            'detail': serializers.CharField(
                default='No PhoneUser matches the given query.'
            )
        }
    ),
    400: inline_serializer(
        name='Error',
        fields={
            'detail': serializers.CharField(
                default='Текст ошибки.'
            )
        }
    ),
}

activate_invite_code_examples = [
    OpenApiExample(
        'Ввод invite-кода для активации',
        value={
            'invite_code': 'sJ8Hk0',
        },
        request_only=True,
    ),
    OpenApiExample(
        'Invite-код активирован',
        status_codes=[200],
        value={
            'detail': 'Invite-код активирован.',
        },
        response_only=True,
    ),
    OpenApiExample(
        'Некорректный invite-код',
        status_codes=[400],
        value={
            'invite_code': [
                'Некорректный invite-код. Проверьте, что вводите '
                '6-значный код, содержащий только цифры или латинские '
                'буквы (строчные или заглавные).'
            ]
        },
        response_only=True,
    ),
    OpenApiExample(
        'Invite-код не существует',
        status_codes=[400],
        value={
            'detail': 'Такого invite-кода не существует.'
        },
        response_only=True,
    ),
    OpenApiExample(
        'Повторная активация',
        status_codes=[400],
        value={
            'detail': 'Данный пользователь уже активировал invite-код.'
        },
        response_only=True,
    ),
    OpenApiExample(
        'Активация собственного invite-кода',
        status_codes=[400],
        value={
            'detail': 'Пользователю нельзя активировать собственный invite-код.'
        },
        response_only=True,
    ),
    OpenApiExample(
        'Пользователь не существует',
        status_codes=[404],
        value={
            'detail': 'No PhoneUser matches the given query.'
        },
        response_only=True,
    ),
]

phone_users_profile_404 = inline_serializer(
    name='PhoneUserDoesNotExist',
    fields={
        'detail': serializers.CharField(
            default='No PhoneUser matches the given query.'
        )
    }
)

phone_users_profile_examples = [
    OpenApiExample(
        'Профиль получен',
        status_codes=[200],
        value={
            'id': 1,
            'phone': '+79991112233',
            'confirmation_code': '5171',
            'is_authenticated': True,
            'owned_invite_code': {
                'id': 1,
                'invite_code': '5HbcDQ'
            },
            'activated_invite_code': {
                'id': 2,
                'invite_code': 'h9yjks'
            },
            'invite_code_activators': [
                {
                    'phone': '89901102200'
                },
                {
                    'phone': '+79851527989'
                }
            ]
        },
        response_only=True,
    ),
    OpenApiExample(
        'Пользователь не существует',
        status_codes=[404],
        value={
            'detail': 'No PhoneUser matches the given query.'
        },
        response_only=True,
    ),
]
