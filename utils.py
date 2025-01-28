from colorama import Fore, Style, Back
import platform, os

version = 0.3
operating_system = platform.system()

def clear():
    os.system("cls" if operating_system == "Windows" else "clear")
    print(f"{Back.GREEN}{Fore.BLACK} SpotMod Patcher v{str(version)} {Style.RESET_ALL}{Fore.GREEN}\n")