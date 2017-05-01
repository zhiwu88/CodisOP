
from django.conf.urls import url
from django.contrib import admin
from codisapp.views import *

urlpatterns = [
    url(r'^$',index),
    url(r'^search/$',search),
    url(r'^monitor/$',monitor),
    url(r'^login/$', login),
    url(r'^login2system/$', login2System),
    url(r'^logout/$', logout),
    url(r'^used/$', used),
    url(r'^unused/$', unused),
    url(r'unused/addhost/$', addHost),
    url(r'^unused/addhost2db/$', addHost2db),
    url(r'unused/delhost/(?P<hostID>([\w]*))/$', delHost),
    url(r'unused/updatehost/(?P<hostID>([\w]*))/$', updateHost),
    url(r'^dashboard/(.+)/$', dashboardurl),
    url(r'^dashboard_new/(.+)/$', dashboardurl_new),
    url(r'^addcodis/$', addCodis),
    url(r'^addcodis2db/$', addCodis2db),
    url(r'^delcodis/(?P<hostID>([\w]*))/$', delCodis),
    url(r'^updatecodis/(?P<codisID>([\w]*))/$', updateCodis),
    url(r'^updatecodis2db/$', updateCodis2DB),
    url(r'^codisinfo/$', codisInfo),
    url(r'^codiscounter/$', codisCounter),
    url(r'^publiccounter/$', publicCounter),
    url(r'^public/noprefix/$', publicNoPrefix),
    url(r'^bigkey/(.+)/$', BigKey),
    url(r'^addprefix/$', addPrefix),
    url(r'^addprefix2db/$', addPrefix2db),
    url(r'^prefixlist/$', prefixList),   
    url(r'^delprefix/(?P<prefixID>([\w]*))/$', delPrefix),
    url(r'^Report/ClusterReport/$', ClusterReport),
    url(r'^Report/BigKvReport/$', BigKvReport),
    url(r'^Report/BigKvDetailReport/$', BigKvDetailReport)

    
]
