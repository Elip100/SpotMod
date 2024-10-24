import zipfile as zf
import os, shutil, json, keyboard
from bs4 import BeautifulSoup
from time import sleep

def patch_spotify(spotify_path, delete_data = False):
    if delete_data:
        delete_local_files()

    extract_xpui(spotify_path)

    replace_spotmod_dat()
    open(f"{spotify_path}/SpotMod.txt", "w").write("This file tells SpotMod that you have patched Spotify.")

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

    print("Patch applied!\nPress enter to continue...")
    keyboard.wait("Enter")

def unpatch_spotify(spotify_path):
    extract_xpui(spotify_path)
    
    print("Undoing modifications...")

    shutil.rmtree("xpui-spa/SpotMod-dat")
    os.remove(f"{spotify_path}/SpotMod.txt")

    soup = BeautifulSoup(open("xpui-spa/index.html"), features="lxml")
    soup.find("script", {"src": "SpotMod-dat/loader.js"}).decompose()
    soup.find("script", {"src": "https://cdn.jsdelivr.net/npm/toastify-js"}).decompose()
    soup.find("link", {"href": "https://cdn.jsdelivr.net/npm/toastify-js/src/toastify.min.css"}).decompose()
    open("xpui-spa/index.html", "wb").write(soup.prettify("utf-8"))

    compile_xpui(spotify_path)
    delete_local_files()
    clean_up()

    print("SpotMod has been uninstalled.\nPress enter to quit...")
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
    shutil.rmtree("xpui-spa")
    os.remove("xpui.spa")

def add_mod(mod_path, spotify_path):
    mod_id = os.path.basename(mod_path)
    if os.path.exists(f"SpotMod-dat/mods/{mod_id}"):
        print("Duplicate mod detected!\nProcess aborted.")
    else:
        print("Copying mod file...")
        shutil.copyfile(mod_path, f"SpotMod-dat/mods/{mod_id}")
        print("Editing data.json...")
        data = json.load(open("SpotMod-dat/data.json"))
        data["mods"].append({"id": mod_id, "enabled": True})
        open("SpotMod-dat/data.json", "w").write(json.dumps(data))
        extract_xpui(spotify_path)
        replace_spotmod_dat()
        compile_xpui(spotify_path)
        clean_up()
        print("Mod added!")
    print("Press enter to continue...")
    keyboard.wait("Enter")

def remove_mod(mod_id, mod_ids, spotify_path):
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

def enable_mod(mod_id, mod_ids, spotify_path, enable = True):
    print("Editing data.json...")
    data = json.load(open("SpotMod-dat/data.json"))
    mod_data = data["mods"][mod_ids.index(mod_id)]
    mod_data["enabled"] = enable
    open("SpotMod-dat/data.json", "w").write(json.dumps(data))
    extract_xpui(spotify_path)
    replace_spotmod_dat()
    compile_xpui(spotify_path)
    clean_up()