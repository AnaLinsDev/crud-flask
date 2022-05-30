from flask import Response, request
from models.User import *
from app import app
import json

@app.route("/users", methods=["GET"])
def get_all_users():
    user_list = User.query.all()
    users_json = [user.to_json() for user in user_list]
    return generate_response(200, "users", users_json)


@app.route("/user/<id>", methods=["GET"])
def get_user_by_id(id):
    user = User.query.filter_by(id=id).first()
    user_json = user.to_json()
    return generate_response(200, "user", user_json)


@app.route("/user", methods=["POST"])
def create_user():
    body = request.get_json()
    try:
        user = User(name=body["name"], email= body["email"])
        db.session.add(user)
        db.session.commit()
        return generate_response(201, "user", user.to_json(), "Created !!")

    except Exception as e:
        print('Error: ', e)
        return generate_response(400, "user", {}, "Error on create !!")


@app.route("/user/<id>", methods=["PUT"])
def update_user(id):
    user = User.query.filter_by(id=id).first()
    body = request.get_json()

    try:
        if('name' in body):
            user.name = body['name']
        if('email' in body):
            user.email = body['email']
        
        db.session.add(user)
        db.session.commit()
        return generate_response(200, "user", user.to_json(), "Updated !!")

    except Exception as e:
        print('Error: ', e)
        return generate_response(400, "user", {}, "Error on update !!")


@app.route("/user/<id>", methods=["DELETE"])
def delete_usero(id):
    user = User.query.filter_by(id=id).first()

    try:
        db.session.delete(user)
        db.session.commit()
        return generate_response(200, "user", user.to_json(), "Deleted !!")

    except Exception as e:
        print('Error: ', e)
        return generate_response(400, "user", {}, "Error on delete !!")



def generate_response(status, type, conteudo, mensagem=False):
    body = {}
    body[type] = conteudo

    if(mensagem):
        body['mensagem'] = mensagem

    # dumps irá mudar obj para string
    # mimetype está definindo o tipo de retorno
    return Response(json.dumps(body), status=status, mimetype="application/json")
