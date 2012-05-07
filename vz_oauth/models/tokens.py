# -*- coding: utf-8 -*
from django.db import models
from django.contrib.auth.models import User
from vz_oauth.models.client import Client

class AccessToken(models.Model):
    access_token = models.CharField(u'Access Token', max_length=255, unique=True)
    expires_in = models.IntegerField(u'Expires in')
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    
    class Meta:
        app_label =  'vz_oauth'
    
class RequestToken(models.Model):
    request_token = models.CharField(u'Request Token', max_length=255, unique=True)
    client = models.ForeignKey(Client)
    used = models.BooleanField(default=False)
    user = models.ForeignKey(User)
    
    class Meta:
        app_label =  'vz_oauth'
    