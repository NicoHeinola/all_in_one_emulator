from strenum import StrEnum
import pyautogui


class HotkeyType(StrEnum):
    HOLD = "hold"
    PRESS = "press"


class HotkeyManager:
    @staticmethod
    def run_hotkey_config(hotkey_config: list) -> None:
        to_release = []
        for hotkey in hotkey_config:
            hotkey_type = hotkey['type']
            key = hotkey['key']

            if hotkey_type == HotkeyType.HOLD:
                to_release.append(key)
                pyautogui.keyDown(key)
            elif hotkey_type == HotkeyType.PRESS:
                pyautogui.press(key)

        for key in to_release:
            pyautogui.keyUp(key)
