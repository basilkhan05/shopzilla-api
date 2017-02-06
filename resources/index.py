from flask_restful import Resource
from flask import redirect, url_for

class Index(Resource):
    def get(self):
        return redirect(url_for("products"))