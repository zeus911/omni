from django.conf.urls import patterns, include, url
from .views.base import EnvInfoCreateView

urlpatterns = patterns(
    '',
    url(r'^$', EnvInfoCreateView.as_view())
)
