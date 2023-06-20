from enum import Enum
import os
from typing import List
from flask import request
import requests
from bs4 import BeautifulSoup
import zipfile


class VimmsLairRegion(Enum):
    EUROPE = 8
    USA = 25
    JAPAN = 15
    ALL = "All"


class VimmsLairEmulator(Enum):
    SNES = "SNES"
    NES = "NES"
    VIRTUAL_BOY = "VB"
    GAME_BOY = "GB"
    GAME_BOY_ADVANCE = "GBA"
    GAME_BOY_COLOR = "GBC"
    NINTENDO_64 = "N64"


class VimmsLairRom:
    def __init__(self, name: str, id: str, region: VimmsLairRegion, emulator: VimmsLairEmulator) -> None:
        self._name = name
        self._id = id  # Vault id
        self._region = region
        self._emulator = emulator
        self._media_id: str = None

    def _find_media_id(self) -> str:
        if self._media_id is not None:
            return self._media_id

        url = f"https://vimm.net/vault/{self._id}"
        r = requests.get(url)
        html = r.text

        soup = BeautifulSoup(html, 'html.parser')
        media_id_element = soup.find('input', {"name": "mediaId"})
        media_id = media_id_element['value']
        self._media_id = media_id

        return self._media_id

    def download(self, output_folder: str) -> None:
        media_id = self._find_media_id()

        download_base_url = "https://download3.vimm.net/download/?mediaId="
        full_url = download_base_url + media_id

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0",
            "Referer": "https://vimm.net/"
        }

        if not os.path.exists(output_folder):
            os.mkdir(output_folder)

        r = requests.get(full_url, headers=headers)

        ext = r.headers['content-type'].split('/')[-1]
        output_file = self._name + "." + ext
        output_path = os.path.join(output_folder, output_file)
        with open(output_path, 'wb+') as f:
            f.write(r.content)

        ZIP_EXTENSION = "zip"
        if ext == ZIP_EXTENSION:
            zip_file = zipfile.ZipFile(output_path, 'r')
            NOT_ALLOWED_EXTENSIONS = ('.txt')

            # Extract all game files from zip
            for file in zip_file.namelist():
                if file.endswith(NOT_ALLOWED_EXTENSIONS):
                    continue

                zip_file.extract(file, output_folder)
            zip_file.close()

            # Delete zip
            os.remove(output_path)

    def __repr__(self) -> str:
        return f"(VimmsLairRom: {self._name, self._id, self._region, self._emulator}))"


class VimmsLairSearchAPI:
    @staticmethod
    def search_roms(region: VimmsLairRegion, emulator: VimmsLairEmulator, term: str = "") -> List[VimmsLairRom]:
        base_url: str = "https://vimm.net/vault/?"
        terms: str = f"mode=adv&p=list&system={emulator.value}&q={term}&players=%3E%3D&playersValue=1&simultaneous=&publisher=&year=%3D&yearValue=&cart=%3D&cartValue=&rating=%3E%3D&ratingValue=&region={region.value}&sort=Title&sortOrder=ASC"
        full_url: str = base_url + terms

        r = requests.get(full_url)
        html = r.text

        soup = BeautifulSoup(html, 'html.parser')
        full_rom_table_element = soup.find("table", {"class": "rounded centered cellpadding1 hovertable striped"})

        # Find header order
        header_elements = full_rom_table_element.find('table', {"class": "cellpadding1"}).find_all("td")
        headers = {header_element.text.lower(): index for index, header_element in enumerate(header_elements)}

        # Find rom elements
        rom_elements: List[BeautifulSoup] = full_rom_table_element.find_all('tr')
        rom_elements = rom_elements[1:]  # Skip titles

        roms: List[VimmsLairRom] = []
        for rom_element in rom_elements:
            td_elements = rom_element.find_all('td')

            link = td_elements[headers['title']].find('a', href=True)
            name = link.text
            id = link['href'].split("/")[2]

            rom = VimmsLairRom(name, id, region, emulator)
            roms.append(rom)
        return roms


if __name__ == "__main__":
    roms = VimmsLairSearchAPI.search_roms(VimmsLairRegion.ALL, VimmsLairEmulator.SNES, 'super mario world')
    print(roms[0])
    roms[0].download('roms')
    print(VimmsLairEmulator.GAME_BOY.name)
