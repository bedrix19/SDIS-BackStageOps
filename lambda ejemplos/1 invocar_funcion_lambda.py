import boto3
import json

lambda_client = boto3.client('lambda')

nombre_funcion = "miPrimeraFuncion"

payload = {
    "nombre": "BackStage-Test"
}

response = lambda_client.invoke(
    FunctionName=nombre_funcion,
    InvocationType='RequestResponse',
    Payload=json.dumps(payload),
)

response_payload = json.load(response['Payload'])
print(f"Respuesta de la Lambda: {response_payload}")
# Debería ser 200 si todo fue bien
print(f"Código de estado: {response['StatusCode']}")
