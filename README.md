# Descrição
Estudos práticos da disciplina de Tópicos Especiais em NoSQL, utilizando o MongoDB. 

## Divisão do repositório

A pasta [exerciciosMongoDB](https://github.com/itepifanio/mongoStudy/tree/master/exerciciosMongoDB) contém os exercícios passados em sala durante a disciplina. Até o momento foram desenvolvidos dois exercícios, um utilizando consultas básicas do mongoDB e outro utilizando aggregation. Também está inserido nessa pasta um exemplo de código em Java que exibe as consultas realizadas nos exercícios anteriores, mas com a conexão do mongoDB, bastando então apenas compilar o projeto para exibir os resultados.

## Projeto final da disciplina

Consiste em um sistema web que consome os dados abertos da UFRN, utilizando os dados de turmas e docentes para determinar a taxa de aprovação de cada professor. 

O aluno irá se logar através da autenticação da SINFO. Quando logado recuperaremos seu vínculo ativo da graduação, recuperado o semestre atual e a estrutura curricular do aluno, assim ele poderá acessar através das disciplinas, quais os professores disponíveis e a taxa de aprovação de cada um deles.

O projeto será escrito em Python e Django, utilizando MongoDB. O banco de dados será estruturado em conjunto com os dados abertos da UFRN, entretanto, serão feitas algumas adaptações nesses dados utilizando o Jupyter Notebook, algo que pode ser acompanhado na pasta [tratandoCSV](https://github.com/itepifanio/mongoStudy/blob/master/projeto/tratandoCSV/Turmas%20de%20graduacao%202015-2018%20.ipynb).

Todo o banco estará disponível no serviço de banco de dados do MongoDB, o Atlas. 

## Recomendações de contribuição 


- Sempre que for implementar algo verifique se existe uma issue para isso, caso não exista, crie uma e atribua a você. 

- As issues devem ser criadas como cards dentro do projeto, depois transfromadas em issues, assim teremos um to-do list organizado.

- As issues devem ser atribuidas sempre a uma milestone, para podermos acompanhar o desenvolvimento do projeto. 

- As branchs criadas deverao acompanhar o numero da issue, tal qual "issue-42"

- Antes de mergear uma branch, o pull request tem que passar por uma revisão e teste de outra pessoa.
