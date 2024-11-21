# SpotMod - A simple mod injector for Spotify
SpotMod is a very simple tool that will allow you to inject JavaScript (and more in the future) into Spotify.<br><br>
SpotMod is very early in development, and many features are planned for the future.

## Features
🟩 - Implemented<br>
🟨 - Implemented, not tested<br>
🟧 - Planned for the future

Feature|Status|Notes
-|:-:|-:
Windows support | 🟩 
Mac/Linux support | 🟧 | May not be added for a while...
Inject JS into render process | 🟩
Inject CSS into render process | 🟧 | Coming in the next few updates
Modify existing JS | 🟧
Modify existing CSS | 🟧
Modify image files and resources | 🟧
Re-patch Spotify | 🟩 | Adds mods back after Spotify updates

## Usage
To run the tool, download the source code and install the requirements with pip, then run `main.py`.

## Updating
To update SpotMod, uninstall the old patch and install the new one with the new injector.
__Do not just use the "Re-patch" option in the new injector. That is for when Spotify updates, not SpotMod!__