# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0001_initial'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='sighting',
            index_together=set([('normalize_processed', 'host', 'device_id', 'timestamp')]),
        ),
    ]
