# Generated by Django 4.2.4 on 2023-09-05 22:56

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0003_entry_user_alter_entry_content'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Entry',
            new_name='Entries',
        ),
    ]