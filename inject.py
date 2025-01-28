import zipfile as zf
from bs4 import BeautifulSoup
from time import sleep
from colorama import Fore, Style, Back
import os, shutil, json, keyboard, sys, pathlib, utils


def print_blue(text):
    print(f"{Fore.BLUE}{text}{Fore.GREEN}")
def print_pink(text):
    print(f"{Fore.MAGENTA}{text}{Fore.GREEN}")


def patch_spotify(spotify_path, delete_data = False):
    utils.clear()
    print_blue("Patching Spotify...")

    if delete_data:
        delete_local_files()

    extract_xpui(spotify_path)

    replace_spotmod_dat()

    data = json.load(open("SpotMod-dat/data.json"))
    data["version"] = utils.version
    json.dump(data, open(f"SpotMod-dat/data.json", "w"))

    print("Adding JavaScript libraries...")
    soup = BeautifulSoup(open("xpui-spa/index.html"), features="lxml")
    soup.head.append(soup.new_tag("script", src="https://cdn.jsdelivr.net/npm/toastify-js"))
    soup.head.append(soup.new_tag("link", rel="stylesheet", href="https://cdn.jsdelivr.net/npm/toastify-js/src/toastify.min.css"))

    print("Linking loader.js to HTML...")
    soup.body.append(soup.new_tag("script", id="spotmod-patch", src=f"SpotMod-dat/loader.js"))
    html = soup.prettify("utf-8")
    with open("xpui-spa/index.html", "wb") as index:
        index.write(html)

    compile_xpui(spotify_path)

    clean_up()

    print_pink("Patch applied!\nPress enter to continue...")
    keyboard.wait("Enter")

def unpatch_spotify(spotify_path, delete_data = True, quit_after = True):
    utils.clear()
    print_blue("Uninstalling SpotMod...")

    extract_xpui(spotify_path)
    
    print("Undoing modifications...")

    shutil.rmtree("xpui-spa/SpotMod-dat")
    if os.path.exists(f"{spotify_path}/SpotMod.txt"): os.remove(f"{spotify_path}/SpotMod.txt")

    soup = BeautifulSoup(open("xpui-spa/index.html"), features="lxml")
    soup.find("script", {"src": "SpotMod-dat/loader.js"}).decompose()
    soup.find("script", {"src": "https://cdn.jsdelivr.net/npm/toastify-js"}).decompose()
    soup.find("link", {"href": "https://cdn.jsdelivr.net/npm/toastify-js/src/toastify.min.css"}).decompose()
    open("xpui-spa/index.html", "wb").write(soup.prettify("utf-8"))

    compile_xpui(spotify_path)
    if delete_data: delete_local_files()
    clean_up()

    if quit_after:
        print_pink("SpotMod has been uninstalled.\nPress enter to quit...")
        keyboard.wait("Enter")
        quit()

def delete_local_files():
    print("Deleting local files...")
    shutil.rmtree("SpotMod-dat/mods")
    os.mkdir("SpotMod-dat/mods")
    open(f"SpotMod-dat/data.json", "w").write(json.dumps({"mods": []}))

def extract_xpui(spotify_path):
    print("Extracting xpui.spa...")
    with zf.ZipFile(f"{spotify_path}/apps/xpui.spa", "r") as spa_file:
        spa_file.extractall("xpui-spa")
        spa_file.close()

def compile_xpui(spotify_path):
    print("Compiling new xpui.spa...")
    with zf.ZipFile("xpui.spa", 'w') as spa_file:
        for root, _, files in os.walk("xpui-spa"):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, "xpui-spa")
                spa_file.write(file_path, arcname)
        spa_file.close()
    print("Replacing old xpui.spa...")
    os.remove(f"{spotify_path}/apps/xpui.spa")
    shutil.copyfile("xpui.spa", f"{spotify_path}/apps/xpui.spa")

def replace_spotmod_dat():
    print("Adding/Replacing SpotMod files and folders...")
    if os.path.exists("xpui-spa/SpotMod-dat"):
        shutil.rmtree("xpui-spa/SpotMod-dat")
    shutil.copytree("SpotMod-dat", "xpui-spa/SpotMod-dat")

def clean_up():
    print("Cleaning up...")
    try:
        shutil.rmtree("xpui-spa")
        os.remove("xpui.spa")
    except:
        pass

def add_mod(mod_path, spotify_path):
    utils.clear()
    mod_id = os.path.basename(mod_path)
    print_blue(f"Adding mod: {mod_id}...")

    if os.path.exists(f"SpotMod-dat/mods/{mod_id}"):
        print("Duplicate mod detected!\nProcess aborted.")
    else:
        print("Copying mod file...")
        shutil.copyfile(mod_path, f"SpotMod-dat/mods/{mod_id}")
        print("Editing data.json...")
        data = json.load(open("SpotMod-dat/data.json"))
        data["mods"].append({"id": mod_id, "type": pathlib.Path(mod_path).suffix, "enabled": True})
        open("SpotMod-dat/data.json", "w").write(json.dumps(data))
        extract_xpui(spotify_path)
        replace_spotmod_dat()
        compile_xpui(spotify_path)
        clean_up()
        print_pink("Mod added!")
    print_pink("Press enter to continue...")
    keyboard.wait("Enter")

def remove_mod(mod_id, mod_ids, spotify_path):
    utils.clear()
    print_blue(f"Removing mod: {mod_id}...")

    print("Editing data.json...")
    data = json.load(open("SpotMod-dat/data.json"))
    data["mods"].pop(mod_ids.index(mod_id))
    open("SpotMod-dat/data.json", "w").write(json.dumps(data))

    print("Deleting mod file...")
    os.remove(f"SpotMod-dat/mods/{mod_id}")
    
    extract_xpui(spotify_path)
    replace_spotmod_dat()
    compile_xpui(spotify_path)
    clean_up()

def toggle_mod(mod_id, mod_ids, spotify_path, enable = True):
    utils.clear()
    print_blue(f"Toggling mod: {mod_id}...")

    print("Editing data.json...")
    data = json.load(open("SpotMod-dat/data.json"))
    mod_data = data["mods"][mod_ids.index(mod_id)]
    mod_data["enabled"] = enable
    open("SpotMod-dat/data.json", "w").write(json.dumps(data))
    extract_xpui(spotify_path)
    replace_spotmod_dat()
    compile_xpui(spotify_path)
    clean_up()

def get_spotmod_version(spotify_path):
    if os.path.exists(f"{spotify_path}/SpotMod.txt"):
        return 0.2
    extract_xpui(spotify_path)
    if os.path.exists("xpui-spa/SpotMod-dat"):
        data = json.load(open("xpui-spa/SpotMod-dat/data.json"))["version"]
        clean_up()
        return data
    else:
        clean_up()
        return None

def quit():
    sys.exit()