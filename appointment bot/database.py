import psycopg2

from config import password

conn = psycopg2.connect(dbname="appointment_bot", user="postgres", password=password)

cur = conn.cursor()


def create_db():
    cur.execute("CREATE TABLE IF NOT EXISTS clients (id integer PRIMARY KEY, tg varchar, name varchar)")
    cur.execute("CREATE TABLE IF NOT EXISTS dates (date_id serial PRIMARY KEY, date date UNIQUE, client_id integer references clients)")
    cur.execute("ALTER TABLE dates ALTER COLUMN client_id SET DEFAULT NULL")
    conn.commit()


def select_users(client_id, client_tg, client_name):
    cur.execute("INSERT INTO clients(id, tg, name) SELECT %s, $s, %s WHERE NOT EXISTS (SELECT id FROM clients WHERE id = %s)", (client_id, client_tg, client_name, client_id))
    conn.commit()