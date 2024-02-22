from sqlalchemy import exc
from flask import request
from flask_jwt_extended import create_access_token, current_user, jwt_required
from flask_restful import Resource

from modelos import db, Usuario, UsuarioSchema, Administrador, TipoUsuario, Propietario

usuario_schema = UsuarioSchema()


class VistaSignIn(Resource):

    def post(self):
        if request.json["tipo"] == "ADMINISTRADOR" :
            nuevo_administrador = Administrador()
            nuevo_administrador.usuario=request.json["usuario"]
            nuevo_administrador.contrasena=request.json["contrasena"]
            nuevo_administrador.tipo=TipoUsuario.ADMINISTRADOR
            
            db.session.add(nuevo_administrador)
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print("(37)error -> ", e)
                return {
                    "mensaje": "Ya existe un usuario con este identificador"
                }, 400
            token_de_acceso = create_access_token(identity=nuevo_administrador.id)
            # db.session.expunge(nuevo_administrador)
            return {
                "mensaje": "usuario creado", 
                "token": token_de_acceso, 
                "id": nuevo_administrador.id
            }, 201
        elif request.json["tipo"] == "PROPIETARIO" :
            nuevo_propietario = Propietario()
            nuevo_propietario.usuario=request.json["usuario"]
            nuevo_propietario.contrasena=request.json["contrasena"]
            nuevo_propietario.tipo=TipoUsuario.PROPIETARIO

            nuevo_propietario.nombre=request.json["nombre"]
            nuevo_propietario.apellido=request.json["apellido"]
            nuevo_propietario.telefono=request.json["telefono"]
            nuevo_propietario.correo_electronico=request.json["correo_electronico"]

            db.session.add(nuevo_propietario)
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print("(37)error -> ", e)
                return {
                    "mensaje": "Ya existe un usuario con este identificador"
                }, 400
            token_de_acceso = create_access_token(identity=nuevo_propietario.id)
            # db.session.expunge(nuevo_propietario)
            return {
                "mensaje": "usuario creado", 
                "token": token_de_acceso, 
                "id": nuevo_propietario.id
            }, 201
        else:
            return {
                "mensaje": "El tipo de usuario recibido no es valido"
            }, 400
      

    @jwt_required()
    def put(self, id_usuario):
        usuario_token = current_user
        if id_usuario != current_user.id:
            return {"mensaje": "Peticion invalida"}, 400
        usuario_token.contrasena = request.json.get("contrasena", usuario_token.contrasena)
        db.session.commit()
        return usuario_schema.dump(usuario_token)
