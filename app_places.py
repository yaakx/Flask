# -*- coding: utf-8 -*-

"""CRUD microservice for places"""

from flask_restplus import Api
from flask_restplus import  Resource
import views as v
from app import create_app

app = create_app()
api = Api()
api.init_app(app)
HOST_PLACES = "place-microservice:8081"


@api.route("/v1/places")

class PlacesList(Resource):

    """GET and POST"""

    def get(self):

        """GET"""

        return v.PlaceView().get()

    def post(self):

        """POST"""

        return v.PlaceView().post()


@api.route("/v1/places/<int:idplace>")

class PlacesModify(Resource):

    """PUT and DELETE"""

    def put(self, idplace):

        """PUT"""

        return v.PlaceView().put(id_self=idplace)

    def delete(self, idplace):

        """DELETE"""

        return v.PlaceView().delete(id_self=idplace)


if __name__ == "__main__":
    app.run(debug=True, host=HOST_PLACES.split(":")[0], port=HOST_PLACES.split(":")[1])
