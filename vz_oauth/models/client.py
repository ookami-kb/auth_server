# -*- coding: utf-8 -*
from django.db import models

class Client(models.Model):
    redirect_uri = models.URLField(u'Redirect URI', max_length=255)
    client_secret = models.CharField(u'Секретный код', max_length=255)
    
    class Meta:
        app_label =  'vz_oauth'