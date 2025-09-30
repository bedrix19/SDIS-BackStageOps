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
    print(
        f"Protocolo(s) utilizado(s) del tópico seleccionado: {suscripcion.get('Protocol')}")
