import json
from django.http import HttpResponse
from django.shortcuts import render
from stressboard.compat import Controller

from datetime import datetime, timedelta
import time


def index(request):
    controller = Controller()
    runs = controller.get_runs()
    return render(request, 'stressboard/index.html', {
        'runs': runs
    })


def run(request, run_id=None):
    controller = Controller()
    return render(request, 'stressboard/run.html', {
        'run_id': run_id
    })


def api_run(request, run_id=None):
    controller = Controller()
    #info = controller.get_run_info(run_id)
    metadata = controller.client.get_metadata(run_id)
    counts = dict(controller.client.get_counts(run_id))

    started = metadata.get('started')
    ended = metadata.get('ended', time.time())
    active = metadata.get('active', False)

    if started is not None:
        if active:
            elapsed = time.time() - started
        else:
            elapsed = ended - started

        hits = counts.get('add_hit', 0)
        if hits == 0:
            rps = 0
        else:
            rps = hits / elapsed

    data = {
        'run_id': run_id,
        #'info': info,
        #'active': info['metadata'].get('active', False),
        'counts': dict(counts),
        'rps': rps
    }

    return HttpResponse(json.dumps(data), mimetype="application/json")
