from django.conf.urls import patterns, include, url
from django.contrib import admin
from snapshot import views

urlpatterns = patterns('',
  url(r'^admin/', include(admin.site.urls)),
  url(r'^login/$', views.login),
  url(r'^register/$', views.register),
  url(r'^create/$', views.create),
  url(r'^list/$', views.list),
)
