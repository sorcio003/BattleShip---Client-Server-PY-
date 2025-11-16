import socket
import threading
import json

HOST = ""
PORT = 50001

clients = {}        # username -> socket
username_list = []  # elenco utenti


# ============================================================
# UTILS JSON
# ============================================================
def send_json(sock, obj):
    """Invia JSON come singola riga."""
    try:
        message = json.dumps(obj) + "\n"
        sock.sendall(message.encode())
    except:
        pass


# ============================================================
# INVIO LISTA UTENTI
# ============================================================
def broadcast_user_list():
    data = {
        "type": "userlist",
        "users": username_list
    }

    for user, sock in clients.items():
        send_json(sock, data)


# ============================================================
# PROCESSORE MESSAGGI
# ============================================================
def process_message(username, sock, msg):
    msg_type = msg.get("type")

    # --------------------------------------------------------
    # CHALLENGE
    # --------------------------------------------------------
    if msg_type == "challenge":
        target = msg["to"]

        if target in clients:
            send_json(clients[target], {
                "type": "challenge",
                "from": username
            })
        else:
            send_json(sock, {
                "type": "error",
                "message": f"User {target} not found"
            })
        return

    # --------------------------------------------------------
    # CHALLENGE ACCEPTED
    # --------------------------------------------------------
    if msg_type == "challenge_accept":
        target = msg["to"]

        if target in clients:
            send_json(clients[target], {
                "type": "challenge_accept",
                "from": username
            })
        else:
            send_json(sock, {
                "type": "error",
                "message": f"User {target} not found"
            })
        return

    # --------------------------------------------------------
    # ATTACK
    # --------------------------------------------------------
    if msg_type == "attack":
        target = msg["to"]
        if target in clients:
            send_json(clients[target], msg)
        return

    # --------------------------------------------------------
    # RESULT
    # --------------------------------------------------------
    if msg_type == "result":
        target = msg["to"]
        if target in clients:
            send_json(clients[target], msg)
        return

    # --------------------------------------------------------
    # CHAT
    # --------------------------------------------------------
    if msg_type == "chat":
        target = msg["to"]
        if target in clients:
            send_json(clients[target], msg)
        return

    print("[SERVER] Messaggio sconosciuto:", msg)


# ============================================================
# GESTIONE CLIENT
# ============================================================
def handle_client(sock, addr):
    username = None

    try:
        # LOGIN JSON
        first = sock.recv(1024).decode()
        first = first.strip()
        login_msg = json.loads(first)

        username = login_msg["username"]

        if username in clients:
            send_json(sock, {"type": "error", "message": "Username exists"})
            sock.close()
            return

        username_list.append(username)
        clients[username] = sock

        # BENVENUTO
        send_json(sock, {"type": "welcome", "username": username})
        broadcast_user_list()

        buffer = ""

        while True:
            chunk = sock.recv(1024).decode()
            if not chunk:
                break

            buffer += chunk

            # Leggi tutti i messaggi completi
            while "\n" in buffer:
                raw, buffer = buffer.split("\n", 1)
                raw = raw.strip()
                if not raw:
                    continue

                try:
                    obj = json.loads(raw)
                    process_message(username, sock, obj)
                except Exception as e:
                    print("[ERRORE JSON]", e)

    except Exception as e:
        print("[SERVER] errore con", username, e)

    finally:
        print("[-]", username, "disconnesso")

        if username in username_list:
            username_list.remove(username)
        if username in clients:
            del clients[username]

        broadcast_user_list()

        try:
            sock.close()
        except:
            pass


# ============================================================
# START SERVER
# ============================================================
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print("[SERVER] In ascolto su", HOST, PORT)

    while True:
        sock, addr = server.accept()
        threading.Thread(target=handle_client, args=(sock, addr), daemon=True).start()


if __name__ == "__main__":
    start_server()
