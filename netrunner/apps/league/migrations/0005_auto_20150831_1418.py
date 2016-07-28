# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('league', '0004_league'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeaguePlayer',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='LeagueStatus',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('overall_elo_points', models.IntegerField()),
                ('corp_elo_points', models.IntegerField()),
                ('runner_elo_points', models.IntegerField()),
                ('corp_wins', models.IntegerField()),
                ('runner_wins', models.IntegerField()),
                ('corp_loses', models.IntegerField()),
                ('runner_loses', models.IntegerField()),
                ('player', models.ForeignKey(related_name='player_status', to='league.LeaguePlayer')),
                ('unique_opponents', models.ManyToManyField(db_index=True, related_name='unique_opponents', to='league.LeaguePlayer')),
            ],
        ),
        migrations.AddField(
            model_name='league',
            name='elo_starting_points',
            field=models.IntegerField(default=1500),
        ),
        migrations.AddField(
            model_name='league',
            name='end_date',
            field=models.DateTimeField(default='2015-08-31 15:18'),
        ),
        migrations.AddField(
            model_name='league',
            name='start_date',
            field=models.DateTimeField(default='2015-08-31 15:18'),
        ),
        migrations.AlterField(
            model_name='match',
            name='date',
            field=models.DateTimeField(),
        ),
        migrations.AddField(
            model_name='leagueplayer',
            name='league',
            field=models.ForeignKey(related_name='league', to='league.League'),
        ),
        migrations.AddField(
            model_name='leagueplayer',
            name='player',
            field=models.ForeignKey(related_name='player', to=settings.AUTH_USER_MODEL),
        ),
    ]
