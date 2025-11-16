# Battleship Socket Game

Battleship Socket Game è un gioco di battaglia navale multiplayer sviluppato in Python. 
Utilizza socket TCP per la comunicazione tra client e server e offre un'interfaccia grafica moderna con **CustomTkinter**.

## Caratteristiche

- Multiplayer in tempo reale tramite rete locale o Internet.
- Interfaccia grafica con CustomTkinter.
- Lobby per vedere gli utenti online e sfidare amici.
- Comunicazione tramite JSON per una gestione strutturata dei messaggi.
- Notifiche di sfida e gestione partite.

## Requisiti

- Python 3.10 o superiore
- Librerie Python:
  - `customtkinter`
  - `tkinter` (incluso con Python)
- (Opzionale) Eventuali altre librerie indicate nel progetto

## Installazione

1. Clona il repository:

```bash
git clone https://github.com/tuo-username/battleship-socket.git
cd battleship-socket
```

2. Installa le dipendenze:

```bash
pip install -r requirements.txt
```

3. Avvia il server:

```bash
python server.py
```

4. Avvia i client:

```bash
python clients.py
```

## Struttura del progetto

```
app/
├── battleship.py       # Main client GUI
├── clients.py          # Avvio del client
├── server.py           # Server per gestire la lobby e le partite
├── scenes/             # Cartella con le scene Tkinter (Home, Lobby, Game)
└── utils/              # Funzioni di utilità, es. invio/ricezione JSON
```

## Utilizzo

1. Avvia il server.
2. Avvia uno o più client.
3. Inserisci l'username e connettiti.
4. Accedi alla lobby per vedere altri utenti online.
5. Sfida un giocatore e inizia la partita.

## Comunicazione

I messaggi tra client e server sono gestiti in **JSON**, ad esempio:

```json
{
  "action": "challenge",
  "from": "Player1",
  "to": "Player2"
}
```

## Licenza

MIT License

---

Creato con ❤️ in Python
