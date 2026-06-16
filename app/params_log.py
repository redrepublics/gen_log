from datetime import datetime
import time

current_datetime = datetime.now().strftime("%YYYY-%MM-%D %HH:%S:%M:%MS")
time_stamp = datetime.now().strftime("%S:%MS")

# YYYY-MM-DDThh:mm:ss:ms <имя метода> <время отклика> <OK|ERROR>