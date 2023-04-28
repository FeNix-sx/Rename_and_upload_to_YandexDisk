import os


def get_files_jpg():
    folder = os.getcwd()
    return [f for f in os.listdir(folder) if f.endswith('.jpg')]