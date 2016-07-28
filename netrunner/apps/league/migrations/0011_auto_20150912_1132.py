# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0010_auto_20150912_1126'),
    ]

    operations = [
        migrations.CreateModel(
            name='MeetupLeague',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('start_date', models.DateTimeField(default='2015-08-31 15:18')),
                ('end_date', models.DateTimeField(default='2015-08-31 15:18')),
                ('elo_starting_points', models.IntegerField(default=1500)),
            ],
        ),
        migrations.AlterField(
            model_name='leagueplayer',
            name='league',
            field=models.ForeignKey(to='league.MeetupLeague', related_name='league'),
        ),
        migrations.DeleteModel(
            name='League',
        ),
    ]
