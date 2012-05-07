from .models import UserProfile
from django.contrib import admin

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone')
admin.site.register(UserProfile, ProfileAdmin)
