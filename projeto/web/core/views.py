from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.urls import reverse
from django.conf import settings
from . import services
from . import sigaa_api
import json
import logging

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
        return HttpResponseRedirect('/dashboard/cursos')

    user = sigaa_api.getUserInfo(request)
    if user is not None:
        services.init_session(request, user)
        return HttpResponseRedirect('/dashboard/cursos')

    return HttpResponseRedirect('/')

def cursos(request):
    return render(request, 'core/dashboard/cursos.html', {'user': services.get_user_session(request)})

def getCursos(request):
    vinculos = sigaa_api.getUserVinculos(request)

    data = []
    if vinculos is not None:
        for vinculo in vinculos:
            discente = sigaa_api.getDiscente(request, vinculo.id)
            data.append({'id': vinculo.id_curso, 'nome': vinculo.nome_curso , 'matricula': vinculo.matricula, 'ingresso': discente.ingresso, 'discente': discente.id})
    return JsonResponse(data, safe=False)

def disciplinas(request):
    user = sigaa_api.getUserInfo(request)
    discente_id = request.GET.get('discente-id', -1);
    curso_id = request.GET.get('curso-id', -1);

    return render(request, 'core/dashboard/disciplinas.html', {'user': user, 'discente_id': discente_id, 'curso_id': curso_id})

def getDisciplinas(request):
    discente_id = request.GET.get('discente-id', -1);
    curso_id = request.GET.get('curso-id', -1);

    matrizesCurriculares = sigaa_api.getMatrizesCurricularesCurso(request, curso_id)
    matrizCurricular = None
    for matriz in matrizesCurriculares:
        if matriz.ativa:
            matrizCurricular = matriz
            break

    disciplinasCurso = sigaa_api.getDisciplinasCurso(request, matrizCurricular.id)
    matriculas = sigaa_api.getMatriculas(request, discente_id)

    disciplinas  = [disciplina for disciplina in disciplinasCurso if not any( matricula.id_disciplina == disciplina.id for matricula in matriculas)]

    data = []
    for disciplina in disciplinas:
        data.append({'id': disciplina.id, 'codigo': disciplina.codigo, 'nome': disciplina.nome, 'semestre': disciplina.semestre})

    return JsonResponse(data, safe=False)

def estatisticas(request):
    user = sigaa_api.getUserInfo(request)
    discente_id = request.GET.get('discente-id', -1);
    curso_id = request.GET.get('curso-id', -1);
    disciplina_id = request.GET.get('disciplina-id', -1);

    return render(request, 'core/dashboard/estatisticas.html', {'user': user, 'discente_id': discente_id, 'curso_id': curso_id, 'disciplina_id': disciplina_id})
