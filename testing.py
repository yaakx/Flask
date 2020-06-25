# -*- coding: utf-8 -*-

"""Unit Test for all the microservices."""

import unittest
import random
import requests
from app import create_app
from models import db, People, Place

app = create_app()
app.app_context().push()


class TestBase(unittest.TestCase):

    """This will be done before and after each test respectively."""

    def setUp(self):

        """Setting up a database for the test before each test."""

        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://gotuser:julenflask@localhost/got_test'
        db.create_all()

    def tearDown(self):

        """Erasing the database after each test."""

        db.session.remove()
        db.drop_all()


class TestModel(TestBase):

    """Tests for the Models"""

    def test_place_model(self):

        """Test the class Place from the models and all its functions."""

        place = Place(name="test_name")
        place.insert()
        self.assertEqual(place.query.count(), 1)
        place.update(name="test_name2")
        self.assertEqual(place.name, "test_name2")
        place.remove()
        self.assertEqual(place.query.count(), 0)

    def test_people_model_null(self):

        """Test the class People from the models when idplace is null."""

        people = People(name="test_name", isAlive=1, idplace=None)
        people.insert()
        self.assertEqual(people.query.count(), 1)

    def test_people_model(self):

        """Test the class People from models and all its functions"""

        place = Place(name="test_name")
        place.insert()
        people = People(name="test_name", isAlive=random.choice([0, 1]), idplace=random.choice([None, 1]))
        people.insert()
        self.assertEqual(people.query.count(), 1)
        people.update(name="test_name2", isAlive=random.choice([0, 1]), idplace=random.choice([None, 1]))
        self.assertEqual(people.name, "test_name2")
        people.remove()
        self.assertEqual(people.query.count(), 0)


class TestView(TestBase):

    """Tests for the views"""

    def test_place_views(self):

        """Test CRUD in Place"""

        response = requests.get("http://place-microservice:8081/v1/places")
        self.assertEqual(response.status_code, 200)
        response_post = requests.post("http://place-microservice:8081/v1/places", data={"name":"test_name"})
        self.assertEqual(response_post.status_code, 201)
        id_temp = response_post.json()["id"]
        response_put = requests.put("http://place-microservice:8081/v1/places/{}".format(id_temp), data={"name":"put_name"})
        self.assertEqual(response_put.status_code, 200)
        response_del = requests.delete("http://place-microservice:8081/v1/places/{}".format(id_temp))
        self.assertEqual(response_del.status_code, 204)

    def test_people_view(self):

        """Test CRUD in People"""

        place_test = requests.post("http://place-microservice:8081/v1/places", data={"name":"test_name"})
        place_id = place_test.json()["id"]
        response = requests.get("http://people-microservice:8082/v1/people")
        self.assertEqual(response.status_code, 200)
        response_post = requests.post("http://people-microservice:8082/v1/people", data={"name":"test_name", "isAlive":random.choice([0, 1]), "idplace":random.choice([None, place_id])})
        self.assertEqual(response_post.status_code, 201)
        id_temp = response_post.json()["id"]
        response_put = requests.put("http://people-microservice:8082/v1/people/{}".format(id_temp), data={"name":"put_name", "isAlive":random.choice([0, 1]), "idplace":random.choice([None, place_id])})
        self.assertEqual(response_put.status_code, 200)
        response_del = requests.delete("http://people-microservice:8082/v1/people/{}".format(id_temp))
        self.assertEqual(response_del.status_code, 204)
        requests.delete("http://place-microservice:8081/v1/places/{}".format(place_id))

    def test_got_view(self):

        """Test combination of both Api"""

        place_test = requests.post("http://place-microservice:8081/v1/places", data={"name":"test_place"})
        place_id = place_test.json()["id"]
        people_test = requests.post("http://people-microservice:8082/v1/people", data={"name":"test_people", "isAlive":random.choice([0, 1]), "idplace": place_id})
        people_id = people_test.json()["id"]
        response_get=requests.get("http://got-microservice:8083/v1/places").json()
        place = response_get[-1]
        people = place["people"][0]["name"]
        self.assertEqual(place["name"], "test_place")
        self.assertEqual(people, "test_people")
        requests.delete("http://place-microservice:8081/v1/places/{}".format(place_id))
        requests.delete("http://people-microservice:8082/v1/people/{}".format(people_id))

if __name__ == "__main__":
    unittest.main()
