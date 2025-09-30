import boto3

# Crea el cliente de SNS. Boto3 buscará las credenciales automáticamente.
sns_client = boto3.client(
    'sns', region_name='us-east-1')  # Especifica tu región

# Listamos todos tópicos existentes
lista_topicos = sns_client.list_topics()
for data in lista_topicos.get('Topics'):
    print(f"ARN de Topicos existentes -> {data.get('TopicArn')}")

# Una vez identificado el ARN, lo colocamos en la siguiente variable
ARN_TOPIC = "arn:aws:sns:us-east-1:637423199166:BackStage-notification"

suscripciones = sns_client.list_subscriptions_by_topic(
    TopicArn=ARN_TOPIC
)
for suscripcion in suscripciones.get('Subscriptions'):
    print(f"Protocolo utilizado: {suscripcion.get('Protocol')}")

# Ahora puedes usar el cliente, por ejemplo, para publicar un mensaje
response = sns_client.publish(
    # Colocar el ARN del topico creado
    TopicArn=ARN_TOPIC,
    Message='Sistemas Distribuidos 11 AM',
    Subject='Asunto de Prueba SNS'
)

print(f"Mensaje enviado con ID: {response['MessageId']}")
