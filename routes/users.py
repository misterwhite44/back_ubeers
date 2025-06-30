from flask_restx import Namespace, Resource, fields
from models import db, User

users_ns = Namespace("users", description="User operations")

user_model = users_ns.model("User", {
    "id": fields.Integer(readonly=True),
    "email": fields.String(required=True),
    "password": fields.String(required=True)
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
        user = User(**data)
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
        for key, value in users_ns.payload.items():
            setattr(user, key, value)
        db.session.commit()
        return user

    @users_ns.response(204, "User deleted")
    def delete(self, id):
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return '', 204
