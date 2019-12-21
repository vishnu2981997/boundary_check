"""
routes
"""
import json
import logging

from flask import Flask
from flask_restplus import Api, Resource, fields

from utils import BoundaryCheck

APP = Flask(__name__)
APP.config['JSON_SORT_KEYS'] = False
API = Api(APP, version='1.0', title='Boundary check Api',
          description='given a polygon and a point verifies if the point lies within the polygon or not')
NS = API.namespace('boundaryCheck',
                   description='given a polygon and a point verifies if the point lies within the polygon or not')

CITY_MODEL = API.model('city', {
    "name": fields.String('Required - city name'),
    "boundaries": fields.Raw('Required - city boundaries')

})

LOCATE_MODEL = API.model('locate', {
    "name": fields.String('Required - city name'),
    "point": fields.Raw('Required - point')

})

CITIES = {}


@NS.route('/createCity')
class CreateCity(Resource):
    """
    Create City

    {
          "name": "a",
          "boundaries": {"coords":[[0, 0], [0, 2], [2, 4], [3, 4], [3, 1]]}
    }

    """

    message = {"code": 500, "response": "Internal server error"}

    @NS.expect(CITY_MODEL)
    def post(self):
        """
        create a city with boundaries
        """
        try:
            request = API.payload

            name = request.get("name", None)
            coords = None

            try:
                coords = json.dumps(request.get("boundaries", None))
            except TypeError as exe:
                logger.debug(exe)

            if coords not in [None, {}] and name is not None:

                if json.loads(coords):
                    coords = json.loads(coords)

                    if CITIES.get(name, None) is None:
                        CITIES[name] = coords["coords"]

                        self.message["response"] = request
                        self.message["code"] = 201
                    else:
                        self.message["response"] = "already exists"
                        self.message["code"] = 404
            else:
                self.message["response"] = "improper data or missing parameters"
                self.message["code"] = 404
        except Exception as exe:
            logger.debug(exe)

        return self.message


@NS.route('/checkBoundary')
class CheckBoundary(Resource):
    """
    Check Boundary

    for a given point check if it lies with in the plain


    {
          "name": "a",
          "point": {"coords":{"x": 2,"y": 2}}
    }
    """

    message = {"code": 500, "response": "Internal server error"}

    @NS.expect(LOCATE_MODEL)
    def post(self):
        """check if a given point is with in a desired city"""
        try:
            request = API.payload

            name = request.get("name", None)
            point = None

            try:
                point = json.dumps(request.get("point", None))
            except TypeError as exe:
                print(exe)

            if point not in [None, {}] and name is not None:

                if json.loads(point):
                    point = json.loads(point)

                    if name in CITIES:
                        point = [point["coords"]["x"], point["coords"]["y"]]
                        coords = CITIES[name]

                        bc = BoundaryCheck(coords)

                        if bc.exists(point=point):
                            self.message["response"] = "YES"
                            self.message["code"] = 200
                        else:
                            self.message["response"] = "NO"
                            self.message["code"] = 200
                    else:
                        self.message["response"] = "Unknown city"
                        self.message["code"] = 404
            else:
                self.message["response"] = "improper data or missing parameters"
                self.message["code"] = 404
        except Exception as exe:
            logger.debug(exe)

        return self.message


if __name__ == '__main__':
    logging.basicConfig(filename="logs.log", format='%(asctime)s %(message)s', filemode='a+')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    APP.run(host='0.0.0.0', debug=True, port=8008)
