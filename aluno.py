from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import json
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/ticursosapi'
db = SQLAlchemy(app)
CORS(app)

class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    nome = db.Column(db.String(50))
    email = db.Column(db.String(100))
    nome_empresa = db.Column(db.String(10))
    nome_plano = db.Column(db.String(20))

    def to_json(self):
        return {"id": self.id, "nome": self.nome, "email": self.email, "nome_empresa": self.nome_empresa,
                "nome_plano":self.nome_plano}

# Selecionar Tudo
@app.route("/aluno", methods=["GET"])
def seleciona_alunos():
    alunos_objetos = Aluno.query.all()
    alunos_json = [aluno.to_json() for aluno in alunos_objetos]
    return gera_response(200, "Alunos", alunos_json, "oks")

# Selecionar Individual
@app.route("/aluno/<id>", methods=["GET"])
def seleciona_aluno(id):
    aluno_objeto = Aluno.query.filter_by(id=id).first()
    aluno_json = aluno_objeto.to_json()
    return gera_response(200, "Aluno", aluno_json)

# Cadastrar
@app.route("/aluno", methods=["POST"])
def cria_aluno():
    body = request.get_json()

    try:
        aluno = Aluno(id=body["id"], nome=body["nome"], email= body["email"], nome_empresa=body["nome_empresa"],
                      nome_plano=body["nome_plano"])
        db.session.add(aluno)
        db.session.commit()
        return gera_response(201, "Aluno", aluno.to_json(), "Criado com sucesso")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "Aluno", {}, "Erro ao cadastrar")
    
# Atualizar
@app.route("/aluno/<id>", methods=["PUT"])
def atualiza_aluno(id):
    aluno_objeto = Aluno.query.filter_by(id=id).first()
    body = request.get_json()

    try:
        if('id' in body):
            aluno_objeto.id = body['id']
        if('nome' in body):
            aluno_objeto.nome = body['nome']
        if('email' in body):
            aluno_objeto.email = body['email']
        if('nome_empresa' in body):
            aluno_objeto.nome_empresa = body['nome_empresa']
        if('nome_plano' in body):
            aluno_objeto.nome_plano = body['nome_plano']    
        
        db.session.add(aluno_objeto)
        db.session.commit()
        return gera_response(200, "Aluno", aluno_objeto.to_json(), "Atualizado com sucesso")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "Aluno", {}, "Erro ao atualizar")

# Deletar
@app.route("/aluno/<id>", methods=["DELETE"])
def deleta_usuario(id):
    aluno_objeto = Aluno.query.filter_by(id=id).first()

    try:
        db.session.delete(aluno_objeto)
        db.session.commit()
        return gera_response(200, "Aluno", aluno_objeto.to_json(), "Deletado com sucesso")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "Aluno", {}, "Erro ao deletar")


def gera_response(status, nome_do_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_do_conteudo] = conteudo
    if(mensagem):
        body["mensagem"] = mensagem
    return Response(json.dumps(body), status=status, mimetype="application/json")


app.run()