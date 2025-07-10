from flask import Flask, jsonify, Response
import sqlite3
import random
from kubernetes import client, config
from kubernetes.client.rest import ApiException

app = Flask(__name__)
DB_PATH = "/data/db.sqlite"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS records (id INTEGER PRIMARY KEY, value INTEGER)")
    c.execute("INSERT INTO records (value) VALUES (?)", (random.randint(1, 1000),))
    conn.commit()
    conn.close()

def get_greeting_message():
    try:
        config.load_incluster_config()  # Pod içindeyse
    except config.ConfigException:
        try:
            config.load_kube_config()  # Lokal test için
        except:
            return "Hello (default greeting)!"

    api = client.CustomObjectsApi()
    group = "demo.io"
    version = "v1"
    namespace = "default"
    plural = "myappconfigs"
    name = "example-config"

    try:
        crd_obj = api.get_namespaced_custom_object(group, version, namespace, plural, name)
        return crd_obj['spec'].get('greetingMessage', "Hello (no greeting found)!")
    except ApiException:
        return "Hello (CRD not found)!"

@app.route('/')
def index():
    greeting = get_greeting_message()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT value FROM records ORDER BY id DESC LIMIT 1")
    row = c.fetchone()
    conn.close()
    return f"{greeting} Last DB value: {row[0] if row else 'No data'}"

@app.route('/metrics')
def metrics():
    value = random.randint(0,100)
    return Response(f"demo_app_random_metric {value}\n", mimetype="text/plain")

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
