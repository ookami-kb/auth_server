# -*- coding: utf-8 -*
from .models import UserProfile
from .forms import ProfileForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext

@login_required
def profile(request):
    try:
        profile = request.user.get_profile()
    except ObjectDoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
        
    if request.POST:
        form = ProfileForm(instance=profile, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = ProfileForm(instance=profile)
    return render_to_response('profile/profile.html', {'form': form},
                              RequestContext(request))        