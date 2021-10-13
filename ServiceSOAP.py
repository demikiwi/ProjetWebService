from spyne import Application
from spyne import ServiceBase
from spyne import rpc
from spyne.server.wsgi import WsgiApplication
from spyne.protocol.soap import Soap11
from spyne import *
from math import sin, cos, acos, pi
from requests import *

class distanceGPS(ServiceBase):
    @rpc(Float, Float, Float, Float, _returns=Iterable(Float))
    def distanceGPS(ctx, latA, longA, latB, longB):
        """Retourne la distance en mètres entre les 2 points A et B connus grâce à
           leurs coordonnées GPS (en radians).
        """
        # Rayon de la terre en mètres (sphère IAG-GRS80)
        RT = 6378137
        # angle en radians entre les 2 points
        S = acos(sin(latA)*sin(latB) + cos(latA)*cos(latB)*cos(abs(longB-longA)))
        # distance entre les 2 points, comptée sur un arc de grand cercle
        result=S*RT
        yield result

class tempsParcours(ServiceBase):
    @rpc(String, String, String, String, _returns=Iterable(Float))
    def tempsParcours(ctx, latA, longA, latB, longB):
        proto="http://wxs.ign.fr/essentiels/itineraire/rest/route.json?origin=" + latA + "," + longA + "&destination=" + latB + "," + longB + "&method=DISTANCE&graphName=Voiture"
        rawdata= requests.get(proto)
        json = json.loads(rawdata)
        result = json["distance"]
        yield result
            
application = Application([tempsParcours], 'spyne.examples.hello.soap', in_protocol=Soap11(validator='lxml'), out_protocol=Soap11())
wsgi_application = WsgiApplication(application)
        
if __name__ == "__main__":
    from wsgiref.simple_server import make_server
    server = make_server('127.0.0.1', 8000, wsgi_application)
    server.serve_forever()