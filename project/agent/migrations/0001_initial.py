# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NormalizedSighting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('host', models.CharField(max_length=32)),
                ('device_id', models.CharField(max_length=32)),
                ('signal_low', models.IntegerField()),
                ('signal_high', models.IntegerField()),
                ('signal_avg', models.IntegerField()),
                ('num_samples', models.IntegerField()),
                ('timestamp', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sighting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('host', models.CharField(max_length=32)),
                ('device_id', models.CharField(max_length=32)),
                ('signal_dbm', models.IntegerField()),
                ('timestamp', models.IntegerField(db_index=True)),
                ('normalize_processed', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
