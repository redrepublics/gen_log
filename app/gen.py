from datetime import datetime
from params_log import *


N = int(input("Ввежите колличество строк"))  # заданное количество записей

with open(file_log, 'w', encoding='utf-8') as file:
    for i in range(N):
        # Форматирование строки с инкрементом
        record = f"{error_log_text}\n"
        file.write(record)