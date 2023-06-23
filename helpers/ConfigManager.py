import json
import os
from typing import Dict


class ConfigManager:
    config_path = './config.json'
    config_data = {}
    loaded_config_once = False
    extensions_per_emulator: Dict[str, str] = None
    loaded_extensions_per_emulator_once = False

    @staticmethod
    def get_emulator_executable_path(emulator) -> str:
        config: dict = ConfigManager.get_config()
        emulator_executable_path = os.path.join(config['emulators_folder_path'], emulator, config['emulators'][emulator]['executable_name'])
        return emulator_executable_path

    @staticmethod
    def load_emulator_extension_map() -> None:
        config: dict = ConfigManager.get_config()
        emulators = config['emulators']

        extensions_map = {}
        for emulator, data in emulators.items():
            for file_type in data['file_types']:
                extensions_map[file_type] = emulator

        ConfigManager.extensions_per_emulator = extensions_map
        ConfigManager.loaded_extensions_per_emulator_once = True

    @staticmethod
    def get_extensions_per_emulator() -> Dict[str, str]:
        if not ConfigManager.loaded_extensions_per_emulator_once:
            ConfigManager.load_emulator_extension_map()

        return ConfigManager.extensions_per_emulator

    @staticmethod
    def load_config() -> None:
        # Loads config data
        with open(ConfigManager.config_path, 'r') as file:
            data = json.loads(file.read())
            ConfigManager.config_data = data

        ConfigManager.loaded_config_once = True

    @staticmethod
    def get_config() -> dict:
        if not ConfigManager.loaded_config_once:
            ConfigManager.load_config()

        return ConfigManager.config_data
