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
Inject JS into CEF | 🟩
Inject CSS into CEF | 🟨 | Styles may be overridden
Modify existing JS | 🟥
Modify image files and other resources | 🟥

## Usage
To use the tool, download the latest version [here](https://github.com/Elip100/SpotMod/releases) and run it (Windows only). Spotify must have been downloaded from the Spotify website (not the Microsoft Store). If you installed Spotify from the Microsoft Store, uninstall it and click "Download directly from Spotify" on [this page](https://www.spotify.com/download/windows/).

## Updating
To update SpotMod, [download the new injector EXE file](https://github.com/Elip100/SpotMod/releases) and run it. As soon as you open the new injector, you will be prompted to update the loader. Choose yes and it will automatically update while keeping all of your mods. *__Some versions require different steps when updating, so make sure to check the release description for details.__*

## Building
To build the injector from source, clone the repo. As of version 0.5, SpotMod uses uv to manage and install Python dependencies — uv must be installed on your system before proceeding. If uv is not installed, install it using your preferred method (for example, `pip install uv` or your system package manager).

From the root directory of the project, sync the requirements with:
```
uv sync
```
After dependencies are installed, build the injector with:
```
pyinstaller "SpotMod Injector.spec"
```
You will find the executable in the `dist` folder.
