# SpotMod - A simple mod injector for Spotify
SpotMod is a simple tool that allows you to inject JavaScript and CSS into Spotify.<br><br>
SpotMod is very early in development, and many features are planned for the future.

## Features
🟩 - Implemented<br>
🟨 - Experimental<br>
🟥 - Planned for the future

Feature|Status|Notes
:-|:-:|-:
Windows support | 🟩 | Binaries can be found [here](https://github.com/Elip100/SpotMod/releases)
Mac/Linux support | 🟥 | May not be added for a while...
Inject JS into render process | 🟩
Inject CSS into render process | 🟨 | Styles may be overridden
Modify existing JS | 🟥
Modify existing CSS | 🟥
Modify image files and resources | 🟥

## Usage
To use the tool, download the latest version [here](https://github.com/Elip100/SpotMod/releases) and run it (Windows only). Spotify must have been downloaded from the Spotify website (not the Microsoft Store). If you installed Spotify from the Microsoft Store, uninstall it and click "Download directly from Spotify" on [this page](https://www.spotify.com/download/windows/).

## Updating
To update SpotMod, [download the new injector EXE file](https://github.com/Elip100/SpotMod/releases) and run it. As soon as you open the new injector, you will be prompted to update the loader. Choose yes and it will automatically update while keeping all of your mods. *__Some versions require different steps when updating, so make sure to check the release description for details.__*

## Building
To build the injector from the source, clone the repo and install the requirements with `pip install -r requirements.txt`. Then, from the root directory of the project, build it with `pyinstaller "SpotMod Injector.spec"`. You will find the executable in the `dist` folder.