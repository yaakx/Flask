# -*- coding: utf-8 -*-
"""CRUD microservice that combines places and people"""

from flask_restplus import Api
from flask_restplus import  Resource
import views as v
from app import create_app

app = create_app()
api = Api()
api.init_app(app)
HOST_PLACES = "place-microservice:8081"
HOST_PEOPLE = "people-microservice:8082"
HOST_COMBINATION = "got-microservice:8083"


@api.route("/v1/places")

class GotList(Resource):

    """GET"""

    def get(self):

        """GET"""

        return v.GotView(host_places=HOST_PLACES, host_people=HOST_PEOPLE).get()


if __name__ == "__main__":
    app.run(debug=True, host=HOST_COMBINATION.split(":")[0], port=HOST_COMBINATION.split(":")[1])
