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
if not Path(".pkgPy").exists():
    Path(".pkgPy").mkdir()
cachedir = Path(".pkgPy") / "cache"
if not cachedir.exists():
    cachedir.mkdir()
def library_installed(package_name: str) -> tuple[bool, str]:
    try:
        return True, version(package_name)
    except PackageNotFoundError:
        return False, ""
def main():
    root = tk.Tk()
    root.title("pkgPy Manager")
    root.geometry("600x1000")


    def download(verdir: str, pkgname:str):
        print(url+verdir)
        with urlopen(url+verdir) as response:
            data = response.read()

        b = cachedir / "simple"
        if not b.exists():
            b.mkdir()
        c = b / pkgname
        if not c.exists():
            c.mkdir()

        if not Path(verdir.removesuffix(".whl")).exists():
            Path(verdir.removesuffix(".whl")).mkdir()


        a = cachedir / verdir
        a.touch()

        with open(cachedir / verdir, "wb") as file:
            file.write(data)
    def install(verdir:str, pkgname:str):
        subprocess.check_call([
            sys.executable,
            "-m",
            "pip",
            "install",
            str(cachedir / verdir)
        ])
        root.destroy()
        main()

    def downnin(verdir:str, pkgname:str):
        download(verdir, pkgname)
        install(verdir, pkgname)

    for num, package in enumerate(directory):
        pos = num*6
        pack = directory[package]
        tk.Label(text=f"{package}={pack['latest']}").grid(column=0, row=pos, padx=5, pady=5)
        packlen = 0
        for ver in pack:
            packlen += 1
        print(packlen)
        for i, (vers, location) in enumerate(pack.items()):
            installed, ver = library_installed(package)
            if i >= 5:
                break
            a = ""
            tk.Label(text=vers).grid(column=0, row=pos+(i+1), padx=5, pady=1)
            if vers == "latest":
                tk.Label(text=pack[vers]).grid(column=1, row=pos + (i + 1), padx=5, pady=1)
                a = pack[pack[vers]]
                if a == "null" or a is None:
                    installed = True
            else:
                a = location
                if pack[vers] is None or pack[vers] == "null":
                    installed = True

            dbtn = tk.Button(root, text="Install", command=lambda loc=a, nm = package: downnin(loc,nm))
            dbtn.config(state="normal" if not installed else "disabled")
            dbtn.grid(column=2, row=pos+(i+1), padx=5, pady=1)





    root.mainloop()

if __name__ == '__main__':
    main()