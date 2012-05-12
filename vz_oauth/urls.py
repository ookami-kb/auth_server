from django.conf.urls import patterns, url
urlpatterns = patterns('vz_oauth.views',
    url(r'^authorize/', 'oauth_authorize'),
    url(r'^get_access_token/', 'get_access_token'),
    url(r'^get_user_data/', 'get_user_data'),
)
