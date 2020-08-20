from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.store import StoreModel


class Store(Resource):

    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)

        if store:
            return store.json(), 200
        return {'message': 'store not found'}, 404

    def post(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return {'message': "An store with name '{}' already exists".format(name)}, 400

        store = StoreModel(name)

        try:
            store.save_to_db()
        except:
            return {"message": "An error occurred"}, 500

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {'message': 'store deleted'}


class StoreList(Resource):
    def get(self):
        return {'stores': list(map(lambda x: x.json(), StoreModel.query.all()))}
