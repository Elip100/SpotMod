from colorama import Fore, Style, Back
import platform, os, requests, json

version = 0.3
operating_system = platform.system()

def clear():
    os.system("cls" if operating_system == "Windows" else "clear")
    print(f"{Back.GREEN}{Fore.BLACK} SpotMod Patcher v{str(version)} {Style.RESET_ALL}{Fore.GREEN}\n")

def check_for_update():
    try:
        response = requests.get("https://elip100.github.io/SpotMod/data.json")
        return response.json()["latest_version"] > version
    except:
        return False