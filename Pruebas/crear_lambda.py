import boto3
import json

lambda_client = boto3.client('lambda')

with open('deployment_package.zip', 'rb') as f:
    zipped_code = f.read()

role_arn = "arn:aws:iam::637423199166:role/LabRole"

response = lambda_client.create_function(
    FunctionName='BackStageFunction',
    Runtime='python3.9',
    Role=role_arn,
    Handler='lambda_function.lambda_handler',  # archivo.método
    Code={'ZipFile': zipped_code},
    Description='Función creada con Boto3 para el proyecto BackStageOps',
    Timeout=10,  # en segundos
    MemorySize=128  # en MB
)
