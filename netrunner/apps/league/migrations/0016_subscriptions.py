# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('league', '0015_auto_20151007_1705'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscriptions',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('subscribed', models.BooleanField(default=False)),
                ('player', models.ForeignKey(related_name='subscribed_player', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
