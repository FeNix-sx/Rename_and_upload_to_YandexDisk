import csv
import os
import shutil
import re
import time

from dotenv import load_dotenv
from colorama import init, Fore, Style
init(autoreset=True)


class CodeNamePhone:
    def __init__(self, filename):
        self.__filename = self.__chek_name(filename)

    def __chek_name(self, filename: str) -> str:
        if filename.endswith("models.csv"):
            return filename
        else:
            print("Ошибка! Не найден файл 'models.csv', или имя файла изменено!")

    @property
    def get_names_code(self) -> dict:
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
            return None


class NamesFolder:
    def __init__(self):
        self.__foldername = self.__chek_folder_name()

    def __chek_folder_name(self) -> str|bool:
        try:
            foldername = [
                folder for folder in os.listdir('.') \
                if os.path.isdir(folder) and folder not in (
                    '.git', '.idea','venv', 'mytools', 'output'
                )
            ]
            if len(foldername) != 1:
                raise ValueError

            old_name = foldername[0]

            # получаем словарь: ключ - название телефона, значение - код соот-й названию
            names_codes_dict: dict = CodeNamePhone("models.csv").get_names_code
            if not names_codes_dict:
                raise None

            # убеждаемся, что название или код есть в таблице (базе телефонов) файла models.csv
            code_name = FindCodeName(
                names_codes=names_codes_dict,
                foldername=old_name
            ).get_code

            self.__rename_folder(old_name, code_name)
            return code_name

        except ValueError:
            print(
                Fore.LIGHTRED_EX + f"Ошибка! Должна быть одна папка с названием/кодом телефона.\n",
                Fore.LIGHTRED_EX + f"Проверьте наличие папки, её название или удалите лишние папки.",
                sep=''
            )
            time.sleep(3)
            return False

    def __rename_folder(self, old_name: str, new_name: str) -> None:
        os.rename(old_name, new_name)

    @property
    def get_code_name(self) -> str:
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


class MoveFile:
    def __init__(self, new_dir:str):
        self.__new_dir = new_dir
        self.__current_dir = os.getcwd()
        self.__new_dir_path = os.path.join(self.__current_dir, self.__new_dir)

    def __get_new_name(self, name: str, racurs:str) ->str:
        # загрузка параметров: FOLDER_PATH - папка, в которую сохранится folder_name на яддекс_диске
        while True:
            try:
                dotenv_path = 'setting.env'

                if os.path.exists(dotenv_path):
                    load_dotenv(dotenv_path)

                PREFIX = os.getenv('PREFIX')

                if PREFIX == "":
                    raise ValueError
                break



            except Exception as ex:
                print(Fore.LIGHTRED_EX + f"Ошибка! {ex}")
                print(
                    Fore.LIGHTRED_EX + f"Проверьте наличие файла 'setting.env' и наличие в нём параметра PREFIX.")
                if input(Fore.CYAN + Style.BRIGHT + "Повторить попытку? (y/n)") == "y":
                    continue
                else:
                    return

        # racurs = input("C каким ракурсом работаем? Введите число от 1 до 4: ")
        pref = "" if racurs in ("1", 1) else f"_{racurs}"
        # имя файла 001.jpg, 052.jpg и т.д.
        regex = r"\d+"
        res = re.findall(regex, name)[0]
        new_name = f"{self.__new_dir}-{PREFIX}#{str(res).rjust(3,'0')}{pref}.jpg"
        return new_name

    def move_and_rename_file(self, old_name:str, racurs:str):
        try:
            new_name = self.__get_new_name(old_name, racurs)
            old_file_path = os.path.join(self.__current_dir, old_name)
            new_file_path = os.path.join(self.__new_dir_path, new_name)
            shutil.move(old_file_path, new_file_path)
            # print(f"Файл {old_name} переименован в {new_name}\n"
            #       f"и перемещен в папку {new_file_path}")

        except Exception as ex:
            print(Fore.LIGHTRED_EX + f"{ex}")