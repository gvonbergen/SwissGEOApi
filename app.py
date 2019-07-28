import json
import falcon

from shapely.geometry import Point, shape

class SwissIdentifier:

    def __init__(self):
        self.coordinates = None

        with open('geodata/CHE.json', 'r') as jfile:
            self.coordinates = shape(json.loads(jfile.read()))

    def on_get(self, req, resp):

        try:
            lat, lng = float(req.params['lat']), float(req.params['lng'])
        except (KeyError, ValueError):
            raise falcon.HTTPBadRequest(f'Required parameters: lat, lng')

        # Lng / lat vice versa
        coordinates = Point(lng, lat)

        result = {'result': False}

        try:
            if 5.95590199 <= lng <= 10.49217186 and 45.81795857 <= lat <= 47.80845449:
                if self.coordinates.contains(coordinates):
                    result = {'result': True}
        except Exception:
            pass

        resp.body = json.dumps(result)

api = application = falcon.API()

identifier = SwissIdentifier()

api.add_route('/ident', identifier)