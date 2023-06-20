from ast import Dict
import os
import requests
from helpers.ConfigManager import ConfigManager
import zipfile
import py7zr


class EmulatorDownloadManager:
    @staticmethod
    def download_emulator(name: str) -> bool:
        config: Dict = ConfigManager.get_config()
        emulators: Dict = config['emulators']

        # If emulator config not found
        if name not in emulators:
            return False

        emulators_folder_path: str = config['emulators_folder_path']
        save_folder_path: str = os.path.join(emulators_folder_path, name)
        if not os.path.exists(emulators_folder_path):  # Check if emulators folder exists, if not create it
            os.mkdir(emulators_folder_path)

        if not os.path.exists(save_folder_path):  # Check if specific emulator folder exists, if not create it
            os.mkdir(save_folder_path)

        # Get emulator config & download link
        emulator_config: str = emulators[name]
        download_link: str = emulator_config['download_link']

        # Get extension
        extension_array: list = download_link.split(".")
        extension: str = extension_array[len(extension_array) - 1]

        # Download & Save emulator
        response = requests.get(download_link)
        save_file_path: str = os.path.join(save_folder_path, name + "." + extension)
        with open(save_file_path, "wb+") as file:
            file.write(response.content)

        # If emulator is inside a zip file, extract it
        should_extract: bool = emulator_config['extract']
        if should_extract == True:
            # Extract all files
            if extension == "zip":
                with zipfile.ZipFile(save_file_path, 'r') as zip_ref:
                    zip_ref.extractall(save_folder_path)
            elif extension == "7z":
                with py7zr.SevenZipFile(save_file_path, mode='r') as archive:
                    archive.extractall(path=save_folder_path)
            else:
                return False

            # Remove the original zip file
            os.remove(save_file_path)

        return True
