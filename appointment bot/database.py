import psycopg2

from config import password

conn = psycopg2.connect(dbname="appointment_bot", user="postgres", password=password)

cur = conn.cursor()


def create_db():
    cur.execute("CREATE TABLE IF NOT EXISTS users (id integer PRIMARY KEY, tg varchar, name varchar, role varchar); ALTER TABLE users ALTER COLUMN role SET DEFAULT 'client'")
    cur.execute("CREATE TABLE IF NOT EXISTS dates (date_id serial PRIMARY KEY, date date UNIQUE, client_id integer references users); ALTER TABLE dates ALTER COLUMN client_id SET DEFAULT NULL")
    conn.commit()


def create_user(client_id, client_tg, client_name):
    cur.execute("INSERT INTO users(id, tg, name) SELECT %s, %s, %s WHERE NOT EXISTS (SELECT id FROM users WHERE id = %s)", (client_id, client_tg, client_name, client_id))
    conn.commit()


def get_role(user_id):
    cur.execute("SELECT role FROM users WHERE id = %s", (user_id,))
    return cur.fetchone()[0]
