import zeep

wsdl = 'http://127.0.0.1:8000/?WSDL'
client = zeep.Client(wsdl=wsdl)

result = client.service.tempsParcours(-0.6756162643432286,45.8786949940647,-0.34465312957759703,46.015243021856286)

print(result)