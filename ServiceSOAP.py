from spyne import *
from spyne.server.wsgi import WsgiApplication
from spyne.protocol.soap import Soap11
from spyne import *
from math import sin, cos, acos, pi
import requests
import json

class tempsParcours(ServiceBase):
    @rpc(String, String, String, String, String, _returns=String)
    def tempsParcours(ctx, latA, longA, latB, longB, autonomie):
        proto="http://wxs.ign.fr/essentiels/itineraire/rest/route.json?origin=" + latA + "," + longA + "&destination=" + latB + "," + longB + "&method=DISTANCE"
        rawdata= requests.get(proto)
        json_loaded = rawdata.json()
        duration = json_loaded.get('duration')
        distance = json_loaded.get('distance')

        print("distance = " + distance)
        print("autaunomie = " + autonomie)

        if distance < autonomie:
            # result = '{"duree":" + duration + ",message : 'pas de recharge necessaire'}"
            result = json.dumps({'duree': duration,'message':'pas de recharge necessaire'})
        else:
            distance = distance[:-3]
            distanceINT = float(distance)
            autonomieINT = float(autonomie)
            restant = (distanceINT-autonomieINT)
            temps = round(0.2*restant)
            tempsSTR = str(temps)
            # result = ("{duree : '" + duration + "',temps_recharge : '" + tempsSTR + "',message : 'une recharge est necessaire'}")
            result = json.dumps({'duree': duration,'message':'pas de recharge necessaire','temps_recharge': tempsSTR})
        return result

            
application = Application([tempsParcours], 'spyne.examples.hello.soap', in_protocol=Soap11(validator='lxml'), out_protocol=Soap11())
wsgi_application = WsgiApplication(application)

if __name__ == "__main__":
    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0', 80, wsgi_application)
    server.serve_forever()
