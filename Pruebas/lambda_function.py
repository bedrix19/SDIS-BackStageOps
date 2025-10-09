import json


def lambda_handler(message, context):
    try:
        message = json.loads(message)
        user_id = message.get('user_id')
        print(f'User {user_id} conectado.!')
        # Let the queue know that the message is processed
        # message.delete()
    except:
        print("No hay datos para procesar")
