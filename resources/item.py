from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This field cannot be left blank')

    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help='This field cannot be left blank')

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            return item.json(), 200
        return {'message': 'item not found'}, 404

    def post(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return {'message': "An item with name '{}' already exists".format(name)}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred"}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': 'item deleted'}

    def put(self, name):
        data = ItemModel.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            try:
                item = ItemModel(name, data['price'])
            except:
                return {"message": "An error occurred in insertion"}, 500
        else:
            try:
                item.price = data['price']
                item.store_id = data['store_id']
            except:
                return {"message": "An error occurred in update"}, 500

        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
