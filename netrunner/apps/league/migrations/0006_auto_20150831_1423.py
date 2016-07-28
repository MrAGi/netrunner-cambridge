# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0005_auto_20150831_1418'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='leagueplayer',
            unique_together=set([('league', 'player')]),
        ),
    ]
