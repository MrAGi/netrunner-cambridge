# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0002_remove_gameresult_validated'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameresult',
            name='validated',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
