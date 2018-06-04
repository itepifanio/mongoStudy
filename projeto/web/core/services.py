from django.conf import settings
from core.sigaa_api import User
import requests

def init_session(request, user):
    request.session['user'] = {
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'active': user.active,
        'photo_id': user.photo_id,
        'photo_key': user.photo_key,
    }

def get_user_session(request):
    user = User()
    user.id = request.session['user']['id']
    user.name = request.session['user']['name']
    user.email = request.session['user']['email']
    user.active = request.session['user']['active']
    user.photo_id = request.session['user']['photo_id']
    user.photo_key = request.session['user']['photo_key']

    return user

def is_logged(request):
    return 'user' in request.session
