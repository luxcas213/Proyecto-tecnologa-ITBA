import csv
import os
from typing import Optional, Dict, List

DB_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'db')
CSV_PATH = os.path.join(DB_DIR, 'users.csv')
HISTORIAL_PATH = os.path.join(DB_DIR, 'historial_global.csv')

HISTORIAL_FIELDS = ['UserID', 'Ciudad', 'FechaHora', 'Temperatura_C', 'Condicion_Clima', 'Humedad_Porcentaje', 'Viento_kmh']


def get_userid_by_name(name: str) -> Optional[str]:
    for user in read_users():
        if user['name'] == name:
            return user['userid']
    return None


def guardar_historial(username: str, ciudad: str, fecha_hora: str, temperatura: str, condicion: str, humedad: str, viento: str) -> None:
    userid = get_userid_by_name(username) or username
    archivo_existe = os.path.isfile(HISTORIAL_PATH)
    with open(HISTORIAL_PATH, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=HISTORIAL_FIELDS)
        if not archivo_existe:
            writer.writeheader()
        writer.writerow({
            'UserID': userid,
            'Ciudad': ciudad,
            'FechaHora': fecha_hora,
            'Temperatura_C': temperatura,
            'Condicion_Clima': condicion,
            'Humedad_Porcentaje': humedad,
            'Viento_kmh': viento,
        })


def leer_historial() -> List[Dict[str, str]]:
    if not os.path.isfile(HISTORIAL_PATH):
        return []
    with open(HISTORIAL_PATH, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def read_users() -> List[Dict[str, str]]:
    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def add_user(userid: str, name: str, password: str) -> None:
    users = read_users()
    if any(u['name'] == name for u in users):
        raise ValueError('user already exists')
    with open(CSV_PATH, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['userid', 'name', 'password'])
        writer.writerow({'userid': userid, 'name': name, 'password': password})


def authenticate(name: str, password: str) -> Optional[Dict[str, str]]:
    for user in read_users():
        if user['name'] == name and user['password'] == password:
            return {
                'userid': user['userid'],
                'name': user['name'],
                'password': user['password'],
            }
    return None
