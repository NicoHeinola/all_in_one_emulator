import os
from typing import Dict, List
from ConfigManager import ConfigManager


class Rom:
    def __init__(self, name: str, extension: str) -> None:
        self._name = name
        self._extension = extension

    def get_name(self) -> str:
        return self._name

    def get_extension(self) -> str:
        return self._extension

    def __repr__(self) -> str:
        return f"(Rom: [{self.get_name(), self.get_extension()}])"

    def open(self) -> None:
        config: dict = ConfigManager.get_config()
        rom_folder_path = config['rom_folder_path']
        full_path = os.path.join(rom_folder_path, self._name + self.get_extension())

        extension_map = ConfigManager.get_extensions_per_emulator()
        emulator: str = extension_map[self.get_extension()]

        emulator_executable_path = os.path.join(config['emulators_folder_path'], emulator, config['emulators'][emulator]['executable_name'])
        print(emulator_executable_path)


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
