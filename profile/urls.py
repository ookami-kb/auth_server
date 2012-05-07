from django.conf.urls import patterns, url

urlpatterns = patterns('profile.views',
    # Examples:
    # url(r'^$', 'auth_server.views.home', name='home'),
    # url(r'^auth_server/', include('auth_server.foo.urls')),

    url(r'^profile/', 'profile'),
)
