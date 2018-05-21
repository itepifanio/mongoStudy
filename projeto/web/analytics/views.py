from django.shortcuts import render
from pymongo import Connection

server = "localhost"
port   = 27017
#Estabelece conexão com a instância mongo
conn = Connection(server, port)

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

# Create your views here.
