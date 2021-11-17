import sqlite3

# Percorso relativo della base di dati
DATABASE_PATH = "./data.db"

# Viene stabilita la connessione con il database + creazione del cursor
dbconn = sqlite3.connect(DATABASE_PATH)
cursor = dbconn.cursor()

# Creazione della tabella che conterrà i nomi e le stringhe delle azioni
cursor.execute("""
    CREATE TABLE IF NOT EXISTS movements (
        action TEXT PRIMARY KEY NOT NULL,
        sequence TEXT NOT NULL
    );
""")
dbconn.commit()

# Inserimento dei dati nel database
cursor.execute("""
    INSERT OR IGNORE INTO movements
    VALUES ('zigzag',   'l:150:s:250:f:1000:s:250:r:300:s:250:f:1000:s:250:l:300:s:250:f:1000:s:250:r:300:s:250:f:1000:s:250:l:300:s:250:f:1000:s:250:r:300:s:250:f:1000:s:100'),
           ('circle',   'l:1500:s:100'),
           ('infinity', 'l:1500:r:1500:s:100'),
           ('triangle', 'f:1000:s:250:l:450:s:250:f:1000:s:250:l:450:s:250:f:1000:s:100'),
           ('square',   'f:1000:s:250:l:350:s:250:f:1000:s:250:l:350:s:250:f:1000:s:250:l:350:s:250:f:1000:s:100')
""")
dbconn.commit()

# Testo di selezione di tutti i dati dal db
print("CONNECTION TEST")
print(dbconn.execute("SELECT * FROM movements;").fetchall())
print("OK")

# Chiusura della connessione tra il programma ed il db
dbconn.close()
