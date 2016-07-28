# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0009_auto_20150912_1000'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='league',
            name='registration_closed_date',
        ),
        migrations.RemoveField(
            model_name='league',
            name='registration_open_date',
        ),
    ]
