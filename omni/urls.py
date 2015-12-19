from django.conf.urls import patterns, include, url
from .apps.salt import urls as omni_salt_urls
from .apps.host_node import urls as omni_host_urls

urlpatterns = patterns(
    'omni.views',
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$|^index\.html$', 'index'),
    url(r'^login\.html$', 'login'),
    url(r'^logout\.htm$', 'logout'),
)

urlpatterns += patterns(
    '',
    url(r'^salt/', include(omni_salt_urls))
)

urlpatterns += patterns(
    '',
    url(r'^host/', include(omni_host_urls))
)

# urlpatterns += patterns(
#     '',
#     url(r'^asset/', include(asset_urls))
# )
