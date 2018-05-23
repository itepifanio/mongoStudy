from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from . import services
from . import sigaa_api

# Create your views here.

def index(request):
    return render(request, 'core/index.html', {})

def login(request):
    auth_url = settings.API_SIGAA['AUTH_URL'] + "/authorize"
    client_id = "client_id=" + settings.API_SIGAA['CREDENTIALS']['CLIENT_ID']
    redirect_uri = "redirect_uri=" + settings.API_SIGAA['REDIRECT_URI']
    response_type = "response_type=code"
    login_url = auth_url + "?" + client_id + "&" + redirect_uri + "&" + response_type

    return HttpResponseRedirect(login_url)

def authenticate(request):
    code = request.GET.get('code')

    if code is not None:
        successfullyStarted = sigaa_api.init(request, code)
        if successfullyStarted:
            return HttpResponseRedirect('dashboard')

    return HttpResponseRedirect('/')

def dashboard(request):
    if services.is_logged(request) :
        return render(request, 'core/dashboard.html', {'user': services.get_user_session(request)})

    user = sigaa_api.getUserInfo(request)
    if user is not None:
        services.init_session(request, user)
        return render(request, 'core/dashboard.html', {'user': user})

    return HttpResponseRedirect('/')
