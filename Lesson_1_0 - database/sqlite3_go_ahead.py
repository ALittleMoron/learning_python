import sqlite3
import os.path


def connect_to_database(database_name:str, path:str = '') -> sqlite3.Connection:
    """ Функция подключения к базе данных. Возвращает соединение на уже
    существующую базу данных (Не хочу случайно создать лишнюю БД).

    аргументы:
    database_name -- файл базы данных
    path -- путь к файлу базы данных (Опциональный. Не передавать аргумент,
    если база данных находится рядом с python файлом.
    """
    database = os.path.join(path, database_name)
    if os.path.isfile(database) and ('.db' in database or '.sqlite' in database):
        connection = sqlite3.connect(database, timeout=5)
        return connection
    else:
        return None


def create_databace_table(connection:sqlite3.Connection,
                          table_name:str, args:dict) -> bool:
    """ Функция создания таблицы в базе данных

    аргументы:
    connection -- соединение с базой данных
    table_name -- название таблицы
    args -- словарь элементов таблицы с их типами. Пример: {'title': 'TEXT'}
    """
    if connection is None:
        raise Exception('Неправильное название базы данных. Введите существующую')
    if type(table_name) is not str:
        raise Exception('Название таблицы может быть только строковое')
    if type(args) is not dict:
        raise Exception('элементы таблицы и их типы могут быть представлены только в словаре')
    cursor = connection.cursor()
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table_name.lower()} (
                       {', '.join(f'{k} {v}' for k,v in args.items())})""")
    connection.commit()
    connection.close()


def add_info_to_table(connection:sqlite3.Connection,
                      table_name:str, args:tuple) -> None:
    """ Функция добавления информации в имеющуюся таблицу в базе данных

    аргументы:
    cursor -- курсор на базу данных
    table_name -- название таблицы
    args -- кортеж элементов таблицы без их типов. Пример: ('something', ...)
    """
    if connection is None:
        raise Exception('Неправильное название базы данных. Введите существующую')
    if type(args) is not tuple:
        raise Exception('аргумент args может быть только кортежем или списком')
    cursor = connection.cursor()
    cursor.execute(f"""INSERT INTO {table_name.lower()} VALUES
                       (?{', ?' * (len(args)-1)})""", args)
    connection.commit()
    connection.close()


if __name__ == '__main__':
    dct = {'title': 'TEXT',
           'author': 'TEXT'}
    data = ('asgas', 'asgsagags')
    add_info_to_table(connect_to_database('MyDataBase.db'), 'abstract', data)
