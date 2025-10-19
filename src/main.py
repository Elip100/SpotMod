from tkinter import filedialog
from functools import partial
import os, keyboard, inject, json, time, platformdirs, sys, utils, webbrowser, updater
from colorama import Fore

spotify_path = platformdirs.user_data_dir(roaming=True) + "/Spotify"

def main():
    global spotify_path
    utils.clear()
    if not utils.operating_system == "Windows":
        option_list(["Quit", "Continue anyways (good luck)"], [quit, None], "At the moment, SpotMod only supports Windows.\nMac/Linux support is coming in the (distant) future.\n")
        utils.clear()
    updater.update()
    data = json.load(open(utils.maindata))
    if not data["path"] == "": spotify_path = data["path"]
    if not os.path.exists(f"{spotify_path}/Spotify.exe"):
        not_installed()
    loader_version = inject.get_spotmod_version(spotify_path)
    utils.clear()
    if loader_version is None:
        not_detected()
    if loader_version != utils.version:
        loader_update_required()
    main_menu()

def main_menu():
    update_available = utils.check_for_update()
    while True:
        utils.clear()
        option_list(
            ["Add mod", "Manage mods", "Manage backups", "SPACER", "Uninstall SpotMod", "Quit",
                f"{Fore.BLUE}Update SpotMod Injector{Fore.GREEN}" if update_available else None],
            [add_mod, manage_mods, manage_backups, uninstall, quit,
                partial(webbrowser.open, "https://github.com/Elip100/SpotMod/releases") if update_available else None]
        )

def add_mod():
    utils.clear()
    print("Please select your mod file...")
    mod_file = filedialog.askopenfilename(filetypes=[("Mod Files", "*.js *.css")])
    if mod_file:
        inject.add_mod(mod_file, spotify_path)

def manage_mods():
    while True:
        utils.clear()
        mod_ids = []
        data = json.load(open(f"{utils.datfolder}/data.json", "r"))
        for mod in data["mods"]:
            mod_ids.append(mod["id"])
        mod_ids.append("SPACER")
        mod_ids.append("Cancel")
        mod_id = option_list(mod_ids, None, "Select a mod:")
        if mod_id == "SPACER": return

        utils.clear()
        mod_enabled = data["mods"][mod_ids.index(mod_id)]["enabled"]
        mod_option = option_list(["Disable mod" if mod_enabled else "Enable mod", "Remove mod", "SPACER", "Cancel"])

        match mod_option:
            case "Disable mod":
                inject.toggle_mod(mod_id, mod_ids, spotify_path, False)
            case "Enable mod":
                inject.toggle_mod(mod_id, mod_ids, spotify_path, True)
            case "Remove mod":
                inject.remove_mod(mod_id, mod_ids, spotify_path)
            case _:
                pass

def manage_backups():
    pass

def not_detected():
    print("SpotMod is not detected on this system.\n")
    option_list(["Patch Spotify", "Quit"], [None, quit])
    if len(json.load(open(f"{utils.datfolder}/data.json", "r"))["mods"]) > 0:
        utils.clear()
        option_list(["Install saved mods", "Delete saved mods"], [patch, partial(patch, True)], "You have mods saved. Would you like to install them?")
    else:
        patch()

def not_installed():
    global spotify_path
    print(f"Spotify is not detected on this system at [{spotify_path}].\nMake sure you downloaded it from Spotify.com and not the Microsoft Store.\n")
    option_list(["Spotify is installed somewhere else", "Quit"], [None, quit])
    data = json.load(open("data.json"))
    utils.clear()
    print("Please select your Spotify install folder...")
    data["path"] = filedialog.askdirectory(initialdir=os.getenv("APPDATA"))
    json.dump(data, open("data.json", "w"))
    main()

def loader_update_required():
    option_list(["Update", "Quit"], [None, quit], "The SpotMod loader is out of date.\n")
    inject.unpatch_spotify(spotify_path, False, False)
    inject.patch_spotify(spotify_path, False)

def patch(delete_data = False):
    inject.patch_spotify(spotify_path, delete_data)
    main()

def uninstall():
    utils.clear()
    option_list(["Yes.", "No! Take me back!"], [None, main_menu], "Are you sure you wish to un-patch Spotify and remove all mods?")
    utils.clear()
    option_list(
        ["Yes, keep them.", "No, delete them. (PERMANENT)", "Cancel"],
        [
            partial(inject.unpatch_spotify, spotify_path, False),
            partial(inject.unpatch_spotify, spotify_path, True),
            main_menu
        ],
        "Do you want to keep your mods saved with the Injector so you can restore them in the future?"
    )

def option_list(itemlist, calllist = None, prompt_text = "Please choose an option:"):
    offset = 0
    print(f"{Fore.BLUE}{prompt_text}{Fore.GREEN}")
    for item in itemlist:
        if item == "SPACER":
            print("")
            offset -= 1
        elif item is not None:
            print(f"{itemlist.index(item) + 1 + offset}) {item}")
    while True:
        wait_for_no_keys()
        key = keyboard.read_event().name
        keyboard.send("Backspace")
        keyboard.send("Backspace") # idk, it only works when you do it twice
        if key.isdigit():
            if int(key) <= len(itemlist) + offset and not int(key) == 0:
                if calllist is not None:
                    if calllist[int(key) - 1] is not None:
                        calllist[int(key) - 1]()
                    else:
                        return itemlist[int(key) - 1]
                    break
                else:
                    return itemlist[int(key) - 1]

def wait_for_no_keys():
    while True:
        if not any(keyboard.is_pressed(scan_code) for scan_code in range(1, 256)): # There has to be a more efficient way to do this...
            break
        time.sleep(0.1)

def quit():
    sys.exit()

if __name__ == "__main__":
    main()