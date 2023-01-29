import psycopg2

from config import password

conn = psycopg2.connect(dbname="appointment_bot", user="postgres", password=password)

cur = conn.cursor()


def create_db():
    cur.execute("CREATE TABLE IF NOT EXISTS clients (id integer PRIMARY KEY, tg varchar, name varchar, role varchar); ALTER TABLE clients ALTER COLUMN role SET DEFAULT 'client'")
    cur.execute("CREATE TABLE IF NOT EXISTS dates (date_id serial PRIMARY KEY, date date UNIQUE, client_id integer references clients); ALTER TABLE dates ALTER COLUMN client_id SET DEFAULT NULL")
    conn.commit()


def create_user(client_id, client_tg, client_name):
    cur.execute("INSERT INTO clients(id, tg, name) SELECT %s, %s, %s WHERE NOT EXISTS (SELECT id FROM clients WHERE id = %s)", (client_id, client_tg, client_name, client_id))
    conn.commit()