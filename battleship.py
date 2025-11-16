import socket
import threading
import json
from tkinter import messagebox
import customtkinter as ctk

from scenes.home import Home
from scenes.lobby import Lobby
from scenes.game import Game


def send_json(sock, obj):
    sock.sendall((json.dumps(obj) + "\n").encode())


class Battleship(ctk.CTk):
    def __init__(self, HOST, PORT):
        super().__init__()

        self.title("Battleship")
        self.geometry("400x250")

        self.SERVER_IP = HOST
        self.SERVER_PORT = PORT
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.client_socket = None
        self.connected = False
        self.username = ""
        self.user_list = []

        # SCENE MANAGER
        self.home = Home(self)
        self.lobby = Lobby(self)
        self.game = Game(self)

        self.home.pack(expand=True, fill="both")
        self.lobby.pack_forget()

        # COLLEGAMENTO BOTTONI
        self.home.connect_button.configure(command=self.connect_to_server)
        self.home.dashboard_button.configure(command=self.join_lobby)


    # ============================================================
    # CONNESSIONE
    # ============================================================
    def connect_to_server(self):
        self.username = self.home.get_username()
        if not self.username:
            messagebox.showwarning("Warning", "Insert username!")
            return

        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.SERVER_IP, self.SERVER_PORT))

            # LOGIN JSON
            send_json(self.client_socket, {
                "type": "login",
                "username": self.username
            })

            # Risposta login
            raw = self.client_socket.recv(1024).decode().strip()
            res = json.loads(raw)

            if res["type"] == "error":
                self.home.set_status(res["message"], "red")
                return

            if res["type"] == "welcome":
                self.home.set_status(f"Connected as {self.username}", "green")
                messagebox.showinfo("Connected", "Waiting for lobby...")
                self.connected = True

        except Exception as e:
            self.home.set_status(str(e), "red")


    # ============================================================
    # LISTENER SOCKET
    # ============================================================
    def listen_server(self):
        buffer = ""

        while self.connected:
            try:
                chunk = self.client_socket.recv(1024).decode()
                if not chunk:
                    break

                buffer += chunk

                while "\n" in buffer:
                    raw, buffer = buffer.split("\n", 1)
                    raw = raw.strip()
                    if not raw:
                        continue

                    msg = json.loads(raw)
                    self.process_message(msg)

            except Exception as e:
                print("[CLIENT ERROR]", e)
                break

        print("[CLIENT] Disconnected from server")
        self.connected = False


    # ============================================================
    # PROCESSORE MESSAGGI JSON
    # ============================================================
    def process_message(self, msg):
        t = msg["type"]

        # ---------------------------------------
        # LISTA UTENTI
        # ---------------------------------------
        if t == "userlist":
            self.user_list = msg["users"]
            self.lobby.update_user_list(self.user_list, self.username)
            return

        # ---------------------------------------
        # CHALLENGE
        # ---------------------------------------
        if t == "challenge":
            challenger = msg["from"]

            response = messagebox.askyesno(
                "Challenge",
                f"{challenger} has challenged you to a game. Accept?"
            )

            if response:
                send_json(self.client_socket, {
                    "type": "challenge_accept",
                    "from": self.username,
                    "to": challenger
                })
                self.start_game_with(challenger)

            return

        # ---------------------------------------
        # CHALLENGE ACCEPTED
        # ---------------------------------------
        if t == "challenge_accept":
            accepter = msg["from"]
            messagebox.showinfo("Challenge Accepted",
                                f"{accepter} has accepted your challenge.")
            self.start_game_with(accepter)
            return

        # ---------------------------------------
        # MESSAGGI DI GIOCO
        # ---------------------------------------
        # li gestisce Game.py
        self.game.process(msg)


    # ============================================================
    # LOBBY
    # ============================================================
    def join_lobby(self):
        if not self.connected:
            messagebox.showwarning("Warning", "Not connected to server")
            return

        self.home.pack_forget()
        self.lobby.pack(expand=True, fill="both")
        self.lobby.username_label.configure(text=f"Logged in as: {self.username}")

        threading.Thread(target=self.listen_server, daemon=True).start()


    # ============================================================
    # GAME
    # ============================================================
    def start_game_with(self, opponent):
        print(f"[GAME] Starting game with {opponent}")
        self.lobby.pack_forget()
        self.game.pack(expand=True, fill="both")
        self.geometry("1000x700")

        self.game.start_game(opponent)


    # ============================================================
    # CHIUSURA
    # ============================================================
    def on_close(self):
        try:
            if self.connected:
                send_json(self.client_socket, {"type": "disconnect"})
        except:
            pass

        try:
            self.client_socket.close()
        except:
            pass

        self.destroy()
