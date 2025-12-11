import sqlite3
import os

# -----------------------------
# Databasväg
# -----------------------------
# Använd mappen "data" i projektmappen
db_file = os.getenv("USER_DB_PATH", "./data/sample_users.db")

# Skapa mappen om den inte finns
if not os.path.exists(os.path.dirname(db_file)):
    os.makedirs(os.path.dirname(db_file))


# -----------------------------
# Funktioner
# -----------------------------
def setup_db():
    """Create database and user table if not already present."""
    connection = sqlite3.connect(db_file)
    cur = connection.cursor()

    # Create table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS persons (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            mail TEXT NOT NULL
        )
    """)

    # Check if table has data
    cur.execute("SELECT COUNT(*) FROM persons")
    existing_records = cur.fetchone()[0]

    if existing_records == 0:
        # Insert demo users
        seed_data = [
            ("Karin Karlsson", "karin@example.com"),
            ("David Dahl", "david@example.com")
        ]
        cur.executemany(
            "INSERT INTO persons (full_name, mail) VALUES (?, ?)", seed_data
        )
        print("Database created and demo users added.")
    else:
        print(f"Database already contains {existing_records} users.")

    connection.commit()
    connection.close()


def list_all_users():
    """Print all users from database."""
    connection = sqlite3.connect(db_file)
    cur = connection.cursor()

    cur.execute("SELECT * FROM persons")
    rows = cur.fetchall()

    print("\nUsers currently stored:")
    for uid, name, mail in rows:
        print(f"ID: {uid}, Name: {name}, Email: {mail}")

    connection.close()


def wipe_data():
    """Remove all data (GDPR – delete personal data)."""
    connection = sqlite3.connect(db_file)
    cur = connection.cursor()

    cur.execute("DELETE FROM persons")
    connection.commit()
    connection.close()

    print("All entries removed (GDPR delete action).")


def mask_user_info():
    """Anonymize user names (GDPR pseudonymization)."""
    connection = sqlite3.connect(db_file)
    cur = connection.cursor()

    cur.execute("""
        UPDATE persons 
        SET full_name = 'Anonymiserad Användare'
    """)

    connection.commit()
    connection.close()
    
    print("User names anonymized (GDPR anonymization).")


# -----------------------------
# Huvudprogram
# -----------------------------
if __name__ == "__main__":
    setup_db()
    list_all_users()

    print("\nService running. Press Ctrl+C to exit.")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nStopping program...")