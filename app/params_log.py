from datetime import datetime

current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S") + f".{datetime.now().microsecond // 1000:03d}"
dt = datetime.now()
time_stamp = dt.strftime("%S") + f".{dt.microsecond // 1000:03d}"
