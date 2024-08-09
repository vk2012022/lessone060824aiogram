import sqlite3

# Подключаемся к базе данных
conn = sqlite3.connect('school_data.db')
cur = conn.cursor()

# Выполняем запрос для получения всех данных из таблицы students
cur.execute("SELECT * FROM students")

# Выводим данные на экран
rows = cur.fetchall()
for row in rows:
    print(row)

# Закрываем соединение
conn.close()
