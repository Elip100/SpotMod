#!/usr/bin/env python3
"""
Build script for SpotMod
Packages the application as:
- Windows: exe using PyInstaller
- Linux: AppImage, Flatpak, and deb (on Debian-based)
"""

import platform
import subprocess
import sys
from pathlib import Path
import urllib.request
import shutil


version_str = "0.5.1"


def get_distro_info():
    """Get distro ID and package manager"""
    try:
        with open("/etc/os-release") as f:
            lines = f.readlines()
        info = {}
        for line in lines:
            if "=" in line:
                key, value = line.strip().split("=", 1)
                info[key] = value.strip('"')
        distro_id = info.get("ID", "").lower()
        id_like = info.get("ID_LIKE", "").lower()
        return distro_id, id_like
    except:
        return "unknown", ""


def get_package_manager(distro_id, id_like):
    """Get package manager command"""
    if distro_id in ["ubuntu", "debian"] or "debian" in id_like:
        return ["sudo", "apt", "update"], ["sudo", "apt", "install", "-y"]
    elif distro_id == "fedora":
        return [], ["sudo", "dnf", "install", "-y"]
    elif distro_id == "arch":
        return [], ["sudo", "pacman", "-S", "--noconfirm"]
    elif distro_id == "opensuse":
        return [], ["sudo", "zypper", "install", "-y"]
    else:
        return [], ["sudo", "apt", "install", "-y"]  # fallback


def run_command(cmd, cwd=None, check=True):
    """Run a shell command"""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"Command failed: {' '.join(cmd)}")
        print(f"stdout: {result.stdout}")
        print(f"stderr: {result.stderr}")
        sys.exit(1)
    return result


def download_appimagetool():
    """Download appimagetool AppImage"""
    build_dir = Path("dist-build")
    build_dir.mkdir(exist_ok=True)
    url = "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
    path = build_dir / "appimagetool.AppImage"
    print(f"Downloading {url}...")
    urllib.request.urlretrieve(url, path)
    path.chmod(0o755)
    return path


def install_package(package, distro_id, id_like):
    """Install package using appropriate package manager"""
    update_cmd, install_cmd = get_package_manager(distro_id, id_like)
    if update_cmd:
        run_command(update_cmd)
    run_command(install_cmd + [package])


def install_if_missing(package, check_cmd, distro_id, id_like):
    """Install package if not present"""
    try:
        subprocess.run(check_cmd, check=True, capture_output=True)
        print(f"{package} is already installed")
    except (subprocess.CalledProcessError, FileNotFoundError):
        if package == "appimagetool":
            download_appimagetool()
        else:
            install_package(package, distro_id, id_like)


def build_windows():
    """Build exe for Windows"""
    print("Building for Windows...")
    build_dir = Path("dist-build")
    build_dir.mkdir(exist_ok=True)
    spec_file = "SpotMod Injector.spec"
    run_command(["pyinstaller", "--distpath", str(build_dir), spec_file])


def build_appimage():
    """Build AppImage for Linux"""
    print("Building AppImage...")

    build_dir = Path("dist-build")
    build_dir.mkdir(exist_ok=True)

    distro_id, id_like = get_distro_info()

    # Build with PyInstaller
    spec_file = "SpotMod Injector.spec"
    run_command(["pyinstaller", "--distpath", str(build_dir), spec_file])

    # Install appimagetool if missing
    install_if_missing(
        "appimagetool",
        [str(build_dir / "appimagetool.AppImage"), "--version"],
        distro_id,
        id_like,
    )

    # Create AppDir structure
    appdir = build_dir / "AppDir"
    appdir.mkdir(exist_ok=True)

    # Copy executable
    exe_src = build_dir / "SpotMod Injector"
    exe_dest = appdir / "SpotMod Injector"
    exe_dest.write_bytes(exe_src.read_bytes())
    exe_dest.chmod(0o755)

    # Create AppRun script
    apprun = """#!/bin/bash
HERE="$(dirname "$(readlink -f "${0}")")"
exec "${HERE}/SpotMod Injector" "$@"
"""
    (appdir / "AppRun").write_text(apprun)
    (appdir / "AppRun").chmod(0o755)

    # Create desktop file
    desktop = """[Desktop Entry]
Name=SpotMod Injector
Exec=SpotMod Injector
Icon=spotmod
Type=Application
Categories=Utility;
Terminal=true
"""
    (appdir / "spotmod.desktop").write_text(desktop)

    # Copy icon
    icon_src = Path("icons/spotmod.png")
    if icon_src.exists():
        (appdir / "spotmod.png").write_bytes(icon_src.read_bytes())

    # Build AppImage
    appimagetool_cmd = (
        [str(build_dir / "appimagetool.AppImage")]
        if (build_dir / "appimagetool.AppImage").exists()
        else ["appimagetool"]
    )
    run_command(appimagetool_cmd + [str(appdir), str(build_dir / "SpotMod.AppImage")])


