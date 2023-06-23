from helpers.ConfigManager import ConfigManager
from helpers.EmulatorDownloadManager import EmulatorDownloadManager
from ui.MainUI import MainUI


if __name__ == '__main__':
    config = ConfigManager.get_config()
    emulators = config['emulators']
    for emulator in emulators:
        if EmulatorDownloadManager.emulator_is_downloaded(emulator):
            print("Already downloaded:", emulator)
            continue
        ok = EmulatorDownloadManager.download_emulator(emulator)
        print(ok, emulator)

    ui = MainUI(1280, 720)
    ui.run()
