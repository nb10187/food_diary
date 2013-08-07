from django.conf.urls import patterns, include, url 

from django.contrib import admin
admin.autodiscover()

from diary import views
#diary_entry_id

urlpatterns = patterns('',
    # ex: /polls/
    url(r'^$', views.index, name='index'),
    # ex: /polls/5//diary/gallery
    url(r'^(?P<diary_entry_id>\d+)/$', views.detail, name='detail'),
    # ex: /polls/5/results/
    url(r'^(?P<diary_entry_id>\d+)/results/$', views.results, name='results'),
    # ex: /polls/5/vote/
    url(r'^(?P<diary_entry_id>\d+)/enter/$', views.enter, name='enter'),
    url(r'^gallery/$', views.gallery, name='gallery'),
    url(r'^history/$', views.history, name='history'),
    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detailview'),
    url(r'^create/$', views.create, name='create'),
    url(r'^accounts/login/$', views.login, name='login'),
    url(r'^accounts/login/auth_view/$', views.auth_view, name='auth_view'),
    url(r'^accounts/logout/$', views.logout, name='logout'),
    url(r'^accounts/loggedin/$', views.loggedin, name='loggedin'),
    url(r'^accounts/invalid/$', views.invalid_login, name='invalid_login'),
    #url(r'^accounts/register/$', views.register_user, name='register_user'),
    url(r'^accounts/register_success/$', views.register_success, name='register_success'),
    
    url(r'^admin/', include(admin.site.urls)),
)