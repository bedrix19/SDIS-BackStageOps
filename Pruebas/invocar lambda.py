import boto3
import json
# implementación del conteo y almacenamiento de la data


lambda_client = boto3.client('lambda')
sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName='BackStageOps-queue')
queue_url = queue.url
nombre_funcion = "miPrimeraFuncion"

while True:

    for message in queue.receive_messages():
        # Get the custom author message attribute if it was set
        # Print out the body and author (if set)
        payload = message.body
        # attendee_id = payload.get('attendee_id')
        print(payload)
        # print('Hello, {0}!{1}'.format(message.body, author_text))
        # print(message)
        # Let the queue know that the message is processed
        try:
            response = lambda_client.invoke(
                FunctionName=nombre_funcion,
                InvocationType='RequestResponse',
                Payload=json.dumps(payload),
                # Payload=json.dumps(payload),
            )
            response_payload = json.load(response['Payload'])
            print(f"Respuesta de la Lambda: {response_payload}")
            # Debería ser 200 si todo fue bien
            print(f"Código de estado: {response['StatusCode']}")
            message.delete()
        except:
            print("Datos no enviados")
