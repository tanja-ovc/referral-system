from django.contrib import admin

from users.models import InviteCode, PhoneUser


@admin.register(InviteCode)
class InviteCodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'invite_code', 'code_owner')


@admin.register(PhoneUser)
class PhoneUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone', 'confirmation_code', 'is_authenticated',
                    'owned_invite_code', 'activated_invite_code')
