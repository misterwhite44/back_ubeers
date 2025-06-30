from flask_restx import Namespace, Resource, fields
from models import db, User
from datetime import datetime

users_ns = Namespace("users", description="User operations")

user_model = users_ns.model("User", {
    "id": fields.Integer(readonly=True),
    "pseudo": fields.String(required=True),
    "email": fields.String(required=True),
    "password": fields.String(required=True),
    "address": fields.String,
    "phone_number": fields.String,
    "created_at": fields.DateTime(readonly=True),
    "updated_at": fields.DateTime(readonly=True),
})

@users_ns.route("/")
class UserList(Resource):
    @users_ns.marshal_list_with(user_model)
    def get(self):
        return User.query.all()

    @users_ns.expect(user_model)
    @users_ns.marshal_with(user_model, code=201)
    def post(self):
        data = users_ns.payload
        user = User(
            pseudo=data["pseudo"],
            email=data["email"],
            password=data["password"],
            address=data.get("address"),
            phone_number=data.get("phone_number"),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db.session.add(user)
        db.session.commit()
        return user, 201

@users_ns.route("/<int:id>")
@users_ns.response(404, "User not found")
class UserResource(Resource):
    @users_ns.marshal_with(user_model)
    def get(self, id):
        return User.query.get_or_404(id)

    @users_ns.expect(user_model)
    @users_ns.marshal_with(user_model)
    def put(self, id):
        user = User.query.get_or_404(id)
        data = users_ns.payload
        user.pseudo = data.get("pseudo", user.pseudo)
        user.email = data.get("email", user.email)
        user.password = data.get("password", user.password)
        user.address = data.get("address", user.address)
        user.phone_number = data.get("phone_number", user.phone_number)
        user.updated_at = datetime.utcnow()
        db.session.commit()
        return user

    @users_ns.response(204, "User deleted")
    def delete(self, id):
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return '', 204
