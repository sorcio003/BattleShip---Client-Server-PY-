import customtkinter as ctk


class Home(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.username_entry = ctk.CTkEntry(
            self,
            placeholder_text="Username",
            width=220
        )
        self.username_entry.pack(pady=15)

        self.connect_button = ctk.CTkButton(
            self,
            text="Connect",
            width=150
        )
        self.connect_button.pack(pady=10)

        self.dashboard_button = ctk.CTkButton(
            self,
            text="Open Lobby",
            width=150,
            state="disabled"        # disabilitato finché non si connette
        )
        self.dashboard_button.pack(pady=10)

        self.status_label = ctk.CTkLabel(
            self,
            text="Enter username and connect."
        )
        self.status_label.pack(pady=5)


    # ============================================================
    # GET USERNAME
    # ============================================================
    def get_username(self):
        return self.username_entry.get().strip()


    # ============================================================
    # STATUS MESSAGE
    # ============================================================
    def set_status(self, text, color):
        self.status_label.configure(text=text, text_color=color)

        # Se connesso → abilita accesso alla lobby
        if "Connected" in text:
            self.dashboard_button.configure(state="normal")
        else:
            self.dashboard_button.configure(state="disabled")
