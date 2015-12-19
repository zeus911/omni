from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    'asset.views',
    url(r'^$|^index\.html$', 'index'),
    url(r'^login\.html$', 'login'),
    url(r'^logout\.htm$', 'logout'),
)