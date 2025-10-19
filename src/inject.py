import zipfile as zf
from bs4 import BeautifulSoup
from time import sleep
from colorama import Fore, Style, Back
from tempfile import TemporaryDirectory
from updater import create_sm_appdata
from datetime import datetime
import os, shutil, json, sys, pathlib, utils, uuid


def print_blue(text):
    print(f"{Fore.BLUE}{text}{Fore.GREEN}")
def print_pink(text):
    print(f"{Fore.MAGENTA}{text}{Fore.GREEN}")
def wait():
    print(Fore.MAGENTA, end="", flush=True)
    os.system("pause")

def patch_spotify(spotify_path, delete_data = False):
    utils.clear()
    print_blue("Patching Spotify...")

    if delete_data:
        delete_local_files()

    with TemporaryDirectory() as temp_dir:
        extract_xpui(spotify_path, f"{temp_dir}/xpui-spa")

        data = json.load(open(f"{utils.datfolder}/data.json"))
        data["version"] = utils.version
        json.dump(data, open(f"{utils.datfolder}/data.json", "w"))

        replace_spotmod_dat(temp_dir)

        print("Adding JavaScript libraries...")
        soup = BeautifulSoup(open(f"{temp_dir}/xpui-spa/index.html"), features="lxml")
        soup.head.append(soup.new_tag("script", src="https://cdn.jsdelivr.net/npm/toastify-js"))
        soup.head.append(soup.new_tag("link", rel="stylesheet", href="https://cdn.jsdelivr.net/npm/toastify-js/src/toastify.min.css"))

        print("Linking loader.js to HTML...")
        soup.body.append(soup.new_tag("script", id="spotmod-patch", src="SpotMod-dat/loader.js"))
        html = soup.prettify("utf-8")
        with open(f"{temp_dir}/xpui-spa/index.html", "wb") as index:
            index.write(html)

        compile_xpui(spotify_path, temp_dir)

    print_pink("Patch applied!")
    wait()

def unpatch_spotify(spotify_path, delete_data = True, quit_after = True):
    utils.clear()
    print_blue("Uninstalling SpotMod...")

    with TemporaryDirectory() as temp_dir:
        extract_xpui(spotify_path, f"{temp_dir}/xpui-spa")
        
        print("Undoing modifications...")

        shutil.rmtree(f"{temp_dir}/xpui-spa/SpotMod-dat")
        if os.path.exists(f"{spotify_path}/SpotMod.txt"): os.remove(f"{spotify_path}/SpotMod.txt")

        soup = BeautifulSoup(open(f"{temp_dir}/xpui-spa/index.html"), features="lxml")
        soup.find("script", {"src": "SpotMod-dat/loader.js"}).decompose()
        soup.find("script", {"src": "https://cdn.jsdelivr.net/npm/toastify-js"}).decompose()
        soup.find("link", {"href": "https://cdn.jsdelivr.net/npm/toastify-js/src/toastify.min.css"}).decompose()
        open(f"{temp_dir}/xpui-spa/index.html", "wb").write(soup.prettify("utf-8"))

        compile_xpui(spotify_path, temp_dir)
    if delete_data: delete_local_files()

    if quit_after:
        print_pink("SpotMod has been uninstalled.")
        wait()
        quit()

def delete_local_files():
    print("Deleting local files...")
    shutil.rmtree(utils.sm_appdata)
    create_sm_appdata()

def extract_xpui(spotify_path, dest_dir = "xpui-spa"):
    if detect_spiceify(spotify_path):
        print("Copying xpui...")
        if os.path.exists(dest_dir):
            shutil.rmtree(dest_dir)
        shutil.copytree(f"{spotify_path}/apps/xpui", dest_dir)
    else:
        print("Extracting xpui.spa...")
        with zf.ZipFile(f"{spotify_path}/apps/xpui.spa", "r") as spa_file:
            spa_file.extractall(dest_dir)
            spa_file.close()

def compile_xpui(spotify_path, tmp_dir = os.getcwd()):
    if detect_spiceify(spotify_path):
        print("Replacing xpui...")
        shutil.rmtree(f"{spotify_path}/apps/xpui")
        shutil.copytree(f"{tmp_dir}/xpui-spa", f"{spotify_path}/apps/xpui")
    else:
        print("Compiling new xpui.spa...")
        utils.zip_directory(f"{tmp_dir}/xpui-spa", f"{tmp_dir}/xpui.spa")
        print("Replacing old xpui.spa...")
        os.remove(f"{spotify_path}/apps/xpui.spa")
        shutil.copyfile(f"{tmp_dir}/xpui.spa", f"{spotify_path}/apps/xpui.spa")

