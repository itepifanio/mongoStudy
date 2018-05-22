from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
import requests

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

def init_session(request):
    code = request.GET.get('code')

    if code is not None:
        auth_url = settings.API_SIGAA['AUTH_URL'] + "/token"
        params = {
            'client_id': settings.API_SIGAA['CREDENTIALS']['CLIENT_ID'],
            'client_secret': settings.API_SIGAA['CREDENTIALS']['CLIENT_SECRET'],
            'redirect_uri': settings.API_SIGAA['REDIRECT_URI'],
            'grant_type': 'authorization_code',
            'code': code
        }

        response = requests.post(auth_url, params=params)
        if response.status_code == requests.codes.ok:
            token = response.json()
            request.session['token'] = {
                'access_token': token['access_token'],
                'token_type': token['token_type'],
                'refresh_token': token['refresh_token'],
                'expires_in': token['expires_in'],
                'scope': token['scope']
            }

            return HttpResponseRedirect('dashboard')

    return HttpResponseRedirect('/')

def dashboard(request):
    if 'has' in request.session :
        return render(request, 'core/dashboard.html', {})

    url = settings.API_SIGAA['BASE_URL'] + "/usuario/v0.1/usuarios/info"
    token = request.session.get('token', False)
    headers = {
        'Authorization': 'bearer' + ' ' + token['access_token'],
        'x-api-key': settings.API_SIGAA['CREDENTIALS']['X_API_KEY']
    }

    response = requests.get(url, headers=headers)
    if response.status_code == requests.codes.ok:
        user = response.json()

        request.session['has'] = True
        request.session['user'] = {
            'id': user['id-usuario'],
            'name': user['nome-pessoa'].title(),
            'email': user['email'],
            'active': user['ativo'],
            'photo-id': user['id-foto'],
            'photo-key': user['chave-foto'],
        }

        return render(request, 'core/dashboard.html', {})

    return HttpResponseRedirect('/')
