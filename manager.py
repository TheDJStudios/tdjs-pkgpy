import os
from pathlib import Path
import requests
import json


directory = json.loads(requests.get(
    "https://thedjstudios.github.io/tdjs-pkgpy/directory.json"
).text)

for package in directory:
    print(f"")