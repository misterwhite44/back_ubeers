from flask_restx import Namespace, Resource, fields
from models import db, User

api = Namespace("users", description="User operations")

user_model = api.model("User", {
    "id": fields.Integer(readonly=True),
    "email": fields.String(required=True),
    "password": fields.String(required=True)
})

@api.route("/")
class UserList(Resource):
    @api.marshal_list_with(user_model)
    def get(self):
        return User.query.all()

    @api.expect(user_model)
    @api.marshal_with(user_model, code=201)
    def post(self):
        data = api.payload
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        return user, 201

@api.route("/<int:id>")
@api.response(404, "User not found")
class UserResource(Resource):
    @api.marshal_with(user_model)
    def get(self, id):
        return User.query.get_or_404(id)

    @api.expect(user_model)
    @api.marshal_with(user_model)
    def put(self, id):
        user = User.query.get_or_404(id)
        for key, value in api.payload.items():
            setattr(user, key, value)
        db.session.commit()
        return user

    @api.response(204, "User deleted")
    def delete(self, id):
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return '', 204
