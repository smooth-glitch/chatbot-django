# Generated by Django 5.1 on 2024-08-14 22:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chatAPI', '0006_merge_0004_login_phone_0005_alter_contact_phone'),
    ]

    operations = [
        migrations.RenameField(
            model_name='login',
            old_name='timestamp',
            new_name='last_login',
        ),
    ]