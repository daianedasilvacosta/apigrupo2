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



class Empresa(db.Model):
    id = db.Column(db.Integer)
    nome_empresa = db.Column(db.String(30), primary_key= True)
    descricao_empresa = db.Column(db.Text)
    
    def to_json(self):
        return {"id": self.id, "nome_empresa": self.nome_empresa, 
                "descricao_empresa": self.descricao_empresa}

# Selecionar Tudo
@app.route("/empresa", methods=["GET"])
def seleciona_empresas():
    empresas_objetos = Empresa.query.all()
    empresas_json = [empresa.to_json() for empresa in empresas_objetos]

    return gera_response(200, "Empresa", empresas_json, "oks")

# Selecionar Individual
@app.route("/empresa/<id>", methods=["GET"])
def seleciona_empresa(id):
    empresa_objeto = Empresa.query.filter_by(id=id).first()
    empresa_json = empresa_objeto.to_json()

    return gera_response(200, "Empresa", empresa_json)
# Cadastrar
@app.route("/empresa", methods=["POST"])
def cria_empresa():
    body = request.get_json()

    try:
        empresa = Empresa(id=body["id"], nome=body["nome_empresa"], descricao_empresa= body["descricao_empresa"])
        db.session.add(empresa)
        db.session.commit()
        return gera_response(201, "Empresa", empresa.to_json(), "Criado com sucesso")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "Empresa", {}, "Erro ao cadastrar")
    
# Atualizar
@app.route("/empresa/<id>", methods=["PUT"])
def atualiza_usuario(id):
    empresa_objeto = Empresa.query.filter_by(id=id).first()
    body = request.get_json()

    try:
        if('id' in body):
            empresa_objeto.id = body ['id']
        if('nome_empresa' in body):
            empresa_objeto.nome = body['nome_empresa']
        if('descricao_empresa' in body):
            empresa_objeto.descricao_empresa = body['descricao_empresa']
        
        db.session.add(empresa_objeto)
        db.session.commit()
        return gera_response(200, "Empresa", empresa_objeto.to_json(), "Atualizado com sucesso")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "Empresa", {}, "Erro ao atualizar")

# Deletar
@app.route("/empresa/<id>", methods=["DELETE"])
def deleta_usuario(id):
    empresa_objeto = Empresa.query.filter_by(id=id).first()

    try:
        db.session.delete(empresa_objeto)
        db.session.commit()
        return gera_response(200, "Empresa", empresa_objeto.to_json(), "Deletado com sucesso")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "Empresa", {}, "Erro ao deletar")


def gera_response(status, nome_do_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_do_conteudo] = conteudo
    if(mensagem):
        body["mensagem"] = mensagem
    return Response(json.dumps(body), status=status, mimetype="application/json")


app.run()