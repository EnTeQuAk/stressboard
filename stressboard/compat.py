import time
from datetime import datetime, timedelta
from hashlib import md5

from django.conf import settings
from django.contrib.humanize.templatetags.humanize import naturaltime

from loads.db import get_database
from loads.transport.client import Client


_COUNTS = frozenset((
    'addError', 'addSuccess', 'stopTestRun', 'startTest',
    'startTestRun', 'stopTest', 'add_hit',
    'socket_open', 'socket_message', 'socket_close',
    'socket_message'
))


class Controller(object):

    def __init__(self):
        self.db = get_database(
            settings.LOADS_DATABASE['backend'],
            **settings.LOADS_DATABASE['options']
        )
        self.client = Client(settings.LOADS_BROKER)

    def stop(self, run_id):
        self.client.stop_run(run_id)
        self.get_broker_info()

    def ping_db(self):
        return self.db.ping()

    def get_broker_info(self):
        return self.client.ping()

    def get_runs(self, **filters):
        if not filters:
            return self.db.get_runs()

        runs = []

        for run in self.db.get_runs():
            info = self.get_run_info(run)
            for key, value in filters.items():
                if key not in info['metadata']:
                    continue
                else:
                    if info['metadata'][key] == value:
                        runs.append(run)

        return runs

    def get_run_info(self, run_id, data=True):
        result = {}
        if data:
            data = self.db.get_data(run_id, size=100)
            # Make it easier to serialize so a list is better than a generator
            result['data'] = list(data)
            errors = {}

            lines = self.db.get_data(run_id, data_type='addError', size=100)
            for line in lines:
                error, tb, tb2 = line['exc_info']
                hashed = md5(error).hexdigest()
                if hashed in errors:
                    old_count, tb = errors[hashed]
                    errors[hashed] = old_count + 1, tb
                else:
                    errors[hashed] = 1, tb + '\n' + tb2

            errors = errors.items()
            errors.sort()
            result['errors'] = errors

        counts = self.db.get_counts(run_id)
        custom = {}
        for key, value in list(counts.items()):
            if key in _COUNTS:
                continue
            custom[key] = value
            del counts[key]

        result['custom'] = custom

        metadata = self.db.get_metadata(run_id)
        started = metadata.get('started')
        ended = metadata.get('ended', time.time())
        active = metadata.get('active', False)

        # aproximative = should be set by the broker
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

            #TODO: Move to template
            started = datetime.fromtimestamp(int(started))
            metadata['started'] = started.strftime('%Y-%m-%d %H:%M:%S')
            counts['rps'] = int(rps)
            counts['elapsed'] = naturaltime(elapsed)
            ended = started + timedelta(seconds=elapsed)
            counts['finished'] = naturaltime(ended)
            counts['success'] = counts.get('addError', 0) == 0
            metadata['style'] = counts['success'] and 'green' or 'red'
        else:
            metadata['started'] = 'N/A'
            counts['rps'] = 0
            counts['elapsed'] = 0
            counts['finished'] = 'N/A'
            counts['success'] = False
            metadata['style'] = 'red'


        if metadata.get('active', False):
            metadata['active_label'] = 'Running'
        else:
            metadata['active_label'] = 'Ended'

        result['counts'] = counts
        result['metadata'] = metadata
        return result
