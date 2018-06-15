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

def teste(request, id_componente_curricular):
    """
    Retorna json com a consulta a partir do id_componente_curricular
    retornando os professores que ministraram a disciplina e as taxas
    de aprovação ou reprovação
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
                "id_servidor": 1,
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
                "_id": {"professor": "$nome", "id_servidor":"$id_servidor"},
                "aprovacao": {"$push": "$alunos_lecionados"},
            }
        }
    ]

    objects = []

    for object in db['docentes'].aggregate(pipeline):
        aprovacao = 0
        total = 0
        for i in object['aprovacao']:
            for k in i:
                if k['_id'] == 'APROVADO' or k['_id'] == 'APROVADO POR NOTA':
                    aprovacao += k['num_aprovacao']
                if k['_id'] != 'INDEFERIDO' or k['_id'] != 'DESISTENCIA':
                    total += k['num_aprovacao']
        objects.append(
            {
                'professor':object['_id']['professor'],
                'aprovacao': aprovacao,
                'total': total
            }
        )

    return HttpResponse(
        json_util.dumps(
            objects, sort_keys=False,
            indent=4, default=json_util.default
        ),
        content_type="application/json"
    )
