import time

from mytools import tool_class, tool_func

def manual_mode() -> None:
    try:
        # запрос номера ракурса
        while True:
            racurs = input("C каким ракурсом работаем? Введите число от 1 до 4: ")
            if racurs not in ("1", "2", "3", "4"):
                print("Невозможное значение ракурса принта")
            else:
                break

        # получаем список файлов *.jpg в текущей папке
        list_jpg = tool_func.get_files_jpg()
        if not len(list_jpg):
            print("В текущей папке нет принтов для работы\n"
                  "Поместите в папку файлы с названием &&&.jpg (где & - цифра от 0 до 9) и заново запустите программу" )
            time.sleep(5)
            return

        # получаем словарь: ключ - название телефона, значение - код соот-й названию
        names_codes_dict: dict = tool_class.CodeNamePhone("models.csv").get_names_code
        if not names_codes_dict:
            raise ValueError
        # получаем название модели телефона: название папки - это название/код телефона
        folder_name: str = tool_class.NamesFolder().get_code_name
        if not folder_name:
            raise ValueError
        # убеждаемся, что название или код есть в таблице (базе телефонов) файла models.csv
        code = tool_class.FindCodeName(
            names_codes=names_codes_dict,
            foldername=folder_name
        ).get_code

        for file_jpg in list_jpg:
            tool_class.MoveFile(
                new_dir=folder_name
            ).move_and_rename_file(
                old_name=file_jpg, racurs=racurs
            )


    except ValueError:
        pass


def auto_mode() -> None:
    pass


def main():
    while True:
        mode = input("Выберите режим работы (a - автоматический, р/m - ручной): ")
        match mode:
            case "a"|"а":
                print("Режим работы: РУЧНОЙ")
                manual_mode()
                break
            case "а"|"a":
                print("Режим работы: АВТО")
                auto_mode()
                break
            case _:
                print("Не известный режим работы. Повторите попытку")


if __name__ == '__main__':
    main()