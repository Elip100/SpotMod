from colorama import Fore, Style, Back
from os import path
import platform, os, requests, platformdirs

version = 0.41
version_str = "0.4.1"
operating_system = platform.system()
sm_appdata = platformdirs.user_data_dir() + "\SpotMod"
datfolder = path.join(sm_appdata, "SpotMod-dat")
maindata = path.join(sm_appdata, "data.json")

bundle_dir = path.abspath(path.dirname(__file__))
defdat = path.join(bundle_dir, 'default_dat')

def clear():
    os.system("cls" if operating_system == "Windows" else "clear")
    print(f"{Back.GREEN}{Fore.BLACK} SpotMod Patcher v{version_str} {Style.RESET_ALL}{Fore.GREEN}\n")

def check_for_update():
    try:
        response = requests.get("https://elip100.github.io/SpotMod/data.json")
        return response.json()["latest_version"] > version
    except:
        return False