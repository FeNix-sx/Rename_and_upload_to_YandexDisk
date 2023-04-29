import os
from tqdm import tqdm
from yadisk import YaDisk


def get_files_jpg():
    folder = os.getcwd()
    return [f for f in os.listdir(folder) if f.endswith('.jpg')]

def upload_to_yadick(folder_name:str):
    TOKEN = "y0_AgAAAAABJQnxAAkufQAAAADiFPV_TjOFwUIbR6KNgvJ5KSFpjefPkow"
    yadisk = YaDisk(token=TOKEN)
    # or
    # application_id = "fd1830fcca1744e88e0ced4205e0efb7"
    # application_secret = "ecfd67574d894e978343182840fa651et"
    # yadisk = YaDisk(application_id, application_secret, TOKEN)
    # print(yadisk.check_token())
    # print(yadisk.get_disk_info())

    # создаем объект класса YaDisk
    if yadisk.check_token():
        print("яндекс-диск подключен")

    # создаем папку на яндекс-диске, если ее там нет
    if not yadisk.is_dir(folder_name):
        yadisk.mkdir(folder_name)

    folder_path = os.path.join(os.getcwd(),folder_name)

    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in tqdm(filenames):
            file_path = os.path.join(dirpath, filename)
            # destination_path = os.path.join(f'/FOLDER', os.path.relpath(file_path, folder_path))
            destination_path = f"/{folder_name}/{filename}"
            yadisk.upload(file_path, destination_path)
            os.remove(file_path)

    os.rmdir(folder_path)