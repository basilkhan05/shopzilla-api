from flask import Flask
from flask_pymongo import PyMongo
from flask_restful import Api
from resources.index import Index 
from resources.product import Product

app = Flask(__name__)
app.config["MONGO_DBNAME"] = "shopzilla"
mongo = PyMongo(app, config_prefix='MONGO')

api = Api(app)
api.add_resource(Index, "/", endpoint="index")
api.add_resource(Product, "/api", endpoint="products")
api.add_resource(Product, "/api/product/<string:product_id>", endpoint="product_id")
api.add_resource(Product, "/api/store/<string:store>", endpoint="store")

if __name__ == "__main__":
    app.run(debug=True)