def build_flatpak():
    """Build Flatpak for Linux"""
    print("Building Flatpak...")

    build_dir = Path("dist-build")
    build_dir.mkdir(exist_ok=True)

    distro_id, id_like = get_distro_info()

    # Install flatpak if missing
    install_if_missing("flatpak", ["flatpak", "--version"], distro_id, id_like)

    # Install flatpak-builder if missing
    install_if_missing(
        "flatpak-builder", ["flatpak-builder", "--version"], distro_id, id_like
    )

    # Install Flatpak runtime and SDK
    run_command(
        [
            "flatpak",
            "install",
            "-y",
            "org.freedesktop.Platform//23.08",
            "org.freedesktop.Sdk//23.08",
        ]
    )

    # Build with PyInstaller
    spec_file = "SpotMod Injector.spec"
    run_command(["pyinstaller", "--distpath", str(build_dir), spec_file])

    # Create manifest
    manifest = {
        "app-id": "io.github.Elip100.SpotMod",
        "runtime": "org.freedesktop.Platform",
        "runtime-version": "23.08",
        "sdk": "org.freedesktop.Sdk",
        "command": "spotmod-injector",
        "modules": [
            {
                "name": "spotmod",
                "buildsystem": "simple",
                "build-commands": [
                    "mkdir -p /app/bin",
                    "mkdir -p /app/share/applications",
                    "cp 'SpotMod Injector' /app/bin/spotmod-injector",
                    "chmod +x /app/bin/spotmod-injector",
                    "mkdir -p /app/share/icons/hicolor/256x256/apps",
                    "cp spotmod.png /app/share/icons/hicolor/256x256/apps/io.github.Elip100.SpotMod.png",
                    "cat > /app/share/applications/io.github.Elip100.SpotMod.desktop <<EOF\n"
                    "[Desktop Entry]\n"
                    "Name=SpotMod Injector\n"
                    "Icon=io.github.Elip100.SpotMod\n"
                    "Exec=spotmod-injector\n"
                    "Terminal=true\n"
                    "Type=Application\n"
                    "Categories=Utility;\n"
                    "EOF",
                ],
                "sources": [
                    {
                        "type": "file",
                        "path": "dist-build/SpotMod Injector",
                    },
                    {"type": "file", "path": "icons/spotmod.png"},
                ],
            }
        ],
        "finish-args": [
            "--share=network",
            "--filesystem=/home",
            "--filesystem=/usr/share/spotify",
            "--filesystem=/opt/spotify",
            "--filesystem=/var/lib/flatpak",
            "--socket=x11",
            "--socket=wayland",
            "--device=dri",
            "--env=TERM=xterm-256color",
        ],
    }

    # Write manifest
    import json

    manifest_path = Path("io.github.Elip100.SpotMod.json")
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)

    # Clean cache
    run_command(["rm", "-rf", ".flatpak-builder"])

    # Build Flatpak
    flatpak_build_dir = build_dir / "flatpak-build"
    repo_dir = build_dir / "flatpak-repo"

    run_command(
        [
            "flatpak-builder",
            "--force-clean",
            "--repo=" + str(repo_dir),
            str(flatpak_build_dir),
            str(manifest_path),
        ]
    )

    # Bundle Flatpak
    run_command(
        [
            "flatpak",
            "build-bundle",
            str(repo_dir),
            str(build_dir / "SpotMod Injector.flatpak"),
            "io.github.Elip100.SpotMod",
        ]
    )


def build_deb():
    """Build deb package for Debian-based systems"""
    print("Building deb package...")

    build_dir = Path("dist-build")
    build_dir.mkdir(exist_ok=True)

    # Build with PyInstaller
    spec_file = "SpotMod Injector.spec"
    run_command(["pyinstaller", "--distpath", str(build_dir), spec_file])

    # Create deb structure
    deb_dir = build_dir / "deb-build"
    if deb_dir.exists():
        shutil.rmtree(deb_dir)
    deb_dir.mkdir()

    pkg_dir = deb_dir / f"spotmod-{version_str}"
    pkg_dir.mkdir()

    # Create DEBIAN directory
    debian_dir = pkg_dir / "DEBIAN"
    debian_dir.mkdir()

    # Create control file
    control = f"""Package: spotmod
Version: {version_str}
Architecture: amd64
Maintainer: Elip100
Description: SpotMod Injector
 A simple tool that allows you to inject JavaScript and CSS into Spotify.
"""
    (debian_dir / "control").write_text(control)

    # Create usr/bin
    bin_dir = pkg_dir / "usr" / "bin"
    bin_dir.mkdir(parents=True)

    # Copy executable
    exe_src = build_dir / "SpotMod Injector"
    exe_dest = bin_dir / "spotmod-injector"
    shutil.copy2(exe_src, exe_dest)
    exe_dest.chmod(0o755)

    # Create usr/share/applications
    apps_dir = pkg_dir / "usr" / "share" / "applications"
    apps_dir.mkdir(parents=True)

    # Create desktop file
    desktop = """[Desktop Entry]
Name=SpotMod Injector
Exec=spotmod-injector
Icon=spotmod
Type=Application
Categories=Utility;
Terminal=true
"""
    (apps_dir / "spotmod-injector.desktop").write_text(desktop)

    # Create usr/share/icons
    icons_dir = pkg_dir / "usr" / "share" / "icons" / "hicolor" / "256x256" / "apps"
    icons_dir.mkdir(parents=True)

    # Copy icon
    icon_src = Path("icons/spotmod.png")
    if icon_src.exists():
        shutil.copy2(icon_src, icons_dir / "spotmod.png")

    # Build deb
    run_command(
        [
            "dpkg-deb",
            "--build",
            str(pkg_dir),
            str(build_dir / f"spotmod_{version_str}_amd64.deb"),
        ]
    )


def main():
    system = platform.system()
    if system == "Windows":
        build_windows()
    elif system == "Linux":
        distro_id, id_like = get_distro_info()
        build_appimage()
        build_flatpak()
        if distro_id in ["ubuntu", "debian"] or "debian" in id_like:
            build_deb()
    else:
        print(f"Unsupported platform: {system}")
        sys.exit(1)


if __name__ == "__main__":
    main()
