import json


def lambda_handler(message, context):
    try:
        message = json.loads(message)
        user_id = message.get('attendee_id')
        print(f'Cliente {user_id} conectado.!')
        # Let the queue know that the message is processed
        # message.delete()
    except:
        print("No hay datos para procesar")