def replace_spotmod_dat(tmp_dir = os.getcwd()):
    print("Adding/Replacing SpotMod files and folders...")
    if os.path.exists(f"{tmp_dir}/xpui-spa/SpotMod-dat"):
        shutil.rmtree(f"{tmp_dir}/xpui-spa/SpotMod-dat")
    shutil.copytree(utils.datfolder, f"{tmp_dir}/xpui-spa/SpotMod-dat")

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

    if os.path.exists(f"{utils.datfolder}/mods/{mod_id}"):
        print("Duplicate mod detected!\nProcess aborted.")
    else:
        print("Copying mod file...")
        shutil.copyfile(mod_path, f"{utils.datfolder}/mods/{mod_id}")
        print("Editing data.json...")
        data = json.load(open(f"{utils.datfolder}/data.json"))
        data["mods"].append({"id": mod_id, "type": pathlib.Path(mod_path).suffix, "enabled": True})
        open(f"{utils.datfolder}/data.json", "w").write(json.dumps(data))
        with TemporaryDirectory() as temp_dir:
            extract_xpui(spotify_path, f"{temp_dir}/xpui-spa")
            replace_spotmod_dat(temp_dir)
            compile_xpui(spotify_path, temp_dir)
        print_pink("Mod added!")
    wait()

def remove_mod(mod_id, mod_ids, spotify_path):
    utils.clear()
    print_blue(f"Removing mod: {mod_id}...")

    print("Editing data.json...")
    data = json.load(open(f"{utils.datfolder}/data.json"))
    data["mods"].pop(mod_ids.index(mod_id))
    open(f"{utils.datfolder}/data.json", "w").write(json.dumps(data))

    print("Deleting mod file...")
    os.remove(f"{utils.datfolder}/mods/{mod_id}")
    
    with TemporaryDirectory() as temp_dir:
        extract_xpui(spotify_path, f"{temp_dir}/xpui-spa")
        replace_spotmod_dat(temp_dir)
        compile_xpui(spotify_path, temp_dir)

def toggle_mod(mod_id, mod_ids, spotify_path, enable = True):
    utils.clear()
    print_blue(f"Toggling mod: {mod_id}...")

    print("Editing data.json...")
    data = json.load(open(f"{utils.datfolder}/data.json"))
    mod_data = data["mods"][mod_ids.index(mod_id)]
    mod_data["enabled"] = enable
    open(f"{utils.datfolder}/data.json", "w").write(json.dumps(data))
    with TemporaryDirectory() as temp_dir:
        extract_xpui(spotify_path, f"{temp_dir}/xpui-spa")
        replace_spotmod_dat(temp_dir)
        compile_xpui(spotify_path, temp_dir)

def create_backup(backup_type, modded, spotify_path):
    utils.clear()
    print_blue(f"Creating {backup_type} backup...")

    print("Gathering info...")
    timestamp = datetime.now()
    bak_id = uuid.uuid4()
    bak_ver = utils.get_file_version(os.path.join(spotify_path, "Spotify.exe"))

    print("Copying files...")
    match backup_type:
        case "simple":
            shutil.copyfile(f"{spotify_path}/apps/xpui.spa", os.path.join(utils.backdir, f"{bak_id}.spa.bak"))
        case "full":
            utils.zip_directory(spotify_path, os.path.join(utils.backdir, f"{bak_id}.bak"))
    print("Updating backups.json...")
    backups = json.load(open(utils.backupdata))
    backups.append({
        "type": backup_type,
        "mod": modded,
        "timestamp": str(timestamp),
        "uuid": str(bak_id),
        "ver": utils.version,
        "sver": bak_ver
    })
    json.dump(backups, open(utils.backupdata, "w"))
    print_pink("Backup created!")
    wait()

def restore_backup(backup, spotify_path):
    utils.clear()
    print_blue(f"Restoring backup...")

    print("Removing files...")
    match backup["type"]:
        case "simple":
            os.remove(f"{spotify_path}/apps/xpui.spa")
        case "full":
            shutil.rmtree(spotify_path)
    
    print("Copying files...")
    match backup["type"]:
        case "simple":
            shutil.copyfile(os.path.join(utils.backdir, f"{backup['uuid']}.spa.bak"), f"{spotify_path}/apps/xpui.spa")
        case "full":
            with zf.ZipFile(os.path.join(utils.backdir, f"{backup['uuid']}.bak")) as bak_zip:
                bak_zip.extractall(spotify_path)
                bak_zip.close()
    
    print_pink("Backup restored!")
    wait()

def get_spotmod_version(spotify_path):
    if os.path.exists(f"{spotify_path}/SpotMod.txt"):
        return 0.2
    with TemporaryDirectory() as temp_dir:
        extract_xpui(spotify_path, temp_dir)
        if os.path.exists(f"{temp_dir}/SpotMod-dat"):
            data = json.load(open(f"{temp_dir}/SpotMod-dat/data.json"))["version"]
            return data
        else:
            return None

def detect_spiceify(spotify_path):
    return os.path.exists(f"{spotify_path}/apps/xpui") and not os.path.exists(f"{spotify_path}/apps/xpui.spa")

def quit():
    print(Style.RESET_ALL)
    os.system("cls")
    sys.exit()