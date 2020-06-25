# -*- coding: utf-8 -*-
"""CRUD microservice for people"""

from flask_restplus import Api
from flask_restplus import  Resource
import views as v
from app import create_app

app = create_app()
api = Api()
api.init_app(app)
HOST_PEOPLE = "people-microservice:8082"


@api.route("/v1/people")

class PeopleList(Resource):

    """GET and POST"""

    def get(self):

        """GET"""

        return v.PeopleView().get()

    def post(self):

        """POST"""

        return v.PeopleView().post()


@api.route("/v1/people/<int:idpeople>")

class PeopleModify(Resource):

    """PUT and DELETE"""

    def put(self, idpeople):

        """PUT"""

        return v.PeopleView().put(id_self=idpeople)

    def delete(self, idpeople):

        """DELETE"""

        return v.PeopleView().delete(id_self=idpeople)


if __name__ == "__main__":
    app.run(debug=True, host=HOST_PEOPLE.split(":")[0], port=HOST_PEOPLE.split(":")[1])
