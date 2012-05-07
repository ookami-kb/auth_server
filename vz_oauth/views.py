# -*- coding: utf-8 -*
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.models import get_current_site
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from .models import Client
import re
import urlparse

@csrf_protect
@never_cache
def oauth_authorize(request):
    client_id = request.GET.get('client_id', None)
    if not client_id:
        return HttpResponseBadRequest('Missing client_id')
    redirect_uri = request.GET.get('redirect_uri', None)
    if not redirect_uri:
        return HttpResponseBadRequest('Missing redirect_uri')
    try:
        client = Client.objects.get(pk=client_id)
    except Client.DoesNotExist:
        return HttpResponseBadRequest('Wrong client_id')
    if re.match(r'^%s.*' % client.redirect_uri, redirect_uri) is None:
        return HttpResponseBadRequest('Wrong redirect_uri')

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            redirect_to = urlparse.urlparse(redirect_uri)

            auth_login(request, form.get_user())

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

            return HttpResponseRedirect('%s://%s%s' % (redirect_to.scheme,
                                                       redirect_to.netloc,
                                                       redirect_to.path))
    else:
        form = AuthenticationForm(request)

    request.session.set_test_cookie()

    current_site = get_current_site(request)

    context = {
        'form': form,
        REDIRECT_FIELD_NAME: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    return TemplateResponse(request, 'registration/login.html', context)