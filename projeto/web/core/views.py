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
        return render(request, 'core/dashboard/index.html', {'user': services.get_user_session(request)})

    user = sigaa_api.getUserInfo(request)
    if user is not None:
        services.init_session(request, user)
        return render(request, 'core/dashboard/index.html', {'user': services.get_user_session(request)})

    return HttpResponseRedirect('/')

def getMatrizesCurriculares(request):
    vinculos = sigaa_api.getUserVinculos(request)
    vinculoGraduacaoAtivo = None
    for vinculo in vinculos:
        if vinculo.ativo:
            vinculoGraduacaoAtivo = vinculo
            break

    matrizesCurriculares = sigaa_api.getMatrizesCurricularesCurso(request, vinculoGraduacaoAtivo.id_curso)

    data = []
    for matrizCurricular in matrizesCurriculares:
        if matrizCurricular.ativa:
            data.append({'id': matrizCurricular.id, 'curso': matrizCurricular.curso , 'turno': matrizCurricular.turno, 'ano': str(matrizCurricular.ano) + "." + str(matrizCurricular.periodo), 'enfase': matrizCurricular.enfase})

    return JsonResponse(data, safe=False)

def disciplinas(request):
    user = sigaa_api.getUserInfo(request)
    id_matriz_curricular = request.GET.get('id-matriz-curricular', -1);

    return render(request, 'core/dashboard/disciplinas.html', {'user': user, 'id_matriz_curricular': id_matriz_curricular})

def getDisciplinas(request):
    user = sigaa_api.getUserInfo(request)
    id_matriz_curricular = request.GET.get('id-matriz-curricular', -1);
    tipo = request.GET.get('tipo', "obrigatorias");

    obrigatoria = (tipo == "obrigatorias")

    data = []
    limit = 100
    offset = 0
    disciplinas = sigaa_api.getDisciplinasCurso(request, id_matriz_curricular, obrigatoria, limit, offset)
    while disciplinas is not None and len(disciplinas) > 0:
        for disciplina in disciplinas:
            if hasattr(disciplina, 'componentes'):
                componentes = []
                for componente in disciplina.componentes:
                    componentes.append({'id': componente.id, 'codigo': componente.codigo, 'nome': componente.nome, 'semestre': componente.semestre})
                data.append({'id': disciplina.id, 'codigo': disciplina.codigo, 'nome': disciplina.nome, 'semestre': disciplina.semestre, 'componentes': componentes})
            else:
                data.append({'id': disciplina.id, 'codigo': disciplina.codigo, 'nome': disciplina.nome, 'semestre': disciplina.semestre})

        offset = offset + limit
        disciplinas = sigaa_api.getDisciplinasCurso(request, id_matriz_curricular, limit, offset)

    return JsonResponse(data, safe=False)

def estatisticas(request):
    user = sigaa_api.getUserInfo(request)
    id_matriz_curricular = request.GET.get('id-matriz-curricular', -1);
    id_disciplina = request.GET.get('id-disciplina', -1);

    return render(request, 'core/dashboard/estatisticas.html', {'user': user, 'id_matriz_curricular': id_matriz_curricular, 'id_disciplina': id_disciplina})
