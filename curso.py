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

class Curso(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    nome_curso = db.Column(db.String(100))
    descricao_curso = db.Column(db.Text)
    carga_horaria = db.Column(db.VARCHAR(4))
    ano_curso = db.Column(db.VARCHAR(4))
    formacao_curso = db.Column(db.String(50))

    def to_json(self):
        return {"id":self.id, "nome_curso": self.nome_curso, "descricao_curso": self.descricao_curso, 
                "carga_horaria": self.carga_horaria, "ano_curso": self.ano_curso,
                "formacao_curso": self.formacao_curso}


# Selecionar Tudo
@app.route("/curso", methods=["GET"])
def seleciona_cursos():
    cursos_objetos = Curso.query.all()
    cursos_json = [cursos.to_json() for cursos in cursos_objetos]
    return gera_response(200, "Cursos", cursos_json, "oks")

# Selecionar Individual
@app.route("/curso/<id>", methods=["GET"])
def seleciona_curso(id):
    curso_objeto = Curso.query.filter_by(id=id).first()
    curso_json = curso_objeto.to_json()

    return gera_response(200, "Curso", curso_json)
# Cadastrar
@app.route("/curso", methods=["POST"])
def cria_curso():
    body = request.get_json()

    try:
        cursos = Curso(nome_curso=body["nome_curso"], descricao_curso=body["descricao_curso"],
                      carga_horaria=body["carga_horaria"], ano_curso=body["ano_curso"],
                      formacao_curso=body["formacao_curso"])
        db.session.add(cursos)
        db.session.commit()
        return gera_response(201, "Curso", cursos.to_json(), "Criado com sucesso")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "Curso", {}, "Erro ao cadastrar")
    
# Atualizar
@app.route("/curso/<id>", methods=["PUT"])
def atualiza_curso(id):
    curso_objeto = Curso.query.filter_by(id=id).first()
    body = request.get_json()

    try:
        if('nome_curso' in body):
            curso_objeto.nome_curso = body['nome_curso']
        if('descricao_curso' in body):
            curso_objeto.descricao_curso = body['descricao_curso']
        if('carga_horaria' in body):
            curso_objeto.carga_horaria = body['carga_horaria']
        if('ano_curso' in body):
            curso_objeto.ano_curso = body['ano_curso']    
        if('formacao_curso' in body):
            curso_objeto.formacao_curso = body['formacao_curso']
        
        db.session.add(curso_objeto)
        db.session.commit()
        return gera_response(200, "Curso", curso_objeto.to_json(), "Atualizado com sucesso")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "Curso", {}, "Erro ao atualizar")

# Deletar
@app.route("/curso/<id>", methods=["DELETE"])
def deleta_curso(id):
    curso_objeto = Curso.query.filter_by(id=id).first()

    try:
        db.session.delete(curso_objeto)
        db.session.commit()
        return gera_response(200, "Curso", curso_objeto.to_json(), "Deletado com sucesso")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "Curso", {}, "Erro ao deletar")


def gera_response(status, nome_do_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_do_conteudo] = conteudo
    if(mensagem):
        body["mensagem"] = mensagem
    return Response(json.dumps(body), status=status, mimetype="application/json")


app.run()