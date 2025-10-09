import os
import json
import random
import uuid
import time
import signal
from datetime import datetime

import boto3
sqs = boto3.resource('sqs')
sns = boto3.client("sns")

# --- Lista de ubicaciones ---
LOCATIONS = [
    "Ingreso Principal",
    "Escenario Principal", "Escenario 2", "Escenario 3",
    "Zona de Comida 1", "Zona de Comida 2",
    "Bar 1", "Bar 2", "Bar 3",
    "Baños 1", "Baños 2", "Baños 3",
    "Punto de Primeros Auxilios"
]

# --- Tipos de evento---
EVENT_TYPES = {
    "movimiento": 0.4,          # Probabilidad de que el asistente se mueve
    "alerta_seguridad": 0.01,   # Probabilidad de generar una alerta
    "fire": 0.005               # Probabilidad de generar una alerta de incendio
}

# Constantes para los niveles de observación
CROWD_LEVELS = ["bajo", "moderado", "alto", "abarrotado"]
QUEUE_LEVELS = ["corta", "media", "larga", "muy larga"]

# --- Configuración incial ---
QUEUE_NAME = os.environ.get("QUEUE_NAME", "BackStageOps-queue")
TOPIC_ARN = os.environ.get("TOPIC_ARN", "")

def choose_sns_topic():
    topics = sns.list_topics().get("Topics", [])
    if not topics:
        print("No hay tópicos SNS disponibles.")
        return None
    print("Tópicos SNS disponibles:")
    print("[0] Ninguno")
    for i, topic in enumerate(topics, start=1):
        print(f"[{i}] {topic.get('TopicArn')}")
    while True:
        choice = input("Selecciona un tópico (número): ").strip()
        if not choice.isdigit():
            print("Introduce un número válido.")
            continue
        if(choice == "0"):
            return None
        idx = int(choice) - 1
        if 0 <= idx < len(topics):
            return topics[idx].get("TopicArn")
        else:
            print("Índice fuera de rango.")

def choose_location(prompt="Elige ubicación"):
    for i, loc in enumerate(LOCATIONS, start=1):
        print(f"[{i}] {loc}")
    while True:
        choice = input(f"{prompt} (número): ").strip()
        if not choice.isdigit():
            print("Introduce un número válido.")
            continue
        idx = int(choice) - 1
        if 0 <= idx < len(LOCATIONS):
            return LOCATIONS[idx]
        else:
            print("Índice fuera de rango.")

def send_sqs(payload: str):
    if not QUEUE_NAME:
        print("No hay QUEUE_URL configurada. No se envía nada.")
        return False
    try:
        queue = sqs.get_queue_by_name(QueueName='BackStageOps-queue')
        resp = queue.send_message(MessageBody=payload)
        print("Enviado a SQS MessageId=%s", resp.get("MessageId"))
        return True
    except Exception as e:
        print("Error enviando a SQS: %s", e)
        return False

# --- Bucle Principal de la Simulación ---
if __name__ == "__main__":
    print("\n--- Iniciando Attendee Validator ---\n")
    
    topic_choosed = choose_sns_topic()
    while topic_choosed is not None:
        print(f"Tópico SNS seleccionado: {topic_choosed}")
        try:
            sns.subscribe(
                TopicArn=topic_choosed,
                Protocol='email',
                Endpoint=input("Introduce tu email para recibir alertas: ").strip(),
                ReturnSubscriptionArn=True
            )
            print("Suscripción realizada con éxito.")
            topic_choosed = choose_sns_topic()
        except Exception as e:
            print(f"Error al suscribirse al tópico SNS: {e}")

    user_id = str(uuid.uuid4())
    try:
        while 1:
            print("Opciones:")
            print("[1] Moverse")
            print("[2] Alertar actividad sospechosa")
            print("[3] Fuego")
            print("\n'q' para salir")
            choice = input("Selecciona opción: ").strip()
            if choice in ("q", "Q", "exit"):
                print("Usuario solicitó salir.")
                break
            if choice == "1":
                # Movimiento
                dest = choose_location("Selecciona destino")
                payload = json.dumps({
                    "user_id": user_id,
                    "role": "staff",
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    "event_type": "movimiento",
                    "data": {"destino": dest}
                })
                send_sqs(payload)
            elif choice == "2":
                # Alerta sospechosa
                loc = choose_location("Ubicación del suceso")
                desc = input("Descripción breve del incidente: ").strip()
                severity = input("Severidad (baja/normal/alta): ").strip() or "normal"
                payload = json.dumps({
                    "user_id": user_id,
                    "role": "staff",
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    "event_type": "alerta_seguridad",
                    "data": {"location": loc, "descripcion": desc, "severidad": severity}
                })
                send_sqs(payload)
            elif choice == "3":
                # Fuego
                loc = choose_location("Ubicación del fuego")
                level = input("Nivel de fuego (pequeño/medio/grave): ").strip() or "medio"
                has_people = input("¿Hay personas en la zona? (s/n): ").strip().lower() in ("s", "si", "y", "yes")
                payload = json.dumps({
                    "user_id": user_id,
                    "role": "staff",
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    "event_type": "fuego",
                    "data": {"location": loc, "nivel": level, "hay_personas": has_people}
                })
                send_sqs(payload)
            else:
                print("Opción no válida. Usa 1/2/3 o q para salir.")

    except KeyboardInterrupt:
        print("\n--- Simulación detenida. ---")
