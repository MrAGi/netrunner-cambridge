# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0007_auto_20150831_1424'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='leaguestatus',
            options={'verbose_name_plural': 'league statuses'},
        ),
    ]
