import os
from tqdm import tqdm
from yadisk import YaDisk
from colorama import init, Fore, Style
init()


def get_files_jpg():
    folder = os.getcwd()
    return [f for f in os.listdir(folder) if f.endswith('.jpg')]

def upload_to_yadick(folder_name:str):

    TOKEN = "y0_AgAAAAABJQnxAAkufQAAAADiFPV_TjOFwUIbR6KNgvJ5KSFpjefPkow"
    yadisk = YaDisk(token=TOKEN)

    if yadisk.check_token():
        print("Connection to YD")

    # создаем папку на яндекс-диске, если ее там нет
    if not yadisk.is_dir(folder_name):
        yadisk.mkdir(folder_name)

    folder_path = os.path.join(os.getcwd(),folder_name)

    try:
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for filename in tqdm(
                    filenames, desc=Fore.GREEN + Style.BRIGHT + "upload" + Fore.GREEN, unit=" file",
                    mininterval=0.01,
                    maxinterval=0.1, colour="green" , ncols=100
            ):
                file_path = os.path.join(dirpath, filename)
                # destination_path = os.path.join(f'/FOLDER', os.path.relpath(file_path, folder_path))
                destination_path = f"/{folder_name}/{filename}"
                yadisk.upload(file_path, destination_path)
                os.remove(file_path)

        os.rmdir(folder_path)

    except Exception as ex:
        print(Fore.LIGHTRED_EX + f"{ex}")


def choice_upload_to_yd(folder_name) -> None:
    while True:
        choice = input(Fore.LIGHTBLUE_EX + Style.BRIGHT + f"Переместить папку {folder_name} на яндекс-диск? (y/n): ")
        match choice.lower():
            case "y" | "yes" | "да"| "д" | "н":
                print(Fore.GREEN + "Перенос на яндекс диск")
                upload_to_yadick(folder_name=folder_name)
                break
            case "n" | "no" | "нет"| "т":
                break
            case _:
                print(Fore.LIGHTRED_EX + "Не понятен выбор. Повторите попытку")