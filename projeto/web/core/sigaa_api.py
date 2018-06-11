from django.conf import settings
import requests

def init(request, code):
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
        request.session['token'] = response.json()
        return True
    return False

def getUserInfo(request):
    token = request.session.get('token')
    auth_headers = {
        'Authorization': 'bearer' + ' ' + token['access_token'],
        'x-api-key': settings.API_SIGAA['CREDENTIALS']['X_API_KEY']
    }

    url = settings.API_SIGAA['ENDPOINTS']['USUARIO'] + "/info"
    response = requests.get(url, headers=auth_headers)
    if response.status_code == requests.codes.ok:
        return User(response.json())

    return None

class User:
    def __init__(self, data = None):
        if data is not None:
            self.id = data['id-usuario']
            self.name = data['nome-pessoa'].title()
            self.email =  data['email']
            self.active = data['ativo']
            self.photo_id = data['id-foto']
            self.photo_key = data['chave-foto']
