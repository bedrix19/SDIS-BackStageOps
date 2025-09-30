import boto3

# Crea el cliente de SNS. Boto3 buscará las credenciales automáticamente.
sns_client = boto3.client(
    'sns', region_name='us-east-1')  # Especifica tu región

# Listamos todos tópicos existentes
lista_topicos = sns_client.list_topics()
for data in lista_topicos.get('Topics'):
    print(f"ARN de Topicos existentes -> {data.get('TopicArn')}")

response = sns_client.create_topic(
    # Los nombres declarados deben ser con guion para simular los espacios sino puede haber errores
    # Para FIFO se debe declarar al final del nombre .fifo
    Name='Topico-de-Prueba',
    Attributes={
        'DisplayName': 'Alias del Tópico'  # Solo para suscripciones a SMS
    },
)

# Obtener el ARN del tópico creado
print(f"{response.get('TopicArn')}")
