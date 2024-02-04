import csv
import os
import psycopg2
from datetime import datetime


# Получение текущей директории скрипта
current_dir = os.path.dirname(os.path.abspath(__file__))

# Создание подключения к базе данных
conn = psycopg2.connect(
    host="localhost",
    database="north",
    user="postgres",
    password="1234qweR@"
)

# Формирование полного пути к CSV-файлу
csv_file_path = os.path.join(current_dir, "north_data", "employees_data.csv")

# Открытие CSV-файла и чтение данных
with open(csv_file_path, 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Пропуск заголовков, если они есть
    for row in reader:
        # Преобразование значения "birth_date" в объект date
        birth_date = datetime.strptime(row[4], '%Y-%m-%d').date()
        # Вставка данных в базу данных
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO employees (first_name, last_name, title, birth_date, notes)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (row[1], row[2], row[3], row[4], row[5])
        )
        conn.commit()


# Формирование полного пути к CSV-файлу
csv_file_path2 = os.path.join(current_dir, "north_data", "customers_data.csv")

# Открытие CSV-файла и чтение данных
with open(csv_file_path2, 'r') as file2:
    reader2 = csv.reader(file2)
    next(reader2)  # Пропуск заголовков, если они есть
    for row in reader2:
        # Вставка данных в базу данных
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO customers (customer_id, company_name, contact_name)
            VALUES (%s, %s, %s)
            """,
            (row[0], row[1], row[2])
        )
        conn.commit()

# Формирование полного пути к CSV-файлу
csv_file_path3 = os.path.join(current_dir, "north_data", "orders_data.csv")

with open(csv_file_path3, 'r') as orders_file:
    order_reader = csv.DictReader(orders_file)
    for row in order_reader:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO orders (order_id, customer_id, employee_id, order_date, ship_city)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (row['order_id'], row['customer_id'], row['employee_id'], row['order_date'], row['ship_city'])
        )
        conn.commit()

# Закрытие подключения
cur.close()
conn.close()