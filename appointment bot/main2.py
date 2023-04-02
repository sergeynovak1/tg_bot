import datetime

from database import create_date, get_appointment_by_date_time
from config import duration_time


def get_db_date(date):
    return f"{date[3:]}.{date[:2]}.{datetime.datetime.now().year}"


def get_data(date):
    day = f"{date.day}" if date.day > 9 else f"0{date.day}"
    month = f"{date.month}" if date.month > 9 else f"0{date.month}"
    return f"{day}.{month}"


def get_time(time):
    hour = f"{time.hour}" if time.hour > 9 else f"0{time.hour}"
    minutes = f"{time.minute}" if time.minute > 9 else f"0{time.minute}"
    return f"{hour}:{minutes}"


def insert_appointment(date, time):
    x = []
    start_time = time[:5] + ':00'
    if len(time)>5:
        end_time = time[6:] + ':00'
        while datetime.datetime.strptime(end_time, '%H:%M:%S') >= (datetime.datetime.strptime(start_time,'%H:%M:%S') + datetime.timedelta(minutes=duration_time)):
            x.append(datetime.datetime.strptime(start_time, '%H:%M:%S').time())
            start_time = str((datetime.datetime.strptime(start_time, '%H:%M:%S') + datetime.timedelta(minutes=duration_time)).time())
    else:
        x.append(datetime.datetime.strptime(start_time, '%H:%M:%S').time())
    for z in x:
        if not get_appointment_by_date_time(date, z):
            create_date(date, z)



