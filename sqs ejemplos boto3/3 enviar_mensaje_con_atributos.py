import boto3
# Get the service resource
sqs = boto3.resource('sqs')

# Listamos todas las colas SQS existentes
for queue in sqs.queues.all():
    print(f'Imprimiendo la url de las colas: {queue.url}')

# Creamos y enviamos el mensaje
try:
    # Obtenemos la Queue a utilizar
    queue = sqs.get_queue_by_name(QueueName='BackStageOps-queue')
    # Creamos el mensaje con metadatos incrustados
    response = queue.send_message(MessageBody='Mensaje de Prueba', MessageAttributes={
        'Author': {
            'StringValue': 'Grupo 3 - SDIS',
            'DataType': 'String'
        }
    })

    # Metadata del envío del mensaje
    print(response.get('MessageId'))
    print(response.get('MD5OfMessageBody'))

except:
    print("No se pudo enviar el mensaje, revisa el nombre de la cola SQS")
