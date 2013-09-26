from django.conf.urls import url, include, patterns

urlpatterns = patterns('',
    url(r'^$', 'stressboard.views.index', name='index'),
    url(r'^run/(?P<run_id>.*)', 'stressboard.views.run', name='run'),

    # API

    url(r'^api/run/(?P<run_id>.*)', 'stressboard.views.api_run'),
)
