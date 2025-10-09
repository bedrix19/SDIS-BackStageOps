import boto3
sqs = boto3.resource('sqs')

print("Probando conexión a AWS SQS...")

queue = sqs.get_queue_by_name(QueueName='BackStageOps-queue')
response = queue.send_message(MessageBody="json_event")

print(f"Mensaje enviado a SQS con ID: {response.get('MessageId')}\n")