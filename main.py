import time
from colorama import init, Fore, Style
init(autoreset=True)
from mytools import tool_class, tool_func


def manual_mode() -> None:
    try:
        # запрос номера ракурса
        while True:
            racurs = input(Fore.LIGHTBLUE_EX + Style.BRIGHT +"C каким ракурсом работаем? Введите число от 1 до 4: ")

            if racurs not in ("1", "2", "3", "4"):
                print(Fore.LIGHTRED_EX + Style.BRIGHT + "Невозможное значение ракурса принта")
            else:
                break

        # получаем список файлов *.jpg в текущей папке
        list_jpg = tool_func.get_files_jpg()

        if not len(list_jpg):
            print(
                Fore.LIGHTRED_EX + Style.BRIGHT + "В текущей папке нет принтов для работы\n",
                Fore.LIGHTRED_EX + Style.BRIGHT + "Поместите в папку файлы с названием &&&.jpg "
                                                   "(где & - цифра от 0 до 9) и заново запустите программу",
                sep=''
            )
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
                new_dir=code
            ).move_and_rename_file(
                old_name=file_jpg, racurs=racurs
            )

        # tool_func.choice_upload_to_yd(folder_name)

    except ValueError:
        pass


def auto_mode() -> None:
    while True:
        count_jpg = input(Fore.LIGHTBLUE_EX + Style.BRIGHT + "Введите количество принтов для одного ракурса (число от 1 и более): ")
        if count_jpg.isdigit() and int(count_jpg)>0:
            count_jpg = int(count_jpg)
            break
        else:
            print(Fore.LIGHTRED_EX + Style.BRIGHT + "Ошибка! Нужно ввести число (больше 0).")

    folder_name: str = ""

    try:
        # получаем словарь: ключ - название телефона, значение - код соот-й названию
        names_codes_dict: dict = tool_class.CodeNamePhone("models.csv").get_names_code
        if not names_codes_dict:
            raise ValueError

        for racurs in range(1, 5):
            # получаем список файлов *.jpg в текущей папке
            list_jpg = tool_func.get_files_jpg()
            # получаем список файлов, пока в нем не будет count_jpg
            while len(list_jpg) != count_jpg:
                print(Fore.GREEN + f"\rРакурс: {racurs} | Найдено файлов : {len(list_jpg)}", end="")
                time.sleep(0.5)
                list_jpg = tool_func.get_files_jpg()

            print(Fore.GREEN + f"\nПолучены все файлы для ракуса {racurs}")

            # получаем название модели телефона: название папки - это название/код телефона
            folder_name = tool_class.NamesFolder().get_code_name
            if not folder_name:
                raise ValueError

            # убеждаемся, что название или код есть в таблице (базе телефонов) файла models.csv
            code = tool_class.FindCodeName(
                names_codes=names_codes_dict,
                foldername=folder_name
            ).get_code

            for file_jpg in list_jpg:
                tool_class.MoveFile(
                    new_dir=code
                ).move_and_rename_file(
                    old_name=file_jpg, racurs=racurs
                )

        print(Fore.GREEN + Style.BRIGHT + f"Получено и обработано {racurs*count_jpg} файлов\n")

        tool_func.choice_upload_to_yd(folder_name)
        # while True:
        #     choice = input(f"Переместить папку {folder_name} на яндекс-диск? (y/n): ")
        #     match choice:
        #         case "y" | "yes" | "да"| "д" | "н":
        #             print("Перенос на яндекс диск")
        #             tool_func.upload_to_yadick(folder_name=folder_name)
        #             break
        #         case "n" | "no" | "нет"| "т":
        #             break
        #         case _:
        #             print(Fore.LIGHTRED_EX + "Не понятен выбор. Повторите попытку")

        print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "Завершение работы программы")
        time.sleep(2)

    except ValueError as vr:
        print(Fore.LIGHTRED_EX + f"{vr}")

def main() -> None:
    while True:
        mode = input(Fore.LIGHTBLUE_EX + Style.BRIGHT + "Выберите режим работы (a - автоматический, р/m - ручной): ")
        match mode.lower():
            case "m" | "р":
                print("Режим работы: РУЧНОЙ")
                manual_mode()
                break
            case "а"|"a":
                print("Режим работы: АВТО")
                auto_mode()
                break
            case _:
                print(Fore.LIGHTRED_EX + Style.BRIGHT + "Не известный режим работы. Повторите попытку")

    return None


if __name__ == '__main__':
    main()