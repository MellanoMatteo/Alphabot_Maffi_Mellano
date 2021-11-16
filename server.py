import socket
import sqlite3
import time
import AlphaBot

# Inizializzazione oggetto che gestisce l'AlphaBot
alphabot = AlphaBot.AlphaBot()
alphabot.stop() # Comando di stop per impedire all'AlphaBot di partire una volta avviato lo script

# Costanti per il protocollo di comunicazione dei 2 socket
MESSAGES_SEPARATOR = ":" # Separatore delle stringhe utilizzate dai socket
SERVER_ADDRESS = "0.0.0.0" # Indirizzo IP della macchina su cui gira il processo del server
SERVER_PORT = 2118
BUFFER_SIZE = 2 ** 16

# DIrezioni possibili che l'AlphaBot può compiere
DIRECTIONS = {
    "F": alphabot.forward,
    "B": alphabot.backward,
    "L": alphabot.left,
    "R": alphabot.right,
    "S": alphabot.stop
}

# Comandi speciali
EXIT_CMD = "$exit" # Comando per chiudere in client ed il socket in modo sicuro
CMDS_LIST_CMD = "$cmds" # Comando per listare tutte le azioni disponibili nel database

# Percorso relativo della base di dati
DATABASE_PATH = "./data.db"

# Funzione che preleva la stringa corretta dal db, corrispondente all'azione inviato dal client, ed esegue la stringa
# facendo muovere l'AlphaBot secondo un percorso gestito dalla stringa stessa.
def executeCommand(statement, cursor):
    try:
        # Query di selezione della stringa
        # Dato che il risultato è una lista di tuple (anche se vi è un unico risultato con all'interno un unico dato)
        # bisogna prelevare la prima (ed unica) tupla della lista ed anche estrarre il primo (ed unico) elemento della tupla
        data = list(cursor.execute(f"SELECT sequence FROM movements WHERE action='{statement}';"))[0][0].split(MESSAGES_SEPARATOR)
        
        # Esecuzione della stringa per far muovere l'AlphaBot
        # Ogni elemento con indice pari della lista è una direzione (F, B, L, R, S) ed ogni elemento
        # in posizione dispari è il tempo in millisecondi da attendere
        for i in range(0, len(data), 2):
            DIRECTIONS[data[i].upper()]()
            time.sleep(int(data[i + 1]) / 1000)
    except:
        # Errore -> azione non trovata nel db
        print(f"Invalid action <{statement}>!")

def main():
    # Creazione del server socket + bind
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_ADDRESS, SERVER_PORT))

    # Listen + accept
    server.listen()
    connection, _ = server.accept()

    # Viene stabilita la connessione con il database + creazione del cursor
    DBconn = sqlite3.connect(DATABASE_PATH)
    cursor = DBconn.cursor()

    # Loop di esecuzione dei comandi
    while True:
        # Ricezione del comando dal client
        cmd = connection.recv(BUFFER_SIZE).decode()

        # Controllo comandi speciali
        if cmd == EXIT_CMD:
            break
        elif cmd == CMDS_LIST_CMD:
            # Query per estrarre tutte le azioni possibili dal db
            data = list(cursor.execute("SELECT action FROM movements;"))
            
            # Creazione lista di tutte le azioni -> zigzag:circle:square:...
            lst = ""
            for d in data:
                lst += f"{d[0]}{MESSAGES_SEPARATOR}"

            # Invio della lista al client
            connection.sendall(lst.encode())
        else:
            # Comando non speciale
            executeCommand(cmd, cursor)

    # Chiusura connessione con il database
    DBconn.close()
    # Terminazione del server socket
    server.close()

if __name__ == "__main__":
    main()