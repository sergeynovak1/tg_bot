import psycopg2

from config import password

conn = psycopg2.connect(dbname="appointment_bot", user="postgres", password=password)

cur = conn.cursor()


def create_db():
    cur.execute("CREATE TABLE IF NOT EXISTS users (id bigint PRIMARY KEY, tg varchar, name varchar, role varchar); ALTER TABLE users ALTER COLUMN role SET DEFAULT 'client'")
    cur.execute("CREATE TABLE IF NOT EXISTS dates (date_id serial PRIMARY KEY, date date, time time, client_id bigint, another_data varchar); ALTER TABLE dates ALTER COLUMN client_id SET DEFAULT NULL")
    conn.commit()


def create_user(client_id, client_tg, client_name):
    cur.execute("INSERT INTO users(id, tg, name) SELECT %s, %s, %s WHERE NOT EXISTS (SELECT id FROM users WHERE id = %s)", (client_id, client_tg, client_name, client_id))
    conn.commit()


def user_exist(user_id):
    cur.execute("SELECT id FROM users WHERE id = %s", (user_id, ))
    return cur.fetchone()


def get_role(user_id):
    cur.execute("SELECT role FROM users WHERE id = %s", (user_id, ))
    return cur.fetchone()[0]


def create_date(date, time):
    cur.execute("INSERT INTO dates VALUES(default, %s, %s)", (date, time))
    conn.commit()


def free_date():
    cur.execute("SELECT date FROM dates WHERE client_id is null and another_data is null GROUP BY date ORDER BY date")
    return [x[0] for x in cur.fetchall()]


def all_date():
    cur.execute("SELECT date FROM dates GROUP BY date ORDER BY date")
    return [x[0] for x in cur.fetchall()]


def free_time(date):
    cur.execute("SELECT time FROM dates WHERE date::date = %s and client_id is null and another_data is null ORDER BY time", (date,))
    return cur.fetchall()


def all_time(date):
    cur.execute("SELECT * FROM dates WHERE date::date = %s ORDER BY time", (date,))
    return cur.fetchall()


def del_time(date_id):
    cur.execute("DELETE FROM dates WHERE date_id = %s", (date_id,))
    conn.commit()


def get_time_by_id(date_id):
    cur.execute("SELECT date, time FROM dates WHERE date_id = %s", (date_id,))
    return cur.fetchone()


def del_date(date):
    cur.execute("DELETE FROM dates WHERE date = %s", (date,))
    conn.commit()


def get_appointment_by_date_time(date, time):
    cur.execute("SELECT date_id FROM dates WHERE date = %s and time = %s", (date, time))
    return cur.fetchone()


def check_appointment(date_id):
    cur.execute("SELECT another_data, client_id FROM dates WHERE date_id = %s", (date_id,))
    print(cur.fetchone())
    return cur.fetchone()


def make_appointment(user_id, data, date_id):
    cur.execute("UPDATE dates SET client_id=%s, another_data=%s WHERE date_id=%s", (user_id, data, date_id))
    conn.commit()


def get_name_by_id(user_id):
    cur.execute("SELECT tg FROM users WHERE id = %s", (user_id,))
    return cur.fetchone()[0]


def get_app_by_name(user_id):
    cur.execute("SELECT date_id, date, time FROM dates WHERE client_id = %s", (user_id,))
    return cur.fetchall()


def remove_appointment(date_id):
    cur.execute("UPDATE dates SET client_id=null WHERE date_id=%s", (date_id,))
    conn.commit()


def app_info(date_id):
    cur.execute("SELECT client_id FROM dates WHERE date_id = %s", (date_id,))
    return cur.fetchone()[0]


def id_in_date(date):
    cur.execute("SELECT date_id FROM dates WHERE date = %s", (date,))
    return cur.fetchall()