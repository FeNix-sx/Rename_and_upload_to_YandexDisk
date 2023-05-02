import time

from colorama import init, Fore, Style
init(autoreset=True)
from mytools import tool_class, tool_func


def manual_mode(folder_name) -> None:
    try:
        # запрос номера ракурса
        while True:
            racurs = input(Fore.CYAN + Style.BRIGHT +"C каким ракурсом работаем? Введите число от 1 до 4: ")

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

        for file_jpg in list_jpg:
            tool_class.MoveFile(
                new_dir=folder_name
            ).move_and_rename_file(
                old_name=file_jpg, racurs=racurs
            )

        all_racurs_count = len(tool_func.get_files_jpg(folder_name))

        print(
            Fore.GREEN + f"Обработаны файлы для {all_racurs_count//len(list_jpg)} ракурсов"
        )

        if all_racurs_count//len(list_jpg) == 4 and all_racurs_count % len(list_jpg) == 0:
            tool_func.choice_upload_to_yd(folder_name)

    except ValueError:
        pass


def auto_mode(folder_name: str) -> None:
    while True:
        count_jpg = input(Fore.CYAN + Style.BRIGHT + "Введите количество принтов для одного ракурса (число от 1 и более): ")
        if count_jpg.isdigit() and int(count_jpg)>0:
            count_jpg = int(count_jpg)
            break
        else:
            print(Fore.LIGHTRED_EX + Style.BRIGHT + "Ошибка! Нужно ввести число (больше 0).")

    try:
        for racurs in range(1, 5):
            # получаем список файлов *.jpg в текущей папке
            list_jpg = tool_func.get_files_jpg()
            # получаем список файлов, пока в нем не будет count_jpg
            while len(list_jpg) != count_jpg:
                print(Fore.GREEN + f"\rРакурс: {racurs} | Найдено файлов : {len(list_jpg)}", end="")
                time.sleep(0.5)
                list_jpg = tool_func.get_files_jpg()
            time.sleep(0.5)
            print(Fore.GREEN + f"\rРакурс: {racurs} | Найдено файлов : {len(list_jpg)}", end="")
            time.sleep(0.5)
            print(Fore.GREEN + f"\nПолучены все файлы для ракуса {racurs}")

            for file_jpg in list_jpg:
                tool_class.MoveFile(
                    new_dir=folder_name
                ).move_and_rename_file(
                    old_name=file_jpg, racurs=racurs
                )

        print(Fore.GREEN + Style.BRIGHT + f"Получено и обработано {racurs*count_jpg} файлов\n")

        tool_func.choice_upload_to_yd(folder_name)

        print(Fore.CYAN + Style.BRIGHT + "Завершение работы программы")
        time.sleep(2)

    except ValueError as vr:
        print(Fore.LIGHTRED_EX + f"{vr}")


def main() -> None:
    folder_name = tool_class.NamesFolder().get_code_name

    if not folder_name:
        return None

    while True:
        mode = input(Fore.CYAN + Style.BRIGHT + "Выберите режим работы (a - автоматический, р/m - ручной): ")
        match mode.lower():
            case "m" | "р":
                print("Режим работы: РУЧНОЙ")
                manual_mode(folder_name=folder_name)
                break
            case "а"|"a":
                print("Режим работы: АВТО")
                auto_mode(folder_name=folder_name)
                break
            case _:
                print(Fore.LIGHTRED_EX + Style.BRIGHT + "Не известный режим работы. Повторите попытку")

    return None


if __name__ == '__main__':
    main()