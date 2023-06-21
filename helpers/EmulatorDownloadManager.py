import os
import requests
from helpers.ConfigManager import ConfigManager
import zipfile
import py7zr
from pywinauto import Application

from helpers.HotkeyManager import HotkeyManager


class EmulatorDownloadManager:
    @staticmethod
    def emulator_is_downloaded(name: str) -> bool:
        executable_path = ConfigManager.get_emulator_executable_path(name)
        return os.path.exists(executable_path)

    @staticmethod
    def download_emulator(name: str) -> bool:
        config: dict = ConfigManager.get_config()
        emulators: dict = config['emulators']

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

        # Download & Save emulator
        response = requests.get(download_link)

        # Get extension
        extension = emulator_config['extension']

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

        # If
        needs_to_open_once = emulator_config['needs_to_open_once']
        if needs_to_open_once:
            config: dict = ConfigManager.get_config()

            emulator_executable_path = ConfigManager.get_emulator_executable_path(name)
            current_dir = os.getcwd()

            # Open emulator
            cmd_command = f'start "" /B "{os.path.join(current_dir,emulator_executable_path)}"'
            os.system(cmd_command)

            # Make emulator top most
            app = Application().connect(path=emulator_executable_path)
            window = app.top_window()
            window.set_focus()  # Activate the window

            # Enter initializing hotkeys
            HotkeyManager.run_hotkey_config(config['emulators'][name]['initialize_hotkeys'])

            # Close emulator
            os.system(f"taskkill /F /IM {config['emulators'][name]['executable_name']}")

        return True
