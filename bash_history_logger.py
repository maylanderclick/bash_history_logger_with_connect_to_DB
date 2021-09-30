import psycopg2

conn = psycopg2.connect(dbname='bhlogger', user='postgres',
                        password='', host='localhost', port=5432)
cursor = conn.cursor()
# Распечатать сведения о PostgreSQL
print("Информация о сервере PostgreSQL")
print(conn.get_dsn_parameters(), "\n")

# Выполнение SQL-запроса
cursor.execute("SELECT version();")
# Получить результат
record = cursor.fetchone()

cursor.execute(
    "CREATE TABLE bash_history_logger (id SERIAL PRIMARY KEY, error_txt VARCHAR(1024));")
conn.commit()
print("Таблица успешно создана в PostgreSQL")

print("Вы подключены к - ", record, "\n")

f = open('/home/alena/.bash_history')
f_w = open('/home/alena/Рабочий стол/prog/py/bash_history_logger/txt.txt', 'w')

f_read = f.read()

f_mass = f_read.split('\n')

# print(f_read)

for s in f_mass:
    f_mass_2 = s.split()
    for i in f_mass_2:
        if i == 'sudo' or i == 'reboot' or i == 'rm -rf':
           # print(s)
            s = s.replace("'", " ")
            s = s.replace('"', ' ')
            cursor.execute(
                "INSERT INTO bash_history_logger(error_txt) VALUES(\'{}\')".format(s))
            conn.commit()
            f_w.write(s + '\n')
            break


f.close()
f_w.close()

cursor.close()
conn.close()
