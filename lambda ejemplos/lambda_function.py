import json


def lambda_handler(event, context):
    # Imprime el evento recibido para depuración
    print(f"Evento recibido: {json.dumps(event)}")

    # Extrae un nombre del evento o usa 'mundo' por defecto
    nombre = event.get('nombre', 'mundo')

    # Devuelve un saludo
    return {
        'statusCode': 200,
        'body': json.dumps(f'¡Hola, {nombre} desde Lambda!')
    }
