from django.conf.urls import patterns, include, url
from django.contrib import admin
from registration.forms import RegistrationFormUniqueEmail

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('auth_client.urls')),
    
    url(r'^oauth/', include('vz_oauth.urls')),
    
    url(r'^register/$', 'registration.views.register', 
        {'form_class': RegistrationFormUniqueEmail,
         'backend': 'registration.backends.default.DefaultBackend'}, name='registration_register'),
    (r'', include('registration.urls')),
    
    (r'^accounts/', include('profile.urls')),
    
)

