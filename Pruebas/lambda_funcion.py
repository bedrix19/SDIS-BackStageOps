import json


def lambda_handler(message, context):
    try:
        message = json.loads(message)
        attendee_id = message.get('attendee_id')
        print(f'Cliente {attendee_id} conectado.!')
        # Let the queue know that the message is processed
        # message.delete()
    except:
        print("No hay datos para procesar")

# import json


# def lambda_handler(event, context):
#     # Imprime el evento recibido para depuración
#     print(f"Evento recibido: {json.dumps(event)}")

#     # Extrae un nombre del evento o usa 'mundo' por defecto
#     nombre = event.get('nombre', 'mundo')

#     # Devuelve un saludo
#     return {
#         'statusCode': 200,
#         'body': json.dumps(f'¡Hola, {nombre} desde Lambda!')
#     }
