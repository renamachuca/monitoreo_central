import json
import requests
import time

url = "http://localhost:5000/logs1"
auth_token = "token_service1"

logs = [
    {"timestamp": "2024-08-08T13:02:43.309155Z", "service_name": "example_service", "severity": "DEBUG", "message": "Iniciando verificación de credenciales para el usuario 'usuario123'"},
    {"timestamp": "2024-08-08T13:02:43.309252Z", "service_name": "example_service", "severity": "INFO", "message": "Transacción completada exitosamente para el usuario 'usuario456'"},
    {"timestamp": "2024-08-08T13:02:43.309334Z", "service_name": "example_service", "severity": "WARNING", "message": "Demora en la respuesta del servicio 'user_profile_service', tiempo de respuesta 1500 ms"},
    {"timestamp": "2024-08-08T13:02:43.309389Z", "service_name": "example_service", "severity": "ERROR", "message": "Error al intentar conectar a la base de datos: tiempo de espera agotado"},
    {"timestamp": "2024-08-08T13:02:43.309430Z", "service_name": "example_service", "severity": "CRITICAL", "message": "Fallo crítico en el servidor web: caída del servidor debido a falta de memoria"}
]
for log_entry in logs:
    try:
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = requests.post(url, json=log_entry, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error al enviar el log: {e}")
    time.sleep(1)
