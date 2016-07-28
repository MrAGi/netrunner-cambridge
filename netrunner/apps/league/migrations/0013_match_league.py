# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0012_auto_20150912_1135'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='league',
            field=models.ForeignKey(to='league.MeetupLeague', default=2, related_name='match_league'),
            preserve_default=False,
        ),
    ]
