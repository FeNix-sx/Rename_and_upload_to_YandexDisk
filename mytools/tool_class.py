import csv
import os

class CodeNamePhone:
    def __init__(self, filename):
        self.__filename = self.__chek_name(filename)

    def __chek_name(self, filename: str) -> str:
        if filename.endswith("models.csv"):
            return filename
        else:
            print("Ошибка! Не найден файл 'models.csv', или имя файла изменено!")

    @property
    def get_names_code(self) -> dict|bool:
        """
        Читает модели телефона возвращает словарь с ними:
        ключ - название (вместо "/" пробел)
        значение - код из 6 цифр
        :return: dict
        """
        try:
            name_code_dict = dict()
            with open(self.__filename, encoding='utf-8') as r_file:
                # Создаем объект reader, указываем символ-разделитель ";"
                file_reader = csv.reader(r_file, delimiter=";")
                print("Файл с моделями загружен")
                # Счетчик для подсчета количества строк и вывода заголовков столбцов
                count = 0
                # Считывание данных из CSV файла
                for row in file_reader:
                    if count > 0:
                        # запись в словарь имен из файла с моделями
                        name_code_dict[row[1].replace("/", " ")] = row[0]

                    count += 1

                print(f'Найдено моделей телефонов: {count}.')

                return name_code_dict

        except Exception as ex:
            print(ex)
            print("Не удалось загрузить список смартфоном. Возможно отсутствует файл 'models.csv'")
            return False


class NamesFolder:
    def __init__(self):
        self.__foldername = self.__chek_folder_name()

    def __chek_folder_name(self) -> str|bool:
        try:
            foldername = [
                folder for folder in os.listdir('.') \
                if os.path.isdir(folder) and folder not in (
                    '.git', '.idea','venv', 'mytools'
                )
            ]
            if len(foldername) == 1:
                return str(foldername[0])
            else:
                raise ValueError

        except ValueError:
            print(
                f"Ошибка! Должна быть одна папка с названием/кодом телефона.\n"
                f"Проверьте название или удалите лишние папки."
            )
            return False

    @property
    def get_code_name(self):
        return self.__foldername


class FindCodeName:
    def __init__(self, names_codes:dict, foldername:str):
        self.__names_codes = names_codes
        self.__foldername = foldername

    @property
    def get_code(self):
        # если имя файла - название телефона
        if self.__foldername in self.__names_codes.keys():
            return self.__names_codes[self.__foldername]
        # если имя файла - код (из таблицы) телефона
        elif self.__foldername in self.__names_codes.values():
            for key, value in self.__names_codes.items():
                if self.__foldername == value:
                    return value


