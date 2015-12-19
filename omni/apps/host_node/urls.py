from django.conf.urls import patterns, include, url
from .views import NodeAndGroupListView

urlpatterns = patterns(
    '',
    url(r'^$|^index\.html$', NodeAndGroupListView.as_view()),
)
