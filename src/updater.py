import utils, shutil, os, json

def update():
    if os.path.exists("SpotMod-dat"):
        update__0_4()
    elif not os.path.exists(utils.sm_appdata):
        create_sm_appdata()
    
    data: dict = json.load(open(utils.maindata))
    
    data["version"] = utils.version
    json.dump(data, open(utils.maindata, "w"))

def update__0_4():
    shutil.move("SpotMod-dat", utils.datfolder)
    shutil.move("data.json", utils.maindata)

def create_sm_appdata():
    shutil.copytree(utils.defdat, utils.sm_appdata)