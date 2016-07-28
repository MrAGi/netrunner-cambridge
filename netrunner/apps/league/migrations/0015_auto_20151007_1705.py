# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0014_auto_20150926_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='leaguestatus',
            name='corp_timed_wins',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='leaguestatus',
            name='flatline_wins',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='leaguestatus',
            name='mill_wins',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='leaguestatus',
            name='runner_timed_wins',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
