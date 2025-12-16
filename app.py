# Programmet skapar en SQLite-databas för användare, lägger in testdata om databasen 
# är tom och kan visa, radera eller anonymisera användardata enligt GDPR


import sqlite3  # Används för att arbeta med SQLite-databas
import os       # Används för filer, mappar och miljövariabler


# -----------------------------
# Databasväg
# -----------------------------

# Hämtar databasens sökväg från miljövariabel
# Om den inte finns används standardvägen ./data/sample_users.db
db_file = os.getenv("USER_DB_PATH", "./data/sample_users.db")

# Hämtar mappens namn från sökvägen
folder_path = os.path.dirname(db_file)

# Skapar mappen om den inte redan finns
if not os.path.exists(folder_path):
    os.makedirs(folder_path)


# -----------------------------
# Funktioner
# -----------------------------

def setup_db():
    """Skapar databasen och tabellen om de inte finns"""

    # Ansluter till databasen (skapas om den inte finns)
    connection = sqlite3.connect(db_file)

    # Cursor används för att köra SQL-kommandon
    cur = connection.cursor()

    # Skapar tabellen persons om den inte redan finns
    cur.execute("""
        CREATE TABLE IF NOT EXISTS persons (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Unikt ID
            full_name TEXT NOT NULL,                     -- Användarens namn
            mail TEXT NOT NULL                           -- Användarens e-post
        )
    """)

    # Räknar hur många rader som finns i tabellen
    cur.execute("SELECT COUNT(*) FROM persons")
    existing_records = cur.fetchone()[0]

    # Om tabellen är tom läggs testanvändare till
    if existing_records == 0:
        seed_data = [
            ("Karin Karlsson", "karin@example.com"),
            ("David Dahl", "david@example.com"),
            ("Erik Erikson", "Erik@example.com")
        ]

        # Lägger in flera användare samtidigt
        cur.executemany(
            "INSERT INTO persons (full_name, mail) VALUES (?, ?)",
            seed_data
        )
        print("Databas skapad och testanvändare tillagda.")
    else:
        print(f"Databasen innehåller redan {existing_records} användare.")

    # Sparar ändringar
    connection.commit()

    # Stänger databasen
    connection.close()


def list_all_users():
    """Visar alla användare i databasen"""

    # Ansluter till databasen
    connection = sqlite3.connect(db_file)
    cur = connection.cursor()

    # Hämtar alla användare
    cur.execute("SELECT * FROM persons")
    rows = cur.fetchall()

    # Skriver ut användarna
    print("\nAnvändare i databasen:")
    for user_id, name, mail in rows:
        print(f"ID: {user_id}, Namn: {name}, E-post: {mail}")

    # Stänger databasen
    connection.close()


def wipe_data():
    """Tar bort all användardata (GDPR)"""

    # Ansluter till databasen
    connection = sqlite3.connect(db_file)
    cur = connection.cursor()

    # Tar bort alla rader i tabellen
    cur.execute("DELETE FROM persons")

    # Sparar ändringar
    connection.commit()

    # Stänger databasen
    connection.close()

    print("All användardata är borttagen (GDPR).")


def mask_user_info():
    """Anonymiserar användarnas namn (GDPR)"""

    # Ansluter till databasen
    connection = sqlite3.connect(db_file)
    cur = connection.cursor()

    # Uppdaterar alla namn till ett anonymt värde
    cur.execute("""
        UPDATE persons
        SET full_name = 'Anonymiserad Användare'
    """)

    # Sparar ändringar
    connection.commit()

    # Stänger databasen
    connection.close()

    print("Alla användarnamn är anonymiserade.")
    


# -----------------------------
# TEST
# -----------------------------

def test_generate_test_data():
    """Testar att testdata genereras i databasen"""

    # Använd en separat testdatabas
    global db_file
    original_db = db_file
    test_db = "test_generate_data.db"
    db_file = test_db

    # Säkerställ att testdatabasen inte finns sedan tidigare
    if os.path.exists(test_db):
        os.remove(test_db)

    # Kör funktionen som skapar testdata
    setup_db()

    # Kontrollera att data finns
    connection = sqlite3.connect(test_db)
    cur = connection.cursor()
    cur.execute("SELECT COUNT(*) FROM persons")
    count = cur.fetchone()[0]
    connection.close()

    # Skriv ut testresultat
    print(f"[TEST] Antal genererade testanvändare: {count}")

    assert count > 0  # Testdata har genererats

    # Återställ databas
    db_file = original_db

    # Städa upp
    if os.path.exists(test_db):
        os.remove(test_db)

    print("[TEST] test_generate_test_data lyckades")


# -----------------------------
# Huvudprogram
# -----------------------------

# Körs bara om filen startas direkt
if __name__ == "__main__":

    # Skapar databasen och tabellen
    setup_db()

    # Visar alla användare
    list_all_users()
    
    # KÖR TESTET
    test_generate_test_data()

    print("\nProgrammet körs. Tryck Ctrl+C för att avsluta.")

    try:
        # Oändlig loop för att hålla programmet igång
        while True:
            pass
    except KeyboardInterrupt:
        # Körs när användaren trycker Ctrl+C
        print("\nProgrammet avslutas...")