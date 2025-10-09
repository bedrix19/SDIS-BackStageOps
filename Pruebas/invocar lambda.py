import boto3
import json
from datetime import datetime

# --- Configuración ---
SQS_QUEUE_NAME = 'BackStageOps-queue'
DYNAMODB_TABLE_NAME = 'BackstageOPSDB'
SNS_TOPIC_STAFF = "arn:aws:sns:us-east-1:637423199166:BackStageSNS-Staff"

# --- Clientes de AWS ---
sqs = boto3.resource('sqs')
dynamodb = boto3.resource('dynamodb')
sns_client = boto3.client(
    'sns', region_name='us-east-1')  # Especifica tu región
suscripciones = sns_client.list_subscriptions_by_topic(
    TopicArn=SNS_TOPIC_STAFF
)

# LISTA DE TIPOS DE EVENTOS DE EMERGENCIA
eventos_emergencia = ["SUSPICIOUS ACTIVITY", "FIRE"]
#

# --- Lógica Principal ---
try:
    queue = sqs.get_queue_by_name(QueueName=SQS_QUEUE_NAME)
    table = dynamodb.Table(DYNAMODB_TABLE_NAME)
    print(f"Escuchando mensajes en la cola: {SQS_QUEUE_NAME}...")

    while True:
        # Procesando 10 mensajes por bucle (reemplazar por variable para escalabilidad)
        messages = queue.receive_messages(
            MaxNumberOfMessages=100, WaitTimeSeconds=1)

        if not messages:
            continue  # Si no hay mensajes, se reinicia el bucle

        for message in messages:
            print(f"Procesando mensaje ID: {message.message_id}")
            try:
                # Cargar el payload
                payload_dict = json.loads(message.body)

                # Convertir el timestamp a número (cambio necesario)
                iso_timestamp = payload_dict.get('timestamp')
                if iso_timestamp:
                    dt_object = datetime.fromisoformat(
                        iso_timestamp.replace('Z', '+00:00'))
                    payload_dict['timestamp'] = int(dt_object.timestamp())

                # Guardar la data en Dynamo
                table.put_item(Item=payload_dict)
                print(
                    f"  -> Ítem para user_id '{payload_dict['user_id']}' guardado en DynamoDB.")

                # Intermedio prueba SNS ----------------------
                if payload_dict['event_type'] in eventos_emergencia:
                    response_sns = sns_client.publish(
                        TopicArn=SNS_TOPIC_STAFF,
                        Message=f"Se ha detectado {payload_dict['event_type']} en {payload_dict['location']}",
                        Subject=f"Se ha detectado {payload_dict['event_type']} en {payload_dict['location']}"
                    )
                print(
                    f"  -> Evento tipo '{payload_dict['event_type']}' detectado y notificado por GMAIL.")
                # ---------------------------------------------

                # Eliminar el mensaje de la cola
                message.delete()
                print(
                    f"  -> Mensaje {message.message_id} eliminado de la cola.")

            except Exception as e:
                print(
                    f"  -> ERROR al procesar el mensaje {message.message_id}: {e}")

except KeyboardInterrupt:
    print("\n--- Proceso detenido por el usuario. ---")
except Exception as e:
    print(f"Ocurrió un error crítico: {e}")
