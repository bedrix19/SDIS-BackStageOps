import boto3
# Get the service resource
sqs = boto3.resource('sqs')

# Listamos todas las colas SQS existentes
for queue in sqs.queues.all():
    print(f'Imprimiendo la url de las colas: {queue.url}')

# Creamos y enviamos los mensajes en una sola cola
try:
    # Obtenemos la Queue a utilizar
    queue = sqs.get_queue_by_name(QueueName='BackStageOps-queue')
    # Creamos los mensajes con diferentes metadatos incrustados
    response = queue.send_messages(Entries=[
        {
            'Id': '1',
            'MessageBody': 'BackStageOps'
        },
        {
            'Id': '2',
            'MessageBody': 'SDIS',
            'MessageAttributes': {
                'Author': {
                    'StringValue': 'Grupo 3',
                    'DataType': 'String'
                }
            }
        }
    ])

    # Imprime los errores de envío de los mensajes
    print(f"Errores de envío: {response.get('Failed')}")

    # Metadata de envío de los mensajes
    if response.get('Successful') is not None:
        metadata_response = response.get('Successful')
        for value in metadata_response:
            print(f"Valores de la cola {value.get('Id')}")
            for k, v in value.items():
                print(f"- {k}: {v}")
            print(f"---------------------------------------------------")

except:
    print("No se pudo enviar los mensajes, revisa las colas SQS")
