# -*- coding: utf-8 -*-

"""Views for the 3 micrsoervices."""

from flask import request
import requests
from models import Place, People


class PlaceView():

    """CRUD Places"""

    def get(self):

        """GET"""

        res = Place.query.all()
        return [{'id' : u.id, 'name' : u.name} for u in res]

    def post(self):

        """POST"""

        place = Place(name=request.form.get('name'))
        place.insert()
        return {'id' : place.id, 'name' : place.name}, 201

    def delete(self, id_self):

        """DELETE"""

        place = Place.query.filter_by(id=id_self).first()
        place.remove()
        return "", 204

    def put(self, id_self):

        """PUT"""

        place = Place.query.filter_by(id=id_self).first()
        if request.form.get('name') is None:
            pl_name = place.name
        else:
            pl_name = request.form.get('name')
        place.update(pl_name)
        return {'id' : place.id, 'name' : place.name}


class PeopleView():

    """CRUD People"""

    def get(self):

        """GET"""

        res = People.query.all()
        return[{'id' : u.id, 'name' : u.name, 'isAlive':u.isAlive,
                'idplace' : u.idplace} for u in res]

    def post(self):

        """POST"""

        people = People(name=request.form.get('name'),
                        isAlive=request.form.get('isAlive'),
                        idplace=request.form.get('idplace'))
        if not people.IsCorrect(people.isAlive):
            return {'errMsg' : people.errMsg}, 400
        people.insert()
        return {'id' : people.id, 'name' : people.name,
                'isAlive' : people.isAlive,
                'idplace' : people.idplace}, 201

    def delete(self, id_self):

        """DELETE"""

        people = People.query.filter_by(id=id_self).first()
        people.remove()
        return "", 204

    def put(self, id_self):

        """PUT"""

        people = People.query.filter_by(id=id_self).first()
        if request.form.get('isAlive') is not None:
            if not people.IsCorrect(request.form.get('isAlive')):
                return {'errMsg': people.errMsg}, 400

        if request.form.get('name') is None:
            pe_name = people.name
        else:
            pe_name = request.form.get('name')

        if request.form.get('isAlive') is None:
            pe_alive = people.isAlive
        else:
            pe_alive = request.form.get('isAlive')

        if request.form.get('idplace') is None:
            pe_place = people.idplace
        else:
            pe_place = request.form.get('idplace')

        people.update(name=pe_name,
                      isAlive=pe_alive,
                      idplace=pe_place)
        return {'id' : people.id, 'name' : people.name,
                'isAlive' : people.isAlive, 'idplace' : people.idplace}


class GotView():

    """GET combination"""

    def __init__(self, host_places, host_people):

        """__init__"""

        self.host_places = host_places
        self.host_people = host_people

    def get(self):

        """GET"""

        requestplaces = requests.get('http://{}/v1/places'.format(self.host_places)).json()
        requestpeople = requests.get('http://{}/v1/people'.format(self.host_people)).json()
        response = []
        temp = {}
        for pl in requestplaces:
            pl["people"] = []
            temp[pl["id"]] = pl
        for pe in requestpeople:
            if pe["idplace"]:
                idplace = pe.pop("idplace")
                temp[idplace]["people"].append(pe)
        for v in temp.values():
            if v["people"]:
                response.append(v)
        return response
