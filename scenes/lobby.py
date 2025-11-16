import customtkinter as ctk
from utils.network import send_json  # funzione per inviare JSON tramite socket

class Lobby(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.user_buttons = []

        self.title_label = ctk.CTkLabel(
            self, text="Lobby - Online Users", font=ctk.CTkFont(size=20, weight="bold")
        )
        self.title_label.pack(pady=10)
        
        self.username_label = ctk.CTkLabel(self, text="Logged in as: ")
        self.username_label.pack(pady=5)
        
        self.disconnect_button = ctk.CTkButton(
            self, text="Disconnect", fg_color="red", command=self.disconnect
        )
        self.disconnect_button.pack(pady=10)

        self.user_buttons_container = ctk.CTkFrame(self)
        self.user_buttons_container.pack(expand=True, fill="both", pady=10)

    def disconnect(self):
        """Disconnetti il client e torna alla home"""
        if self.master.connected:
            try:
                send_json(self.master.client_socket, {"type": "disconnect"})
            except:
                pass

            try:
                self.master.client_socket.close()
            except:
                pass

        self.master.connected = False
        self.master.username = ""
        self.master.user_list = []

        # reset lista bottoni
        for btn in self.user_buttons:
            btn.destroy()
        self.user_buttons.clear()

        # torna alla home
        self.pack_forget()
        self.master.home.pack(expand=True, fill="both")

    def update_user_list(self, users, my_name):
        """Aggiorna la lista di utenti online"""
        for btn in self.user_buttons:
            btn.destroy()
        self.user_buttons.clear()

        for u in users:
            if u == my_name:
                continue

            btn = ctk.CTkButton(
                self.user_buttons_container,
                text=u,
                command=lambda x=u: self.challenge_user(x)
            )
            btn.pack(pady=5, fill="x")
            self.user_buttons.append(btn)

    def challenge_user(self, username):
        """Invia una sfida ad un altro utente usando JSON"""
        try:
            send_json(self.master.client_socket, {
                "type": "challenge",
                "to": username
            })
        except Exception as e:
            print(f"[ERROR] Failed to send challenge: {e}")
