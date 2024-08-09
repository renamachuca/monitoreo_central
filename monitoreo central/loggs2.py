import json
import requests
import time

url = "http://localhost:5001/logs2"
auth_token = "token_service2"

logs = [
    {
        "timestamp": "2024-08-09T12:00:00Z",
        "service_name": "service2",
        "severity": "INFO",
        "message": "Log message from service 2"
    },
]

for log_entry in logs:
    try:
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = requests.post(url, json=log_entry, headers=headers)
        response.raise_for_status()
        print(f"Log enviado: {log_entry}")
    except requests.exceptions.RequestException as e:
        print(f"Error al enviar el log: {e}")
    time.sleep(1)
