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
    db = client.professorcheatsheet
except:
    print("Problema na conexão")

def listaProfessores(request, id_componente_curricular):
    """
    Recupera o json com os professores e suas turmas anteriores e filtra
    eles para retornar apenas a taxa de aprovação, o nome do professor e
    seu siape. Essa função não leva em conta a reprovação os dados de alunos
    indefiridos ou desistentes (Mas leva em conta os alunos que trancaram a
    disciplina)
    """
    professores = professorPorTurma(request, id_componente_curricular)

    professores_filtrados = []

    for professor in professores:
        aprovacao = 0
        total = 0
        for i in professor['aprovacao']:
            for k in i:
                if k['_id'] == 'APROVADO' or k['_id'] == 'APROVADO POR NOTA':
                    aprovacao += k['num_aprovacao']
                if k['_id'] != 'INDEFERIDO' or k['_id'] != 'DESISTENCIA':
                    total += k['num_aprovacao']
        professores_filtrados.append(
            {
                'professor':professor['_id']['professor'],
                'siape':professor['_id']['siape'],
                'taxa': round((aprovacao*100)/total, 2)
            }
        )

    return render(request, 'listaTaxaAprovacao.html', {'professores':professores_filtrados})


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

def jsonProfessores(request):
    """
    Retorna o json da função professorPorTurma(request, id_componente_curricular)
    """

    return HttpResponse(
        json_util.dumps(
            professorPorTurma(request, id_componente_curricular),
            sort_keys=False, indent=4, default=json_util.default
        ),
        content_type="application/json"
    )
