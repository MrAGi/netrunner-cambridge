# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Faction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='FactionType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='GameResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('player_one_agenda_points', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(7), django.core.validators.MinValueValidator(0)])),
                ('player_two_agenda_points', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(7), django.core.validators.MinValueValidator(0)])),
                ('validated', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Identity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=100)),
                ('faction', models.ForeignKey(related_name='faction', to='league.Faction')),
            ],
            options={
                'verbose_name_plural': 'identities',
            },
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('date', models.DateField()),
                ('player_one', models.ForeignKey(related_name='player_one', to=settings.AUTH_USER_MODEL)),
                ('player_two', models.ForeignKey(related_name='player_two', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'matches',
            },
        ),
        migrations.CreateModel(
            name='WinType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='gameresult',
            name='pair',
            field=models.ForeignKey(related_name='match', to='league.Match'),
        ),
        migrations.AddField(
            model_name='gameresult',
            name='player_one_identity',
            field=models.ForeignKey(related_name='identity', to='league.Identity', null=True),
        ),
        migrations.AddField(
            model_name='gameresult',
            name='player_two_identity',
            field=models.ForeignKey(related_name='identity2', to='league.Identity', null=True),
        ),
        migrations.AddField(
            model_name='gameresult',
            name='win_type',
            field=models.ForeignKey(related_name='win_type', to='league.WinType'),
        ),
        migrations.AddField(
            model_name='faction',
            name='faction_type',
            field=models.ForeignKey(related_name='faction_type', to='league.FactionType'),
        ),
    ]
