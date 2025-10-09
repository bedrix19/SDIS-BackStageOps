import json
import random
import uuid
import time
from datetime import datetime

import boto3
sqs = boto3.resource('sqs')

# --- Lista de ubicaciones ---
LOCATIONS = [
    "Puerta Principal",
    "Escenario Principal", "Escenario 2", "Escenario 3",
    "Zona de Comida 1", "Zona de Comida 2",
    "Bar 1", "Bar 2", "Bar 3",
    "Baños 1", "Baños 2", "Baños 3",
    "Punto de Primeros Auxilios"
]

# --- Tipos de eventos ---
EVENT_TYPES = {
    "MOVEMENT": 0.8,       # Probabilidad de que el attendee se mueva
    "SUSPICIOUS ACTIVITY": 0.1,  # Probabilidad de generar una alerta
    "FIRE": 0.1  # Probabilidad de generar una alerta
}


class User:
    """
    Representa a un usuario general del festival. En cada acción, reporta un
    estado completo que incluye signos vitales.
    """

    def __init__(self):
        self.user_id = str(uuid.uuid4())
        self.role = "attendee"
        self.location = "Puerta Principal"
        self.heart_rate = random.randint(70, 90)
        print(f"Asistente {self.user_id} creado en {self.location}")

    def _update_vitals_and_observations(self):
        """
        Calcula el estado actual del asistente y su entorno.
        """
        # 1. Actualizar Ritmo Cardíaco
        if "Escenario" in self.location:
            self.heart_rate = random.randint(110, 140)
        elif "Zona de Comida" in self.location or "Punto de Primeros Auxilios" in self.location:
            self.heart_rate = random.randint(65, 85)
        else:  # Bares, baños
            self.heart_rate = random.randint(80, 110)
        self.heart_rate += random.randint(-3, 3)

        return {
            "heart_rate_bpm": self.heart_rate
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
            "user_id": self.user_id,
            "role": self.role,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "location": self.location,
            "event_type": chosen_event
        }

        # Realiza la acción principal
        action_data = {}
        if chosen_event == "MOVEMENT":
            new_location = random.choice(
                [loc for loc in LOCATIONS if loc != self.location or "Puerta Principal"])
            self.location = new_location
            action_data = {"destino": new_location}

        elif chosen_event == "SUSPICIOUS ACTIVITY":
            self.heart_rate = random.randint(130, 160)
            action_data = {
                "descripcion": "Actividad sospechosa detectada en {self.location}"}

        elif chosen_event == "FIRE":
            self.heart_rate = random.randint(130, 160)
            action_data = {
                "descripcion": "Fuego detectado en {self.location}."}

        current_state_data = self._update_vitals_and_observations()

        # Une los datos de la acción principal con los datos de estado
        event_payload["data"] = {**action_data, **current_state_data}

        return json.dumps(event_payload)


# --- Bucle Principal de la Simulación ---
if __name__ == "__main__":
    NUM_USERS = 1
    users = [User() for _ in range(NUM_USERS)]

    print("\n--- Iniciando Simulación con Datos de Estado Completos ---\n")

    try:
        queue = sqs.get_queue_by_name(QueueName='BackStageOps-queue')

        while True:
            random_attendee = random.choice(users)
            json_event = random_attendee.simulate_action()

            if json_event:
                print(json_event)

            response = queue.send_message(MessageBody=json_event)
            print(
                f"Mensaje enviado a SQS con ID: {response.get('MessageId')}\n")

            time.sleep(random.uniform(3.0, 6.0))

    except KeyboardInterrupt:
        print("\n--- Simulación detenida. ---")
