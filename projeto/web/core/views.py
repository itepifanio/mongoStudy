from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.urls import reverse
from django.conf import settings
from . import services
from . import sigaa_api
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django_redis import get_redis_connection
import json
import logging

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

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
            return HttpResponseRedirect('dashboard/matrizesCurriculares')

    return HttpResponseRedirect('/')

def matrizesCurriculares(request):
    if services.is_logged(request) :
        return render(request, 'core/matrizes_curriculares.html', {'user': services.get_user_session(request)})

    user = sigaa_api.getUserInfo(request)
    if user is not None:
        services.init_session(request, user)
        return render(request, 'core/matrizes_curriculares.html', {'user': services.get_user_session(request)})

    return HttpResponseRedirect('/')

def getMatrizesCurriculares(request):
    logger = logging.getLogger(__name__)
    con = get_redis_connection("default")

    data = []
    result = con.lrange("matrizesCurriculares", 0, -1)
    if result:
        r = [x.decode("utf-8") for x in result]
        for id in r:
            result = con.hgetall("matrizesCurricular:" + id)
            m = {k.decode("utf-8"): v.decode("utf-8") for k,v in result.items()}
            data.append({'id': int(m['id']), 'curso': m['curso'] , 'turno': m['turno'], 'ano': m['ano'], 'enfase': m['enfase']})
    else:
        result = con.hgetall("vinculo")
        if result:
            r = {k.decode("utf-8"): v.decode("utf-8") for k,v in result.items()}
            vinculoGraduacaoAtivo = sigaa_api.Vinculo()
            vinculoGraduacaoAtivo.id = int(r['id'])
            vinculoGraduacaoAtivo.tipo = r['tipo']
            vinculoGraduacaoAtivo.matricula = r['matricula']
            vinculoGraduacaoAtivo.id_curso = int(r['id_curso'])
            vinculoGraduacaoAtivo.nome_curso = r['nome_curso']
            vinculoGraduacaoAtivo.situacao = r['situacao']
            vinculoGraduacaoAtivo.ativo = r['ativo'] == 'True'
        else:
            vinculos = sigaa_api.getUserVinculos(request)
            vinculoGraduacaoAtivo = None
            for vinculo in vinculos:
                if vinculo.ativo:
                    vinculoGraduacaoAtivo = vinculo
                    con.hset('vinculo', 'id', vinculo.id)
                    con.hset('vinculo', 'tipo', vinculo.tipo)
                    con.hset('vinculo', 'matricula', vinculo.matricula)
                    con.hset('vinculo', 'id_curso', vinculo.id_curso)
                    con.hset('vinculo', 'nome_curso', vinculo.nome_curso)
                    con.hset('vinculo', 'situacao', vinculo.situacao)
                    con.hset('vinculo', 'ativo', vinculo.ativo)
                    break

        matrizesCurriculares = sigaa_api.getMatrizesCurricularesCurso(request, vinculoGraduacaoAtivo.id_curso)
        for matrizCurricular in matrizesCurriculares:
            if matrizCurricular.ativa:
                con.rpush("matrizesCurriculares", matrizCurricular.id)
                con.hset('matrizesCurricular:' + str(matrizCurricular.id), 'id', matrizCurricular.id)
                con.hset('matrizesCurricular:' + str(matrizCurricular.id), 'curso', matrizCurricular.curso)
                con.hset('matrizesCurricular:' + str(matrizCurricular.id), 'turno', matrizCurricular.turno)
                con.hset('matrizesCurricular:' + str(matrizCurricular.id), 'enfase', matrizCurricular.enfase)
                con.hset('matrizesCurricular:' + str(matrizCurricular.id), 'ano', str(matrizCurricular.ano) + "." + str(matrizCurricular.periodo))
                data.append({'id': matrizCurricular.id, 'curso': matrizCurricular.curso , 'turno': matrizCurricular.turno, 'ano': str(matrizCurricular.ano) + "." + str(matrizCurricular.periodo), 'enfase': matrizCurricular.enfase})

    return JsonResponse(data, safe=False)

def disciplinas(request):
    user = sigaa_api.getUserInfo(request)
    id_matriz_curricular = request.GET.get('id-matriz-curricular', -1);

    return render(request, 'core/disciplinas.html', {'user': user, 'id_matriz_curricular': id_matriz_curricular})

def getDisciplinas(request):
    con = get_redis_connection("default")

    user = sigaa_api.getUserInfo(request)
    id_matriz_curricular = request.GET.get('id-matriz-curricular', -1);
    tipo = request.GET.get('tipo', "obrigatorias");

    obrigatoria = (tipo == "obrigatorias")

    data = []

    result = con.lrange("disciplinas_" + tipo, 0, -1)

    if result:
        r = [x.decode("utf-8") for x in result]
        for id in r:
            result = con.hgetall("disciplina:" + id)
            m = {k.decode("utf-8"): v.decode("utf-8") for k,v in result.items()}
            data.append({'id': int(m['id']), 'codigo': m['codigo'] , 'nome': m['nome'], 'semestre': m['semestre']})
    else:
        limit = 100
        offset = 0
        disciplinas = sigaa_api.getDisciplinasCurso(request, id_matriz_curricular, obrigatoria, limit, offset)
        while disciplinas is not None and len(disciplinas) > 0:
            for disciplina in disciplinas:
                con.rpush("disciplinas_" + tipo, disciplina.id)
                con.hset("disciplina:" + str(disciplina.id), "id", disciplina.id)
                con.hset("disciplina:" + str(disciplina.id), "codigo", disciplina.codigo)
                con.hset("disciplina:" + str(disciplina.id), "nome", disciplina.nome)
                con.hset("disciplina:" + str(disciplina.id), "semestre", disciplina.semestre)
                con.hset("disciplina:" + str(disciplina.id), "obrigatoria", disciplina.obrigatoria)
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

def getDisciplina(request):
    id_componente_curricular = request.GET.get('id-componente-curricular', -1);

    disciplina = sigaa_api.getDisciplina(request, id_componente_curricular)
    data = {}
    if disciplina is not None:
        data['id'] = disciplina.id
        data['codigo'] = disciplina.codigo
        data['nome'] = disciplina.nome
        data['semestre'] = disciplina.semestre
        if hasattr(disciplina, 'componentes'):
            componentes = []
            for componente in disciplina.componentes:
                componentes.append({'id': componente.id, 'codigo': componente.codigo, 'nome': componente.nome, 'semestre': componente.semestre})
            data['componentes'] = disciplina.componentes

    return JsonResponse(data, safe=False)

def estatisticas(request):
    user = sigaa_api.getUserInfo(request)
    id_matriz_curricular = request.GET.get('id-matriz-curricular', -1);
    id_disciplina = request.GET.get('id-disciplina', -1);

    return render(request, 'core/estatisticas.html', {'user': user, 'id_matriz_curricular': id_matriz_curricular, 'id_disciplina': id_disciplina})
