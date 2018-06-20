from django.conf import settings
import requests
import logging
from . import services

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

def getUserVinculos(request):
    logger = logging.getLogger(__name__)
    token = request.session.get('token')
    auth_headers = {
        'Authorization': 'bearer' + ' ' + token['access_token'],
        'x-api-key': settings.API_SIGAA['CREDENTIALS']['X_API_KEY']
    }

    user = services.get_user_session(request)

    url = settings.API_SIGAA['ENDPOINTS']['VINCULO'] + "?id-usuario=" + str(user.id)
    response = requests.get(url, headers=auth_headers)
    if response.status_code == requests.codes.ok:
        vinculos = []
        for vinculo in response.json():
            vinculos.append(Vinculo(vinculo))
        return vinculos
    return None

def getDiscente(request, id):
    token = request.session.get('token')
    auth_headers = {
        'Authorization': 'bearer' + ' ' + token['access_token'],
        'x-api-key': settings.API_SIGAA['CREDENTIALS']['X_API_KEY']
    }

    url = settings.API_SIGAA['ENDPOINTS']['DISCENTE'] + "/" + str(id)
    response = requests.get(url, headers=auth_headers)
    if response.status_code == requests.codes.ok:
        return Discente(response.json())
    return None

def getMatriculas(request, id_discente):
    logger = logging.getLogger(__name__)
    token = request.session.get('token')
    auth_headers = {
        'Authorization': 'bearer' + ' ' + token['access_token'],
        'x-api-key': settings.API_SIGAA['CREDENTIALS']['X_API_KEY']
    }

    url = settings.API_SIGAA['ENDPOINTS']['MATRICULA'] + "?id-discente=" + str(id_discente) + "&limit=100&offset=0"
    response = requests.get(url, headers=auth_headers)

    if response.status_code == requests.codes.ok:
        matriculas = []
        for matricula in response.json():
            matriculas.append(Matricula(matricula))
        return matriculas
    else:
        logger.error("DEU MERDA: " +  str(response.status_code))
    return None

def getMatrizesCurricularesCurso(request, id_curso):
    token = request.session.get('token')
    auth_headers = {
        'Authorization': 'bearer' + ' ' + token['access_token'],
        'x-api-key': settings.API_SIGAA['CREDENTIALS']['X_API_KEY']
    }

    url = settings.API_SIGAA['ENDPOINTS']['CURSO'] + "/matrizes-curriculares?id-curso=" + str(id_curso)
    response = requests.get(url, headers=auth_headers)

    if response.status_code == requests.codes.ok:
        matrizes = []
        for matriz in response.json():
            matrizes.append(MatrizCurricular(matriz))
        return matrizes
    return None

def getDisciplinasCurso(request, id_matriz_curricular):
    token = request.session.get('token')
    auth_headers = {
        'Authorization': 'bearer' + ' ' + token['access_token'],
        'x-api-key': settings.API_SIGAA['CREDENTIALS']['X_API_KEY']
    }

    url = settings.API_SIGAA['ENDPOINTS']['CURSO'] + "/componentes-curriculares?id-matriz-curricular=" + str(id_matriz_curricular) + "&limit=100&offset=0"
    response = requests.get(url, headers=auth_headers)
    if response.status_code == requests.codes.ok:
        disciplinas = []
        for disciplina in response.json():
            disciplinas.append(Disciplina(disciplina))
        return disciplinas
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

class Vinculo:
    def __init__(self, data = None):
        if data is not None:
            self.id = data['id-vinculo']
            self.tipo = data['tipo-vinculo']
            self.matricula = data['identificador']
            self.id_curso = data['id-lotacao']
            self.nome_curso = data['lotacao']
            self.situacao = data['situacao']
            self.ativo = data['ativo']

class Discente:
    def __init__(self, data = None):
        if data is not None:
            self.id = data['id-discente']
            self.nome = data['nome-discente']
            self.email = data['email']
            self.matricula = data['matricula']
            self.ingresso = str(data['ano-ingresso']) + '.' + str(data['periodo-ingresso'])
            self.id_curso = data['id-curso']

class Matricula:
    def __init__(self, data = None):
        if data is not None:
            self.id = data['id-matricula-componente']
            self.id_disciplina = data['id-componente']

class MatrizCurricular:
    def __init__(self, data = None):
        if data is not None:
            self.id = data['id-matriz-curricular']
            self.ativa = data['ativo']

class Disciplina:
    def __init__(self, data = None):
        if data is not None:
            self.id = data['id-componente']
            self.codigo = data['codigo']
            self.nome = data['nome']
            self.semestre = data['semestre-oferta']
            self.obrigatoria = data['disciplina-obrigatoria']
