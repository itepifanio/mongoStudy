from django.shortcuts import render
from pymongo import MongoClient
from bson import BSON
from bson import json_util
# apenas para testes, remover a posteriori
import pprint
import json
from django.http import HttpResponse
from operator import itemgetter

server = "localhost"
port   = 27017

try:
    #Estabelece conexão com a instância mongo
    client = MongoClient(server, port)
    db = client.professorCheatSheet
except:
    print("Problema na conexão")


def listaProfessores(request):
    """
    Recupera o json com os professores e suas turmas anteriores e filtra
    eles para retornar apenas a taxa de aprovação, o nome do professor e
    seu siape. Essa função não leva em conta a reprovação os dados de alunos
    indefiridos ou desistentes (Mas leva em conta os alunos que trancaram a
    disciplina)
    """

    id_matriz_curricular = int(request.GET.get('id-matriz-curricular', -1))
    id_componente_curricular = int(request.GET.get('id-componente-curricular', -1))

    professores = professorPorTurma(request, id_componente_curricular)
    professores_filtrados = []

    for professor in professores:
        aprovacao = 0
        total = 0
        for turmas in professor['aprovacao']:
            for tipoAprovacao in turmas:
                if tipoAprovacao['_id'] == 'APROVADO' or tipoAprovacao['_id'] == 'APROVADO POR NOTA':
                    aprovacao += tipoAprovacao['num_aprovacao']
                if tipoAprovacao['_id'] != 'INDEFERIDO' or tipoAprovacao['_id'] != 'DESISTENCIA':
                    total += tipoAprovacao['num_aprovacao']
        professores_filtrados.append(
            {
                'professor':professor['_id']['professor'],
                'siape':professor['_id']['siape'],
                'taxa': round((aprovacao*100)/total, 2)
            }
        )

    return render(request, 'listaTaxaAprovacao.html', {
        'professores':professores_filtrados,
        'id_componente_curricular': id_componente_curricular,
        'id_matriz_curricular': id_matriz_curricular
    })


def professorPorTurma(request, id_componente_curricular):
    """
    Retorna a consulta a partir do id_componente_curricular
    retornando os nomes dos professores, seu siape e um array
    de turmas contendo as quantidades de reprovados, desistentes
    e aprovados
    """
    # Em teoria, pelo fluxo preterido, temos o id_disciplina
    #FMC1 55022
    #FMC2 55025

    pipeline = [
        {
            "$lookup": {
                "from": "turmas",
                "let": {"id_servidor":"$id_servidor"},
                "pipeline": [
                    {
                    "$match":
                        {"$expr":
                            {
                                "$and": [
                                    {"$eq": ["$id_docente_interno", "$$id_servidor"]},

                                        {"$eq": ["$id_componente_curricular", id_componente_curricular]}
                                ]
                            }
                        }
                    },
                    {
                        "$project":{
                            "_id": 0,
                            "ano": 1,
                            "id_turma": 1,
                            "id_componente_curricular": 1
                        }
                    }
                ],
                "as": "turma_lecionada"
            },
        },
        # Tendo o id da disciplina eu só vou ter uma turma_lecionada
        # por cada professor, então posso realizar unwind dessa turma
        {"$unwind":"$turma_lecionada"},
        {
            "$project": {
                "_id": 0,
                "siape": 1,
                "nome": 1,
                "turma_lecionada": 1,
            }
        },
        {
            "$lookup": {
                "from": "matriculas",
                "let": {"turma_lecionada":"$turma_lecionada.id_turma"},
                "pipeline": [
                    {
                        "$match":
                            {"$expr":
                                {
                                    "$eq": ["$id_turma", "$$turma_lecionada"]
                                }
                            }
                    },
                    {
                        "$group": {
                            "_id": "$descricao",
                            "num_aprovacao": {"$sum": 1},
                        }
                    }
                ],
                "as": "alunos_lecionados"
            }
        },
        {
            "$group": {
                "_id": {"professor": "$nome", "siape":"$siape"},
                "aprovacao": {"$push": "$alunos_lecionados"},
            }
        }
    ]

    return db['docentes'].aggregate(pipeline)


def jsonProfessor(request, id_componente_curricular, siape):
    # Siape exemplo do id_componente_curricular 55025:
    # 2251108
    """
    Retorna o json da função professorPorTurma(request, id_componente_curricular)
    filtrando o siape do professor pesquisado
    """
    results = []

    for professor in professorPorTurma(request, id_componente_curricular):
        if professor['_id']['siape'] == siape:
            totalAprovacoes = sum(i['num_aprovacao'] for i in professor['aprovacao'][0])
            for tipoAprovacao in professor['aprovacao'][0]:
                # Acumula os valores para formatar highcharts
                results.append({
                    'name': tipoAprovacao['_id'],
                    'y': round((tipoAprovacao['num_aprovacao']*100)/totalAprovacoes, 2)
                })


            return HttpResponse(
                json_util.dumps(
                    results,
                    sort_keys=False, indent=4, default=json_util.default
                ),
                    content_type="application/json"
                )
    else:
        return HttpResponse("Nenhum professor encontrado com esse siape")


def detalhesProfessor(request):
    id_matriz_curricular = int(request.GET.get('id-matriz-curricular', -1))
    id_componente_curricular = int(request.GET.get('id-componente-curricular', -1))
    siape = int(request.GET.get('siape', -1))

    professor = db['docentes'].find_one({'siape':siape})

    return render(request, 'detalhesProfessor.html', {
        'siape':siape,
        'professor': professor,
        'id_matriz_curricular': id_matriz_curricular,
        'id_componente_curricular': id_componente_curricular
    })
