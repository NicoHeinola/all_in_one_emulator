import os
import time
from typing import Dict, List
from ConfigManager import ConfigManager
import pyautogui
from pywinauto import Application

from HotkeyManager import HotkeyManager


class Rom:
    def __init__(self, name: str, extension: str) -> None:
        self._name = name
        self._extension = extension
        self._open = False

    def get_name(self) -> str:
        return self._name

    def get_extension(self) -> str:
        return self._extension

    def get_emulator(self) -> str:
        extension_map = ConfigManager.get_extensions_per_emulator()
        emulator: str = extension_map[self.get_extension()]
        return emulator

    def __repr__(self) -> str:
        return f"(Rom: [{self.get_name(), self.get_extension()}])"

    def open(self) -> None:
        if self._open:
            return

        config: dict = ConfigManager.get_config()
        rom_folder_path = config['rom_folder_path']
        full_path = os.path.join(rom_folder_path, self._name + "." + self.get_extension())

        emulator_executable_path = ConfigManager.get_emulator_executable_path(self.get_emulator())

        current_dir = os.getcwd()

        cmd_command = f'start "" /B "{os.path.join(current_dir,emulator_executable_path)}" "{os.path.join(current_dir,full_path)}"'
        os.system(cmd_command)

        self._open = True

    def make_top_most(self) -> None:
        if not self._open:
            return

        emulator_executable_path = ConfigManager.get_emulator_executable_path(self.get_emulator())
        app = Application().connect(path=emulator_executable_path)

        # Set the program window as topmost
        window = app.top_window()
        window.set_focus()  # Activate the window

    def make_full_screen(self) -> None:
        if not self._open:
            return

        self.make_top_most()

        config: dict = ConfigManager.get_config()
        emulator = self.get_emulator()
        HotkeyManager.run_hotkey_config(config['emulators'][emulator]['full_screen_hotkey_configurations'])

    def close(self) -> None:
        if not self._open:
            return

        config: dict = ConfigManager.get_config()
        extension_map = ConfigManager.get_extensions_per_emulator()
        emulator: str = extension_map[self.get_extension()]
        os.system(f"taskkill /F /IM {config['emulators'][emulator]['executable_name']}")

        self._open = False


class RomManager:
    def get_rom_list() -> List[Rom]:
        config: dict = ConfigManager.get_config()
        rom_folder_path = config['rom_folder_path']

        if not os.path.exists(rom_folder_path):
            return []

        os_files = os.listdir(rom_folder_path)
        roms: List[Rom] = []
        for file in os_files:
            file_path = os.path.join(rom_folder_path, file)
            file_name, file_extension = os.path.splitext(file)

            rom = Rom(file_name, file_extension[1:])  # Remove dot from extension
            roms.append(rom)

        return roms


if __name__ == "__main__":
    roms = RomManager.get_rom_list()
    roms[0].open()
    roms[0].make_top_most()
    roms[0].make_full_screen()
    time.sleep(2)
    roms[0].close()
