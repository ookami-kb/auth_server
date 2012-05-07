from django.conf.urls import patterns, url
urlpatterns = patterns('vz_oauth.views',
    url(r'^authorize/', 'oauth_authorize'),
)
