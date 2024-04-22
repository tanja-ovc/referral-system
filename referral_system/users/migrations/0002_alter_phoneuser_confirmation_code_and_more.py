# Generated by Django 4.2 on 2024-04-22 19:09

from django.db import migrations, models
import django.db.models.deletion
import users.api.v1.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phoneuser',
            name='confirmation_code',
            field=models.CharField(max_length=4, validators=[users.api.v1.validators.validate_confirmation_code], verbose_name='код подтверждения'),
        ),
        migrations.AlterField(
            model_name='phoneuser',
            name='owned_invite_code',
            field=models.OneToOneField(default=333333, on_delete=django.db.models.deletion.PROTECT, related_name='code_owner', to='users.invitecode', verbose_name='присвоенный invite-код'),
            preserve_default=False,
        ),
    ]
