from django.conf.urls import patterns, include, url
from .views import NodeGroupListView

urlpatterns = patterns(
    '',
    url(r'^$|^index\.html$', NodeGroupListView.as_view()),
)
