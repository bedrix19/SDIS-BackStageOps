import boto3
# Get the service resource
sqs = boto3.resource('sqs')

# Creamos la cola SQS nombrada = "BackStageOps-queue"
try:
    queue = sqs.create_queue(QueueName='BackStageOps-queue',
                             Attributes={'DelaySeconds': '5'})

    # Informacion de la cola creada
    print(f"Url de la Queue: {queue.url}")
    print(f"Delay: {queue.attributes.get('DelaySeconds')}")
except:
    print("La cola no se pudo crear porque ya existe una con el mismo nombre")
