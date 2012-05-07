# -*- coding: utf-8 -*
from django.db import models
import re

class Client(models.Model):
    redirect_uri = models.URLField(u'Redirect URI', max_length=255)
    client_secret = models.CharField(u'Секретный код', max_length=255)
    
    class Meta:
        app_label =  'vz_oauth'
        
    def valid_redirect_uri(self, redirect_uri):
        if re.match(r'^%s.*' % self.redirect_uri, redirect_uri) is None:
            return False
        return True