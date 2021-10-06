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

class Plano_cursos(db.Model):
    id = db.Column(db.Integer)
    nome_plano = db.Column(db.String(50), primary_key= True)
    descricao_plano = db.Column(db.Text)

    def to_json(self):
        return {"id": self.id, "nome_plano": self.nome_plano, "descricao_plano": self.descricao_plano}


# Selecionar Tudo
@app.route("/plano", methods=["GET"])
def seleciona_planos():
    planos_objetos =Plano_cursos.query.all()
    planos_json = [plano_cursos.to_json() for plano_cursos in planos_objetos]
    return gera_response(200, "Plano Curso", planos_json, "oks")

# Selecionar Individual
@app.route("/plano/<id>", methods=["GET"])
def seleciona_plano(id):
    plano_objeto = Plano_cursos.query.filter_by(id=id).first()
    plano_json = plano_objeto.to_json()

    return gera_response(200, "Plano Curso", plano_json)
# Cadastrar
@app.route("/plano", methods=["POST"])
def cria_plano():
    body = request.get_json()

    try:
        plano = Plano_cursos(nome_plano= body["nome_plano"], descricao_plano=body["descricao_plano"])
        db.session.add(plano)
        db.session.commit()
        return gera_response(201, "Plano Curso", plano.to_json(), "Criado com sucesso")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "Plano Curso", {}, "Erro ao cadastrar")
    
# Atualizar
@app.route("/plano/<id>", methods=["PUT"])
def atualiza_usuario(id):
    plano_objeto = Plano_cursos.query.filter_by(id=id).first()
    body = request.get_json()

    try:
        if('nome_plano' in body):
            plano_objeto.nome_plano = body['nome_plano']
        if('descricao_plano' in body):
            plano_objeto.descricao_plano = body['decricao_plano']
        
        db.session.add(plano_objeto)
        db.session.commit()
        return gera_response(200, "Plano Curso", plano_objeto.to_json(), "Atualizado com sucesso")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "Plano Curso", {}, "Erro ao atualizar")

# Deletar
@app.route("/plano/<id>", methods=["DELETE"])
def deleta_plano(id):
    plano_objeto = Plano_cursos.query.filter_by(id=id).first()

    try:
        db.session.delete(plano_objeto)
        db.session.commit()
        return gera_response(200, "Plano Curso", plano_objeto.to_json(), "Deletado com sucesso")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "Plano Curso", {}, "Erro ao deletar")


def gera_response(status, nome_do_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_do_conteudo] = conteudo
    if(mensagem):
        body["mensagem"] = mensagem
    return Response(json.dumps(body), status=status, mimetype="application/json")


app.run()