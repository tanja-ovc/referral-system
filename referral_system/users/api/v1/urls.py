from django.urls import path

from users.api.v1.views.auth import confirm_code, phone_signin
from users.api.v1.views.invite import activate_invite_code
from users.api.v1.views.profile import users_profile

urlpatterns = [
    path('auth/phone/', phone_signin),
    path('auth/phone/confirm/', confirm_code),
    path('users/<int:id>/profile/', users_profile),
    path('users/<int:id>/activate_invite_code/', activate_invite_code),
]
