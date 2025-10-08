import json
import random
import uuid
import time
from datetime import datetime

import boto3
sqs = boto3.resource('sqs')

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
    "movimiento": 0.4,       # Probabilidad de que el asistente se mueve
    "alerta_seguridad": 0.01  # Probabilidad de generar una alerta
}

# Constantes para los niveles de observación
CROWD_LEVELS = ["bajo", "moderado", "alto", "abarrotado"]
QUEUE_LEVELS = ["corta", "media", "larga", "muy larga"]


class Attendee:
    """
    Representa a un asistente del festival. En cada acción, reporta un
    estado completo que incluye signos vitales, y observaciones del entorno.
    """

    def __init__(self):
        self.attendee_id = str(uuid.uuid4())
        self.location = "Ingreso Principal"
        self.heart_rate = random.randint(70, 90)
        print(f"Asistente {self.attendee_id} creado en {self.location}")

    def _update_vitals_and_observations(self):
        """
        Calcula el estado actual del asistente y su entorno.
        Esta es la función clave para generar los datos base.
        """
        # 1. Actualizar Ritmo Cardíaco
        if "Escenario" in self.location:
            self.heart_rate = random.randint(110, 140)
        elif "Zona de Comida" in self.location or "Punto de Primeros Auxilios" in self.location:
            self.heart_rate = random.randint(65, 85)
        else:  # Bares, baños
            self.heart_rate = random.randint(80, 110)
        self.heart_rate += random.randint(-3, 3)

        # 2. Determinar Nivel de Multitud
        crowd_level = "no aplica"
        if "Escenario" in self.location or "Zona de Comida" in self.location:
            crowd_level = random.choice(CROWD_LEVELS)

        # 3. Determinar Longitud de la Cola
        queue_length = "no aplica"
        if "Bar" in self.location or "Baños" or "Punto de Primeros Auxilios" in self.location:
            queue_length = random.choice(QUEUE_LEVELS)

        return {
            "heart_rate_bpm": self.heart_rate,
            "nivel_multitud": crowd_level,
            "longitud_cola": queue_length
        }

    def simulate_action(self):
        """
        Simula una acción principal (moverse o alerta) y genera un
        payload JSON completo con todos los datos de estado.
        """
        chosen_event = random.choices(
            list(EVENT_TYPES.keys()),
            weights=list(EVENT_TYPES.values()),
            k=1
        )[0]

        # Prepara la información base del evento
        event_payload = {
            "attendee_id": self.attendee_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "location": self.location,
            "event_type": chosen_event
        }

        # Realiza la acción principal
        action_data = {}
        if chosen_event == "movimiento":
            new_location = random.choice(
                [loc for loc in LOCATIONS if loc != self.location or "Ingreso Principal"])
            self.location = new_location
            action_data = {"destino": new_location}

        elif chosen_event == "alerta_seguridad":
            self.heart_rate = random.randint(130, 160)  # Simula estrés
            action_data = {"descripcion": "Actividad sospechosa detectada."}

        current_state_data = self._update_vitals_and_observations()

        # Une los datos de la acción principal con los datos de estado
        event_payload["data"] = {**action_data, **current_state_data}

        return json.dumps(event_payload)


# --- Bucle Principal de la Simulación ---
if __name__ == "__main__":
    NUM_ATTENDEES = 1
    attendees = [Attendee() for _ in range(NUM_ATTENDEES)]

    print("\n--- Iniciando Simulación con Datos de Estado Completos ---\n")

    try:
        queue = sqs.get_queue_by_name(QueueName='BackStageOps-queue')
        # print(queue.url)

        while True:
            random_attendee = random.choice(attendees)
            json_event = random_attendee.simulate_action()
            # print(type(json_event))

            if json_event:
                print(json_event)

            response = queue.send_message(MessageBody=json_event)
            print(
                f"Mensaje enviado a SQS con ID: {response.get('MessageId')}\n")

            time.sleep(random.uniform(3.0, 6.0))

    except KeyboardInterrupt:
        print("\n--- Simulación detenida. ---")
