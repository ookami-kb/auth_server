# -*- coding: utf-8 -*
from django.contrib import admin
from .models import Client

class ClientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'redirect_uri')
    
admin.site.register(Client, ClientAdmin)