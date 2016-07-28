# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0008_auto_20150831_1425'),
    ]

    operations = [
        migrations.AddField(
            model_name='league',
            name='registration_closed_date',
            field=models.DateTimeField(default='2015-08-31 15:18'),
        ),
        migrations.AddField(
            model_name='league',
            name='registration_open_date',
            field=models.DateTimeField(default='2015-08-31 15:18'),
        ),
    ]
