# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0011_auto_20150912_1132'),
    ]

    operations = [
        migrations.AddField(
            model_name='meetupleague',
            name='registration_end_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 12, 10, 35, 28, 862660, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='meetupleague',
            name='registration_start_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 12, 10, 35, 35, 822659, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='meetupleague',
            name='end_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='meetupleague',
            name='start_date',
            field=models.DateTimeField(),
        ),
    ]
