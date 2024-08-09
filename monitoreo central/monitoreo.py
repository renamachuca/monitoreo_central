from flask import Flask, request, jsonify, render_template
import psycopg2
from psycopg2 import OperationalError

app = Flask(__name__)

# Lista de tokens válidos
VALID_TOKENS = {
    "service1": "token_service1",
    "service2": "token_service2",
    # Añade más servicios según sea necesario
}

def check_auth():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        token = auth_header.split(" ")[1]  # Se espera que el token esté en el formato 'Bearer <token>'
        if token in VALID_TOKENS.values():
            return True
    return False

def fetch_logs():
    connection = psycopg2.connect(
        host="localhost",
        database="logdb",
        user="loggs",
        password="penguin"
    )
    cursor = connection.cursor()
    cursor.execute("SELECT timestamp, service_name, severity, message FROM loggs ORDER BY timestamp DESC")
    logs = cursor.fetchall()
    cursor.close()
    connection.close()
    return logs

@app.route('/', methods=['GET'])
def index():
    logs = fetch_logs()
    return render_template('index.html', logs=logs)

@app.route('/logs1', methods=['POST'])
def receive_logs1():
    return receive_logs()

@app.route('/logs2', methods=['POST'])
def receive_logs2():
    return receive_logs()

def receive_logs():
    if not check_auth():
        return jsonify({"error": "No autorizado"}), 401

    log_data = request.get_json()
    print(f"Log recibido: {log_data}")  # Para depuración

    connection = None
    cursor = None
    try:
        connection = psycopg2.connect(
            host="localhost",
            database="logdb",
            user="loggs",
            password="penguin"
        )
        cursor = connection.cursor()
        insert_query = """
        INSERT INTO loggs (timestamp, service_name, severity, message)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_query, (log_data['timestamp'], log_data['service_name'], log_data['severity'], log_data['message']))
        connection.commit()

    except (Exception, OperationalError) as error:
        print(f"Error al insertar el log en la base de datos: {error}")
        return jsonify({"error": str(error)}), 500

    finally:
        if cursor:
            cursor.close()  
        if connection:
            connection.close()

    return jsonify({"message": "Log recibido"}), 200

if __name__ == '__main__':
    # Crea dos hilos para ejecutar dos instancias de Flask en diferentes puertos
    from threading import Thread

    def run_app1():
        app.run(port=5000)

    def run_app2():
        app.run(port=5001)

    Thread(target=run_app1).start()
    Thread(target=run_app2).start()
