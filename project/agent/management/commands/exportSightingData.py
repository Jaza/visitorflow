from django.core.management.base import LabelCommand, CommandError
from agent.models import Sighting
import csv


class Command(LabelCommand):
    args = '<filename>'
    label = 'filename'
    help = 'Export and process sighting data'

    def handle_label(self, label, **options):
        file = open(label, 'w')
        writer = csv.writer(file, delimiter=',', quotechar='"')
        pingCount = 0
        dbmTotal = 0
        previousDeviceId = ''
        timeTotal = 0

        for sighting in Sighting.objects.all():
            if sighting.device_id == previousDeviceId or previousDeviceId == '':
                pingCount += 1
                dbmTotal += sighting.signal_dbm
                timeTotal += sighting.timestamp
            else:
                writer.writerow([previousDeviceId, pingCount, dbmTotal / pingCount, timeTotal / pingCount])
                pingCount = 1
                dbmTotal = sighting.signal_dbm
                timeTotal = sighting.timestamp

            previousDeviceId = sighting.device_id
