import json

from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from agent.models import Sighting


@csrf_exempt
def report(request):
    if request.method == 'POST' and request.is_ajax():
        data = json.loads(request.body)

        if 'sightings' in data and data['sightings']:
            sightings = []

            for s in data['sightings']:
                if (s.get('host') is not None
                and s.get('device_id') is not None
                and s.get('timestamp') is not None
                and s.get('signal_dbm') is not None):
                    sightings.append(Sighting(
                        host=s.get('host'),
                        device_id=s.get('device_id'),
                        timestamp=s.get('timestamp'),
                        signal_dbm=s.get('signal_dbm')))

            # create new sightings from the request
            if sightings:
                Sighting.objects.bulk_create(sightings)
                return HttpResponse()

    return HttpResponseBadRequest()
