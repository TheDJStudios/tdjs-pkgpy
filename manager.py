import os
from pathlib import Path
import requests
import json
import tkinter as tk
from urllib.request import urlopen
import subprocess
import sys
from importlib.metadata import version, PackageNotFoundError



"""
WARNING!
This package manager does not check the file hash of the downloaded file.
We recommend you use our URL from below (Go to https://github.com/TheDJStudios/tdjs-pkgpy/ to request your library get added)
"""


url = "https://thedjstudios.github.io/tdjs-pkgpy/"

directory = json.loads(requests.get(
    f"{url}directory.json"
).text)

cachedir = Path(".pkgPy") / "cache"
def library_installed(package_name: str) -> tuple[bool, str]:
    try:
        return True, version(package_name)
    except PackageNotFoundError:
        return False, ""
root = tk.Tk()
root.title("pkgPy Manager")
root.geometry("300x600")


def download(verdir: str):
    with urlopen(url) as response:
        data = response.read()

    with open(cachedir / verdir, "wb") as file:
        file.write(data)
def install(verdir:str):
    subprocess.check_call([
        sys.executable,
        "-m",
        "pip",
        "install",
        str(cachedir / verdir)
    ])

def downnin(verdir:str):
    download(verdir)
    install(verdir)

for num, package in enumerate(directory):
    pack = directory[package]
    tk.Label(text=f"{package}={pack["latest"]}").grid(column=0, row=num*6, padx=5, pady=5)
    packlen = 0
    for ver in pack:
        packlen += 1
    print(packlen)
    for i, (vers, location) in enumerate(pack.items()):
        instaled = library_installed(package)
        if i >= 5:
            break
        a = ""
        tk.Label(text=vers).grid(column=0, row=(num*1)+(i+1), padx=5, pady=1)
        if vers == "latest":
            tk.Label(text=pack[vers]).grid(column=1, row=(num * 1) + (i + 1), padx=5, pady=1)
            a = pack[vers]
        else:
            a = vers

        dbtn = tk.Button(root, text="Install", command=lambda loc=a: downnin(loc))
        dbtn.config(state="normal" if not instaled else "disabled")
        dbtn.grid(column=2, row=(num*1)+(i+1), padx=5, pady=1)





root.mainloop()