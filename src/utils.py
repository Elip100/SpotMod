import sys
import os
import platform
import zipfile
import json
from os import path

import pefile
import platformdirs
import requests
from colorama import Back, Fore, Style
from tkinter import filedialog

version = 0.52
version_str = "0.5.2"
operating_system = platform.system()
sm_appdata = platformdirs.user_data_dir() + "/SpotMod"
datfolder = path.join(sm_appdata, "SpotMod-dat")
maindata = path.join(sm_appdata, "data.json")
backdir = path.join(sm_appdata, "Backups")
backupdata = path.join(backdir, "backups.json")

bundle_dir = path.abspath(path.dirname(__file__))
defdat = path.join(bundle_dir, "default_dat")

appsfolder = "apps" if operating_system == "Windows" else "Apps"


def clear():
    os.system("cls" if operating_system == "Windows" else "clear")
    print(
        f"{Back.GREEN}{Fore.BLACK} SpotMod Injector v{version_str} {Style.RESET_ALL}{Fore.GREEN}\n"
    )


def check_for_update():
    try:
        response = requests.get("https://elip100.github.io/SpotMod/data.json")
        return response.json()["latest_version"] > version
    except:
        return False


def zip_directory(directory_path, zip_filename):
    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(directory_path):
            for file in files:
                filepath = os.path.join(root, file)
                arcname = os.path.relpath(filepath, start=directory_path)
                zipf.write(filepath, arcname=arcname)


def get_file_version(path):
    pe = pefile.PE(path)
    for fileinfo in pe.FileInfo:
        for entry in fileinfo:
            if hasattr(entry, "Key") and entry.Key == b"StringFileInfo":
                for st in entry.StringTable:
                    if b"FileVersion" in st.entries:
                        return st.entries[b"FileVersion"].decode()
    return "0"


def get_spotify_path():
    clear()
    spotify_path = platformdirs.user_data_dir(roaming=True) + "/Spotify"
    with open(maindata) as datfile:
        data = json.load(datfile)
        if not data["path"] == "":
            spotify_path = data["path"]
        if not (
            os.path.exists(f"{spotify_path}/Spotify.exe")
            or os.path.exists(f"{spotify_path}/spotify")
        ):
            not_installed()
            return get_spotify_path()
    return spotify_path


def not_installed():
    global spotify_path
    match operating_system:
        case "Windows":
            print(
                f"Spotify is not detected on this system at [{spotify_path}].\nMake sure you downloaded it from Spotify.com and not the Microsoft Store.\n"
            )
            option_list(["Spotify is installed somewhere else", "Quit"], [None, quit])
        case _:
            print("Failed to find Spotify installation!")
            installed_from = option_list(
                ["APT", "spotify-launcher", "AUR", "Flatpak", "Other"],
                None,
                "\nWhere did you install Spotify from?",
            )
            match installed_from:
                case "APT":
                    print("""
Open a new terminal and run the following commands:

sudo chmod a+wr /usr/share/spotify
sudo chmod a+wr /usr/share/spotify/Apps -R

""")
                    wait()
                    with open(maindata, "r") as datfile:
                        data = json.load(datfile)
                    data["path"] = "/usr/share/spotify"
                    with open(maindata, "w") as datfile:
                        json.dump(data, datfile)
                    return
                case "spotify-launcher":
                    with open(maindata, "r") as datfile:
                        data = json.load(datfile)
                    data["path"] = path.join(
                        platformdirs.user_data_dir("spotify-launcher"),
                        "install/usr/share/spotify",
                    )
                    with open(maindata, "w") as datfile:
                        json.dump(data, datfile)
                    return
                case "AUR":
                    print("""
Open a new terminal and run the following commands:

sudo chmod a+wr /opt/spotify
sudo chmod a+wr /opt/spotify/Apps -R

""")
                    wait()
                    with open(maindata, "r") as datfile:
                        data = json.load(datfile)
                    data["path"] = "/opt/spotify"
                    with open(maindata, "w") as datfile:
                        json.dump(data, datfile)
                    return
                case "Flatpak":
                    print("""
Open a new terminal and run the following commands:

sudo chmod a+wr /var/lib/flatpak/app/com.spotify.Client/x86_64/stable/active/files/extra/share/spotify
sudo chmod a+wr -R /var/lib/flatpak/app/com.spotify.Client/x86_64/stable/active/files/extra/share/spotify/Apps

""")
                    wait()
                    with open(maindata, "r") as datfile:
                        data = json.load(datfile)
                    data["path"] = (
                        "/var/lib/flatpak/app/com.spotify.Client/x86_64/stable/active/files/extra/share/spotify"
                    )
                    with open(maindata, "w") as datfile:
                        json.dump(data, datfile)
                    return
                case "Other":
                    pass
    with open(maindata, "r") as datfile:
        data = json.load(datfile)
    clear()
    print("Please select your Spotify install folder...")
    data["path"] = filedialog.askdirectory(initialdir=platformdirs.user_desktop_dir())
    with open(maindata, "w") as datfile:
        json.dump(data, datfile)


def print_blue(text):
    print(f"{Fore.BLUE}{text}{Fore.GREEN}")


def print_pink(text):
    print(f"{Fore.MAGENTA}{text}{Fore.GREEN}")


def print_yellow(text):
    print(f"{Fore.YELLOW}{text}{Fore.GREEN}")


def print_red(text):
    print(f"{Fore.RED}{text}{Fore.GREEN}")


def option_list(itemlist, calllist=None, prompt_text="Please choose an option:"):
    offset = 0
    print(f"{Fore.BLUE}{prompt_text}{Fore.GREEN}")
    for item in itemlist:
        if item == "SPACER":
            print("")
            offset -= 1
        elif item is not None:
            print(f"{itemlist.index(item) + 1 + offset}) {item}")
    while True:
        key = input("\n[?]: ")
        if int(key) <= len(itemlist) + offset and not int(key) == 0:
            if calllist is not None:
                if calllist[int(key) - 1] is not None:
                    calllist[int(key) - 1]()
                else:
                    return itemlist[int(key) - 1]
                break
            else:
                return itemlist[int(key) - 1]


def wait():
    print(f"{Fore.MAGENTA}Press any key to continue...", end="", flush=True)

    try:
        # Windows
        import msvcrt

        msvcrt.getch()
    except ImportError:
        # Unix (Linux/macOS)
        import termios
        import tty

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)

        try:
            tty.setraw(fd)
            sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    print()
