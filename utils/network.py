import json
import socket

def send_json(sock: socket.socket, data: dict):
    """
    Invia un dizionario come JSON tramite socket.
    Aggiunge un terminatore \n per separare i messaggi.
    """
    try:
        message = json.dumps(data) + "\n"
        sock.sendall(message.encode("utf-8"))
    except Exception as e:
        print(f"[ERROR] send_json failed: {e}")


def recv_json(sock: socket.socket, buffer: str = ""):
    """
    Riceve un messaggio JSON da un socket.
    Restituisce una tupla (dizionario, buffer residuo).
    """
    while True:
        if "\n" in buffer:
            message, buffer = buffer.split("\n", 1)
            try:
                return json.loads(message), buffer
            except json.JSONDecodeError:
                continue
        chunk = sock.recv(1024).decode("utf-8")
        if not chunk:
            return None, buffer  # connessione chiusa
        buffer += chunk
