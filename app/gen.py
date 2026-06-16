# from datetime import datetime
from params_log import *
import random

file_log = f"date_{datetime.now().strftime('%Y.%m.%d.%H.%M.%S')}.txt"


N = input("Введите значение N: ")

if N == "" or N == "0":
    N = 30  # Если ввод пуст или равен "0", присваиваем значение 30

with open(file_log, 'w', encoding='utf-8') as file:
    for i in range(N):
        elements = ['Error 403', 'Ок']
        result_status = random.choices(elements, k=1)
        error_log_text = f"time: {current_datetime}, GET /api/users/123 HTTP/1.1, время отклика ,{time_stamp} Server status {result_status}"
        # Форматирование строки с инкрементом
        record = f"{error_log_text}\n"
        file.write(record)
