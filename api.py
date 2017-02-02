# -*- coding: utf-8 -*-

from flask import Flask, jsonify, url_for, redirect, request
from flask_pymongo import PyMongo
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
app.config["MONGO_DBNAME"] = "shopzilla"
mongo = PyMongo(app, config_prefix='MONGO')
APP_URL = "http://127.0.0.1:5000"


class Product(Resource):
    def get(self, product_id=None, store=None):
        data = []
        URLparser = reqparse.RequestParser()
        URLparser.add_argument('limit', type=str)
        args = URLparser.parse_args()
        limit = int(args['limit']) if args['limit'] else 10 

        # print('----------------HELLO -------------' + parser.parse_args())

        if product_id:
            store_info = mongo.db.product.find_one({"id": int(product_id)}, {"_id": 0})
            if store_info:
                return jsonify({"status": "ok", "data": store_info})
            else:
                return {"response": "no product found for {}".format(product_id)}

        elif store:
            cursor = mongo.db.product.find({"store": store}, {"_id": 0}).limit(limit)
            for product in cursor:
                product['url'] = APP_URL + url_for('products') + "/" + str(product.get('id'))
                data.append(product)

            return jsonify({"store": store, "products": data})

        else:
            cursor = mongo.db.product.find({}, {"_id": 0, "update_time": 0}).limit(limit)

            for product in cursor:
                print(product)
                product['url'] = APP_URL + url_for('products') + "/" + str(product.get('id'))
                data.append(product)

            return jsonify({"response": data})

    def post(self):
        data = request.get_json()
        if not data:
            data = {"response": "ERROR"}
            return jsonify(data)
        else:
            product_id = data.get('id')
            if product_id:
                if mongo.db.product.find_one({"id": int(product_id)}):
                    return {"response": "product already exists."}
                else:
                    mongo.db.product.insert(data)
            else:
                return {"response": "product id number is missing"}

        return redirect(url_for("products"))

    def put(self, product_id):
        data = request.get_json()
        mongo.db.product.update({'id': int(product_id)}, {'$set': data})
        return redirect(url_for("products"))

    def delete(self, product_id):
        mongo.db.product.remove({'id': int(product_id)})
        return redirect(url_for("products"))


class Index(Resource):
    def get(self):
        return redirect(url_for("products"))


api = Api(app)
api.add_resource(Index, "/", endpoint="index")
api.add_resource(Product, "/api", endpoint="products")
api.add_resource(Product, "/api/product/<string:product_id>", endpoint="product_id")
api.add_resource(Product, "/api/store/<string:store>", endpoint="store")

if __name__ == "__main__":
    app.run(debug=True)