# Contributing
To contribute, fork this repo and make a pull request with changes.

## Building from source
To build the injector from source, clone the repo. As of version 0.5, SpotMod uses uv to manage and install Python dependencies. It must be installed on your system before proceeding. If uv is not installed, install it using your preferred method (for example, `pip install uv` or your system package manager).

From the root directory of the project, sync the requirements with:
```
uv sync
```
After dependencies are installed, build the injector with:
```
uv run build.py
```
On Windows, this will generate an EXE file. On Linux, it will generate a binary, an AppImage, a flatpak, and a deb file if you're on Debian.
