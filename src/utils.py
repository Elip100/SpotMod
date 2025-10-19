from colorama import Fore, Style, Back
from os import path
import platform, os, requests, platformdirs, zipfile, pefile

version = 0.5
version_str = "0.5"
operating_system = platform.system()
sm_appdata = platformdirs.user_data_dir() + "\SpotMod"
datfolder = path.join(sm_appdata, "SpotMod-dat")
maindata = path.join(sm_appdata, "data.json")
backdir = path.join(sm_appdata, "Backups")
backupdata = path.join(backdir, "backups.json")

bundle_dir = path.abspath(path.dirname(__file__))
defdat = path.join(bundle_dir, 'default_dat')

def clear():
    os.system("cls" if operating_system == "Windows" else "clear")
    print(f"{Back.GREEN}{Fore.BLACK} SpotMod Injector v{version_str} {Style.RESET_ALL}{Fore.GREEN}\n")

def check_for_update():
    try:
        response = requests.get("https://elip100.github.io/SpotMod/data.json")
        return response.json()["latest_version"] > version
    except:
        return False

def zip_directory(directory_path, zip_filename):
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(directory_path):
            for file in files:
                filepath = os.path.join(root, file)
                arcname = os.path.relpath(filepath, start=directory_path)
                zipf.write(filepath, arcname=arcname)

def get_file_version(path):
    pe = pefile.PE(path)
    for fileinfo in pe.FileInfo:
        for entry in fileinfo:
            if hasattr(entry, 'Key') and entry.Key == b'StringFileInfo':
                for st in entry.StringTable:
                    if b'FileVersion' in st.entries:
                        return st.entries[b'FileVersion'].decode()