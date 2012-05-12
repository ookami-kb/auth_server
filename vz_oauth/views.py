# -*- coding: utf-8 -*
from .models import Client
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.models import get_current_site
from django.http import HttpResponseBadRequest, HttpResponseRedirect, \
    HttpResponse
from django.template.response import TemplateResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from vz_oauth.models.tokens import RequestToken, AccessToken
import simplejson
import time
import urlparse
import datetime
from django.utils.timezone import utc
from django.conf import settings
import hashlib

def get_user_data(request):
    at = request.GET.get('access_token', None)
    if at is None:
        return HttpResponseBadRequest('Missing access_token')
    try:
        access_token = AccessToken.objects.get(access_token=at)
    except AccessToken.DoesNotExist:
        return HttpResponseBadRequest('Wrong access_token')
    
    if access_token.created + datetime.timedelta(seconds=access_token.expires_in) < datetime.datetime.utcnow().replace(tzinfo=utc):
        return HttpResponseBadRequest('Access_token expired')
    
    user = access_token.user
    content = {
               'username': user.username,
               'first_name': user.first_name,
               'last_name': user.last_name,
               }
    try:
        profile = user.get_profile()
        content['phone'] = profile.phone
    except Exception as e:
        print e
    content = simplejson.dumps(content)
    return HttpResponse(content, mimetype='application/javascript')

@never_cache
def get_access_token(request):
    grant_type = request.GET.get('grant_type', None)
    if grant_type != 'authorization_code':
        return HttpResponseBadRequest('Wrong grant_type')
    code = request.GET.get('code', None)
    if code is None:
        return HttpResponseBadRequest('Missing code')
    redirect_uri = request.GET.get('redirect_uri', None)
    if not redirect_uri:
        return HttpResponseBadRequest('Missing redirect_uri')
    client_id = request.GET.get('client_id', None)
    if not client_id:
        return HttpResponseBadRequest('Missing client_id')
    client_secret = request.GET.get('client_secret', None)
    if not client_secret:
        return HttpResponseBadRequest('Missing client_secret')
    
    try:
        client = Client.objects.get(pk=client_id)
    except Client.DoesNotExist:
        return HttpResponseBadRequest('Wrong client_id')
    
    if client_secret != client.client_secret:
        return HttpResponseBadRequest('Client authorization failed')
    
    if not client.valid_redirect_uri(redirect_uri):
        return HttpResponseBadRequest('Wrong redirect_uri')
    
    try:
        request_token = RequestToken.objects.get(request_token=code)
    except RequestToken.DoesNotExist:
        return HttpResponseBadRequest('Wrong code')
    
    if request_token.used:
        return HttpResponseBadRequest('Token is used')
    
    if client != request_token.client:
        return HttpResponseBadRequest('Client mismatch')
    
    request_token.used = True
    request_token.save()
    
    # создаем AccessToken
    access_token = _generate_access_token(request_token.user)
    
    content = {
               'access_token': access_token.access_token,
               'expires_in': access_token.expires_in
               }
    content = simplejson.dumps(content)
    return HttpResponse(content, mimetype='application/javascript')

def _generate_request_token(client, user):
    key = hashlib.sha224(str(time.time()) + settings.SECRET_KEY).hexdigest()
    request_token = RequestToken(request_token=key,
                                 client=client,
                                 user=user)
    request_token.save()
    return request_token

def _generate_access_token(user):
    key = hashlib.sha224(str(time.time()) + settings.SECRET_KEY).hexdigest()
    access_token = AccessToken(access_token=key,
                               expires_in=3600,
                               user=user)
    access_token.save()
    return access_token
    

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
    if not client.valid_redirect_uri(redirect_uri):
        return HttpResponseBadRequest('Wrong redirect_uri')
    
    if request.user.id:
        redirect_to = urlparse.urlparse(redirect_uri)
        # создаем RequestToken
        request_token = _generate_request_token(client, request.user)

        return HttpResponseRedirect('%s://%s%s?code=%s' % (redirect_to.scheme,
                                                   redirect_to.netloc,
                                                   redirect_to.path,
                                                   request_token.request_token))

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            redirect_to = urlparse.urlparse(redirect_uri)

            auth_login(request, form.get_user())

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
                
            # создаем RequestToken
            request_token = _generate_request_token(client, request.user)

            return HttpResponseRedirect('%s://%s%s?code=%s' % (redirect_to.scheme,
                                                       redirect_to.netloc,
                                                       redirect_to.path,
                                                       request_token.request_token))
    else:
        form = AuthenticationForm(request)

    request.session.set_test_cookie()

    current_site = get_current_site(request)

    context = {
        'form': form,
        REDIRECT_FIELD_NAME: 'redirect_uri',
        'site': current_site,
        'site_name': current_site.name,
    }
    return TemplateResponse(request, 'registration/login.html', context)