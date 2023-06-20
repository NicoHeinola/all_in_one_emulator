from helpers.ConfigManager import ConfigManager
from helpers.EmulatorDownloadManager import EmulatorDownloadManager


if __name__ == '__main__':
    ConfigManager.load_config()
    ok = EmulatorDownloadManager.download_emulator('visual_boy_advance')
    print(ok)
