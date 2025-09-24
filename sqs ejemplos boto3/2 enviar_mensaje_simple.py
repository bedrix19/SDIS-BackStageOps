import boto3
# Get the service resource
sqs = boto3.resource('sqs')

# Listamos todas las colas SQS existentes
for queue in sqs.queues.all():
    print(f'Imprimiendo la url de las colas: {queue.url}')

# Creamos y enviamos el mensaje
try:
    # Definimos la cola a utilizar
    queue = sqs.get_queue_by_name(QueueName='BackStageOps-queue')
    # Creamos el mensaje simple
    response = queue.send_message(MessageBody='Hola Mundo!')

    # Metadata del envío del mensaje
    print(response.get('MessageId'))
    print(response.get('MD5OfMessageBody'))

except:
    print("No se pudo enviar el mensaje, revisa el nombre de la cola SQS")
