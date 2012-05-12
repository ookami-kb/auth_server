# -*- coding: utf-8 -*
from django.contrib import admin
from .models import Client, AccessToken, RequestToken

class ClientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'redirect_uri')
    
admin.site.register(Client, ClientAdmin)

class AccessTokenAdmin(admin.ModelAdmin):
    list_display = ('access_token', 'expires_in')
    
admin.site.register(AccessToken, AccessTokenAdmin)

class RequestTokenAdmin(admin.ModelAdmin):
    list_display = ('request_token', 'used')
    
admin.site.register(RequestToken, RequestTokenAdmin)