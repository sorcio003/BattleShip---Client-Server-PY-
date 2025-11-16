from battleship import Battleship

HOST = "192.168.1.54"
PORT = 50001

if __name__ == "__main__":
    app = Battleship(HOST, PORT)
    app.mainloop()
