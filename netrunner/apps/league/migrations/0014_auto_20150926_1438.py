# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0013_match_league'),
    ]

    operations = [
        migrations.AddField(
            model_name='leaguestatus',
            name='corp_start_elo_rank',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='leaguestatus',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 26, 13, 38, 6, 339143, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='leaguestatus',
            name='league',
            field=models.ForeignKey(default=2, to='league.MeetupLeague', related_name='status_league'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='leaguestatus',
            name='overall_start_elo_rank',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='leaguestatus',
            name='runner_start_elo_rank',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='leaguestatus',
            unique_together=set([('league', 'player', 'date')]),
        ),
    ]
