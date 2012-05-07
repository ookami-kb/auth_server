from django.conf.urls import patterns, include, url
from django.contrib import admin
from registration.forms import RegistrationFormUniqueEmail

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'auth_server.views.home', name='home'),
    # url(r'^auth_server/', include('auth_server.foo.urls')),

    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^oauth/', include('vz_oauth.urls')),
    
    url(r'^register/$', 'registration.views.register', 
        {'form_class': RegistrationFormUniqueEmail,
         'backend': 'registration.backends.default.DefaultBackend'}, name='registration_register'),
    (r'', include('registration.urls')),
    
    (r'^accounts/', include('profile.urls')),
    
)

