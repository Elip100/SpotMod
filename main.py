from urllib.request import urlretrieve
from colorama import Fore, Style, Back
from tkinter import filedialog
from functools import partial
import os, keyboard, inject, json, time, platform, platformdirs

version = 0.1

spotify_path = platformdirs.user_data_dir(roaming=True) + "\Spotify"

operating_system = platform.system()

def clear():
    os.system("cls" if operating_system == "Windows" else "clear")
    print(f"{Back.GREEN}{Fore.BLACK} SpotMod Patcher v{str(version)} {Style.RESET_ALL}{Fore.GREEN}\n")

def main():
    global spotify_path
    clear()
    data = json.load(open("data.json"))
    if not data["path"] == "": spotify_path = data["path"]
    if not os.path.exists(f"{spotify_path}/Spotify.exe"):
        not_installed()
    if not os.path.exists(f"{spotify_path}/SpotMod.txt"):
        not_detected()
    main_menu()

def main_menu():
    while True:
        clear()
        option_list(["Add mod", "Manage mods", "Uninstall SpotMod", "Quit"], [add_mod, manage_mods, uninstall, quit])

def add_mod():
    clear()
    print("Please select your mod file...")
    mod_file = filedialog.askopenfilename(filetypes=[("JavaScript Files", "*.js")])
    if mod_file:
        clear()
        inject.add_mod(mod_file, spotify_path)

def manage_mods():
    while True:
        clear()
        mod_ids = []
        data = json.load(open("SpotMod-dat/data.json", "r"))
        for mod in data["mods"]:
            mod_ids.append(mod["id"])
        mod_ids.append("Cancel")
        mod_id = option_list(mod_ids, None, "Select a mod:")
        if mod_id == "Cancel": return

        clear()
        mod_enabled = data["mods"][mod_ids.index(mod_id)]["enabled"]
        mod_option = option_list(["Disable mod" if mod_enabled else "Enable mod", "Remove mod", "Cancel"])

        clear()
        match mod_option:
            case "Disable mod":
                inject.enable_mod(mod_id, mod_ids, spotify_path, False)
            case "Enable mod":
                inject.enable_mod(mod_id, mod_ids, spotify_path, True)
            case "Remove mod":
                inject.remove_mod(mod_id, mod_ids, spotify_path)
            case _:
                pass

def not_detected():
    if len(os.listdir("SpotMod-dat/mods")) == 0:
        print("SpotMod is not detected on this system.\n")
        option_list(["Patch Spotify", "Quit"], [patch, quit])
    else:
        print("SpotMod is not detected on this system, but you have saved mods.\n")
        patch_and_del = partial(patch, True)
        option_list(["Patch Spotify and add saved mods", "Patch Spotify and delete saved mods", "Quit"], [patch, patch_and_del, quit])

def not_installed():
    global spotify_path
    print(f"Spotify is not detected on this system at [{spotify_path}].\nMake sure you downloaded it from Spotify.com and not the Microsoft Store.\n")
    option_list(["Spotify is installed somewhere else", "Quit"], [None, quit])
    data = json.load(open("data.json"))
    clear()
    print("Please select your Spotify install folder...")
    data["path"] = filedialog.askdirectory(initialdir=os.getenv("APPDATA"))
    json.dump(data, open("data.json", "w"))
    main()

def patch(delete_data = False):
    clear()
    inject.patch_spotify(spotify_path, delete_data)
    main()

def uninstall():
    clear()
    option_list(["Yes. Remove all my mods.", "No! Take me back!"], [None, main_menu], "Are you sure you wish to un-patch Spotify and remove all mods?")
    clear()
    inject.unpatch_spotify(spotify_path)

def option_list(itemlist, calllist = None, prompt_text = "Please choose an option:"):
    print(prompt_text)
    for item in itemlist:
        print(f"{itemlist.index(item) + 1}) {item}")
    while True:
        wait_for_no_keys()
        key = keyboard.read_event().name
        keyboard.send("Backspace")
        keyboard.send("Backspace") # idk, it only works when you do it twice
        if key.isdigit():
            if int(key) <= len(itemlist) and not int(key) == 0:
                if calllist is not None:
                    if calllist[int(key) - 1] is not None: calllist[int(key) - 1]()
                    break
                else:
                    return itemlist[int(key) - 1]

def wait_for_no_keys():
    while True:
        if not any(keyboard.is_pressed(scan_code) for scan_code in range(1, 256)): # There has to be a better way to do this...
            break
        time.sleep(0.1)

if __name__ == "__main__":
    main()