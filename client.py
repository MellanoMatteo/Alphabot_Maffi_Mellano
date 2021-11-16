import socket

# Costanti per il protocollo di comunicazione dei 2 socket
MESSAGES_SEPARATOR = ":" # Separatore delle stringhe utilizzate dai socket
SERVER_PORT = 2118
BUFFER_SIZE = 2 ** 16

# Comandi speciali
EXIT_CMD = "$exit" # Comando per chiudere in client ed il socket in modo sicuro
CMDS_LIST_CMD = "$cmds" # Comando per listare tutte le azioni disponibili nel database

def main():
    # Creazione del client socket + connect
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((input("\nEnter server IP address: "), SERVER_PORT))

    # Loop di input dei comandi
    while True:
        # Inserimento del comando da eseguire
        cmd = input("\nCommand: ")

        # Invio del comando al server (all'AlphaBot)
        client.sendall(cmd.encode())

        # Controllo comandi speciali
        if cmd == EXIT_CMD:
            break
        elif cmd == CMDS_LIST_CMD:
            # Ricezione della lista delle azioni nel database
            data = client.recv(BUFFER_SIZE).decode().split(MESSAGES_SEPARATOR)[:-1]

            # Stampa delle azioni
            print("\nAll possible actions:")
            for d in data:
                print(f"-{d}")

    # Terminazione del client socket
    client.close()

if __name__ == "__main__":
    main()