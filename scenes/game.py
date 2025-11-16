import threading
import json
import random
import customtkinter as ctk
import tkinter as tk


def send_json(sock, obj):
    sock.sendall((json.dumps(obj) + "\n").encode())


class Game(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.opponent = None

        # -----------------------------------------------------
        #   UI
        # -----------------------------------------------------
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.place(relx=0.5, rely=0.3, anchor='center')

        ctk.CTkLabel(self.main_frame, text="OWN MAP", font=("Arial", 18, "bold")).grid(row=0, column=0)
        ctk.CTkLabel(self.main_frame, text="ENEMY MAP", font=("Arial", 18, "bold")).grid(row=0, column=1)

        self.player_frame = ctk.CTkFrame(self.main_frame)
        self.enemy_frame = ctk.CTkFrame(self.main_frame)

        self.player_frame.grid(row=1, column=0, padx=20, pady=20)
        self.enemy_frame.grid(row=1, column=1, padx=20, pady=20)

        # MAPPE
        self.player_map = [[' ']*9 for _ in range(9)]
        self.enemy_map  = [[' ']*9 for _ in range(9)]

        self.player_buttons = [[None]*9 for _ in range(9)]
        self.enemy_buttons  = [[None]*9 for _ in range(9)]

        self.ships_to_place = 4

        self.init_ship()
        self.init_player_map()
        self.init_enemy_map()

        # -----------------------------------------------------
        #   CHAT
        # -----------------------------------------------------
        self.chat = ctk.CTkFrame(self)
        self.chat.pack(side="bottom")

        self.chat_box = tk.Text(self.chat, height=10, width=70, bg="#1e1e1e",
                                fg="white", state="disabled")
        self.chat_box.pack(pady=5)

        self.input_box = tk.Text(self.chat, height=3, width=60,
                                 bg="#2b2b2b", fg="white")
        self.input_box.pack(side="left")

        ctk.CTkButton(self.chat, text="Invia", command=self.send_chat).pack(side="left", padx=5)

    # ======================================================
    # MAPPE
    # ======================================================
    def init_ship(self):
        while self.ships_to_place > 0:
            r = random.randint(0, 8)
            c = random.randint(0, 8)
            if self.player_map[r][c] == ' ':
                self.player_map[r][c] = 'x'
                self.ships_to_place -= 1

    def init_player_map(self):
        for r in range(9):
            for c in range(9):
                cell = self.player_map[r][c]
                color = "#2e2e2e" if cell == " " else "#2b6a3f"

                btn = ctk.CTkButton(self.player_frame, text=cell, fg_color=color, width=40, height=30)
                btn.grid(row=r, column=c, padx=3, pady=3)
                self.player_buttons[r][c] = btn

    def init_enemy_map(self):
        for r in range(9):
            for c in range(9):
                btn = ctk.CTkButton(self.enemy_frame, text=" ", fg_color="#1f538d",
                                    width=40, height=30,
                                    command=lambda rr=r, cc=c: self.attack(rr, cc))
                btn.grid(row=r, column=c, padx=3, pady=3)
                self.enemy_buttons[r][c] = btn

    # ======================================================
    # CHAT
    # ======================================================
    def send_chat(self):
        msg = self.input_box.get("1.0", tk.END).strip()
        if not msg:
            return

        send_json(self.master.client_socket, {
            "type": "chat",
            "from": self.master.username,
            "to": self.opponent,
            "msg": msg
        })

        self.add_chat(f"Tu: {msg}")
        self.input_box.delete("1.0", tk.END)

    def add_chat(self, text):
        self.chat_box.configure(state="normal")
        self.chat_box.insert(tk.END, text + "\n")
        self.chat_box.configure(state="disabled")
        self.chat_box.see(tk.END)

    # ======================================================
    # GAME
    # ======================================================
    def attack(self, r, c):
        send_json(self.master.client_socket, {
            "type": "attack",
            "from": self.master.username,
            "to": self.opponent,
            "r": r,
            "c": c
        })

        self.enemy_buttons[r][c].configure(state="disabled")

    # ======================================================
    # RECEIVER JSON
    # ======================================================
    def start_game(self, opponent):
        self.opponent = opponent
        threading.Thread(target=self.receive, daemon=True).start()

    def receive(self):
        buffer = ""

        while True:
            try:
                chunk = self.master.client_socket.recv(1024).decode()
                if not chunk:
                    break

                buffer += chunk

                while "\n" in buffer:
                    raw, buffer = buffer.split("\n", 1)
                    raw = raw.strip()
                    if not raw:
                        continue

                    msg = json.loads(raw)
                    self.process(msg)

            except:
                break

    # ======================================================
    # LOGICA MESSAGGI JSON
    # ======================================================
    def process(self, msg):
        t = msg["type"]

        if t == "chat":
            self.add_chat(f"{msg['from']}: {msg['msg']}")
            return

        if t == "attack":
            r, c = msg["r"], msg["c"]
            hit = self.player_map[r][c] == "x"

            send_json(self.master.client_socket, {
                "type": "result",
                "from": self.master.username,
                "to": msg["from"],
                "r": r,
                "c": c,
                "result": "hit" if hit else "miss"
            })
            return

        if t == "result":
            r, c = msg["r"], msg["c"]
            res = msg["result"]

            if res == "hit":
                self.enemy_buttons[r][c].configure(fg_color="red", text="💥")
            else:
                self.enemy_buttons[r][c].configure(fg_color="#7ed2ff", text="•")
            return
