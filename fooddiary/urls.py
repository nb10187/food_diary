from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^diary/', include('diary.urls', namespace="diary")),
    url(r'^admin/', include(admin.site.urls)),
)