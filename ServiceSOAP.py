from spyne import *
from spyne.server.wsgi import WsgiApplication
from spyne.protocol.soap import Soap11
from spyne import *
from math import sin, cos, acos, pi
import requests
import json
class tempsParcours(ServiceBase):
    @rpc(String, String, String, String, Integer, _returns=String)
    def tempsParcours(ctx, latA, longA, latB, longB, autonomie):
        proto="http://wxs.ign.fr/essentiels/itineraire/rest/route.json?origin=" + latA + "," + longA + "&destination=" + latB + "," + longB + "&method=DISTANCE&graphName=Voiture"
        rawdata= requests.get(proto)
        json_loaded = rawdata.json()
        result = json_loaded.get('duration')
        distance = json_loaded.get('distance')
        #if distance > autonomie:
        #   print("Une recharge est nécessaire")
        #else:
        #    print("pas de recharge nécessaire")
        print(result)
        return result

            
application = Application([tempsParcours], 'spyne.examples.hello.soap', in_protocol=Soap11(validator='lxml'), out_protocol=Soap11())
wsgi_application = WsgiApplication(application)
        
if __name__ == "__main__":
    from wsgiref.simple_server import make_server
    server = make_server('127.0.0.1', 8000, wsgi_application)
    server.serve_forever()