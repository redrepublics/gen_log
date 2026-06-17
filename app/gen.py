import argparse
import random
from datetime import datetime, timedelta
import uuid


def generate_timestamps_with_peak(total_records, step_seconds=1):
    """
    Генератор временных меток для вчерашнего дня с пиком 13:00-15:00
    total_records: общее количество записей
    step_seconds: интервал между метками в секундах
    """
    yesterday = datetime.now() - timedelta(days=1)
    yesterday_date = yesterday.date()

    start_time = datetime.combine(yesterday_date, datetime.min.time())
    end_time = datetime.combine(yesterday_date, datetime.max.time())

    # Определяем пиковый период (13:00 - 15:00)
    peak_start = datetime.combine(yesterday_date, datetime.min.time().replace(hour=13))
    peak_end = datetime.combine(yesterday_date, datetime.min.time().replace(hour=15))

    # Собираем все возможные метки
    all_timestamps = []
    current = start_time

    while current <= end_time:
        all_timestamps.append(current)
        current += timedelta(seconds=step_seconds)

    # Если записей больше чем меток, дублируем с небольшим сдвигом
    if total_records > len(all_timestamps):
        # Добавляем случайные метки из пикового периода
        peak_timestamps = [ts for ts in all_timestamps if peak_start <= ts <= peak_end]
        extra_needed = total_records - len(all_timestamps)

        # Добавляем метки из пика
        for _ in range(extra_needed):
            all_timestamps.append(random.choice(peak_timestamps))

    # Если записей меньше чем меток, выбираем с учетом пика
    elif total_records < len(all_timestamps):
        # Отбираем метки так, чтобы 60% было в пике
        peak_timestamps = [ts for ts in all_timestamps if peak_start <= ts <= peak_end]
        normal_timestamps = [ts for ts in all_timestamps if not (peak_start <= ts <= peak_end)]

        selected = []

        # Выбираем 60% из пика
        peak_count = int(total_records * 0.6)
        if peak_timestamps:
            peak_selected = random.sample(peak_timestamps, min(peak_count, len(peak_timestamps)))
            selected.extend(peak_selected)

        # Остальные из обычного времени
        remaining = total_records - len(selected)
        if normal_timestamps and remaining > 0:
            normal_selected = random.sample(normal_timestamps, min(remaining, len(normal_timestamps)))
            selected.extend(normal_selected)

        # Если все еще не хватает, добираем из пика
        if len(selected) < total_records:
            all_remaining = [ts for ts in all_timestamps if ts not in selected]
            extra = random.sample(all_remaining, min(total_records - len(selected), len(all_remaining)))
            selected.extend(extra)

        all_timestamps = selected

    # Сортируем по времени
    all_timestamps.sort()

    # Форматируем в строки с миллисекундами
    for ts in all_timestamps:
        yield ts.strftime("%Y-%m-%d %H:%M:%S") + f".{ts.microsecond // 1000:03d}"


# Создаем парсер
parser = argparse.ArgumentParser(description='Генератор лог-файлов с пиковой нагрузкой')

yesterday = datetime.now() - timedelta(days=1)
file_log = f"log_{yesterday.strftime('%Y.%m.%d.%H.%M.%S')}.txt"

parser.add_argument('-n', '--number', type=int, default=30, help='Количество строк для генерации (по умолчанию: 30)')
parser.add_argument('-s', '--step', type=int, default=1,
                    help='Шаг между временными метками в секундах (по умолчанию: 1)')
args = parser.parse_args()
n = args.number
step = args.step

# Создаем генератор временных меток с пиком
timestamp_gen = generate_timestamps_with_peak(n, step)

# Проверяем, что меток достаточно
timestamps_list = list(timestamp_gen)
if len(timestamps_list) < n:
    # Если меток меньше чем нужно, дополняем из пикового периода
    yesterday_date = (datetime.now() - timedelta(days=1)).date()
    peak_start = datetime.combine(yesterday_date, datetime.min.time().replace(hour=13))
    peak_end = datetime.combine(yesterday_date, datetime.min.time().replace(hour=15))

    while len(timestamps_list) < n:
        # Генерируем случайную метку в пиковый период
        random_seconds = random.randint(
            int((peak_start - datetime.combine(yesterday_date, datetime.min.time())).total_seconds()),
            int((peak_end - datetime.combine(yesterday_date, datetime.min.time())).total_seconds())
        )
        new_ts = datetime.combine(yesterday_date, datetime.min.time()) + timedelta(seconds=random_seconds)
        timestamps_list.append(new_ts.strftime("%Y-%m-%d %H:%M:%S") + f".{new_ts.microsecond // 1000:03d}")

# Запись в файл
with open(file_log, 'w', encoding='utf-8') as file:
    for i in range(n):
        current_datetime = timestamps_list[i]

        num = round(random.uniform(0.1, 5.0), 2)
        result_status = random.choices(['Error 403', 'Ок', 'memory overflow'], weights=[0.2, 0.7, 0.1], k=1)[0]
        api_result = random.choices(['GET', 'POST', 'PUT'], weights=[0.2, 0.7, 0.1], k=1)[0]
        uid = uuid.uuid4()

        error_log_text = f"time: {current_datetime}, {api_result}/api/users/urn:uuid:{uid} HTTP/1.1, время отклика {num}ms, Server status {result_status}"
        file.write(f"{error_log_text}\n")

# Статистика
peak_count = sum(1 for ts in timestamps_list if '13:' in ts or '14:' in ts)
print(f"✅ Сгенерировано {n} записей в файл: {file_log}")
print(f"📅 Дата: {yesterday.strftime('%Y-%m-%d')}")
print(f"⏱️ Шаг между метками: {step} секунд")
print(f"🕐 Диапазон: с 00:00:00 до 23:59:59 вчерашнего дня")
print(f"📊 Записей в пиковый период (13:00-15:00): {peak_count} ({peak_count / n * 100:.1f}%)")