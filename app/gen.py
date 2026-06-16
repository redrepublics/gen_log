import argparse
import random
from datetime import datetime, timedelta

yesterday_pas = datetime.now() - timedelta(days=1)
current_datetime = yesterday_pas.strftime("%Y-%m-%d %H:%M:%S") + f".{yesterday_pas.microsecond // 1000:03d}"
# Создаем парсер
parser = argparse.ArgumentParser(description='Генератор лог-файлов')

yesterday = datetime.now() - timedelta(days=1)
file_log = f"date_{yesterday.strftime('%Y.%m.%d.%H.%M.%S')}.txt"

parser.add_argument('-n', '--number', type=int, default=30,  help='Количество строк для генерации (по умолчанию: 30)')
args = parser.parse_args()
n = args.number


with open(file_log, 'w', encoding='utf-8') as file:
    for i in range(n):
        num = round(random.random(), 2)
        elements = ['Error 403', 'Ок']
        result_status = random.choices(elements, k=1)
        error_log_text = f"time: {current_datetime}, GET /api/users/123 HTTP/1.1, время отклика ,{num} Server status {result_status}"
        # Форматирование строки с инкрементом
        record = f"{error_log_text}\n"
        file.write(record)
