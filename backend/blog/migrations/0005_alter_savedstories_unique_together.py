# Generated by Django 4.0.6 on 2022-08-06 19:17

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0004_alter_tagfollower_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='savedstories',
            unique_together={('user', 'story')},
        ),
    ]
