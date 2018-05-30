from django.shortcuts import render
from pymongo import MongoClient
from bson import BSON
from bson import json_util
# apenas para testes, remover a posteriori
import pprint
import json
from django.http import HttpResponse

server = "localhost"
port   = 27017

try:
    #Estabelece conexão com a instância mongo
    client = MongoClient(server, port)
    db = client.professorcheatsheet
except:
    print("Problema na conexão")


"""
Recuperando um documento da coleção:
Note que o primeiro parâmetro do find_one é a query
o segundo a projeção
print("title: ", poll['title']
poll = conn.events.polls_post.find_one({}, {"title":1})

Recuperando todos os documentos da coleção:
polls = conn.events.polls_post.find({},{"title" : 1})
for poll in polls:
    print "Title : ",poll['title']
"""

def teste(request):
    # Em teoria, pelo fluxo preterido, temos o id_disciplina
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
                                # No fluxo, quando vier o id_disciplina adicionar
                                # aqui um "$and" ["$id_componente", id_disciplina]
                                "$and": [
                                    {"$eq": ["$id_docente_interno", "$$id_servidor"]},
                                    {"$eq": ["$id_componente_curricular", 57807]}
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
                "as": "turmas_lecionadas"
            },
        },
        # Tendo o id da disciplina eu só vou ter uma turma_lecionada
        # por cada professor, então posso realizar unwind dessa turma
        {"$unwind":"$turmas_lecionadas"},
        {
            "$project": {
                "_id": 0,
                "id_servidor": 1,
                "nome": 1,
                "turmas_lecionadas": 1,
            }
        },
    ]
    # Só retorna um dos docentes

    return HttpResponse(
        json_util.dumps(
            db['docentes'].aggregate(pipeline), sort_keys=True,
            indent=4, default=json_util.default
        ),
        content_type="application/json"
    )
