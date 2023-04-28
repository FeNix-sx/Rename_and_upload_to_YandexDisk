from mytools import tool_class, tool_func


def main():
    try:
        # получаем словарь: ключ - название телефона, значение - код соот-й названию
        names_codes_dict:dict = tool_class.CodeNamePhone("models.csv").get_names_code
        if not names_codes_dict:
            raise ValueError
        # получаем название модели телефона: название папки - это название/код телефона
        folder_name:str = tool_class.NamesFolder().get_code_name
        if not folder_name:
            raise ValueError
        # убеждаемся, что название или код есть в таблице (базе телефонов) файла models.csv
        code = tool_class.FindCodeName(
            names_codes=names_codes_dict,
            foldername=folder_name
        ).get_code

        list_jpg = tool_func.get_files_jpg()

        while True:
            racurs = input("C каким ракурсом работаем? Введите число от 1 до 4: ")
            if racurs not in ("1", "2", "3", "4"):
                print("Невозможное значение ракурса принта")
            else:
                break

        for file_jpg in list_jpg:
            tool_class.MoveFile(
                new_dir=folder_name
            ).move_and_rename_file(
                old_name=file_jpg, racurs=racurs
            )


    except ValueError:
        pass

if __name__ == '__main__':
    main()