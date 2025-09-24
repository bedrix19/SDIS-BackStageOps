import boto3
# Get the service resource
sqs = boto3.resource('sqs')

# Listamos todas las colas SQS existentes
for queue in sqs.queues.all():
    print(f'Imprimiendo la url de las colas: {queue.url}')

# Obtenemos los datos de la cola a utilizar
try:
    queue = sqs.get_queue_by_name(QueueName='BackStageOps-queue')

    # Informacion de la cola utilizada
    print(f"Url de la Queue: {queue.url}")
    print(f"Delay: {queue.attributes.get('DelaySeconds')}")
except:
    print("El servicio SQS consultado no existe")
