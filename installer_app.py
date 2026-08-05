import os
import shutil
import sys
import tkinter as tk
from tkinter import messagebox

APP_NAME = "CryptoProg"


def get_resource_path(relative_path: str) -> str:
    search_roots = []
    if getattr(sys, "frozen", False):
        search_roots.extend([
            os.path.dirname(os.path.abspath(sys.executable)),
            os.path.dirname(os.path.abspath(sys.argv[0])),
            sys._MEIPASS,
            os.getcwd(),
        ])
    else:
        search_roots.extend([
            os.path.dirname(os.path.abspath(__file__)),
            os.getcwd(),
        ])

    for base_path in search_roots:
        candidate = os.path.join(base_path, relative_path)
        if os.path.exists(candidate):
            return candidate

    return os.path.join(search_roots[0], relative_path)


def install_app() -> None:
    source_exe = get_resource_path("CryptoProg.exe")
    if not os.path.exists(source_exe):
        messagebox.showerror("Installation impossible", "Le fichier d'application n'a pas été trouvé dans l'installateur.")
        return

    install_dir = os.path.join(os.environ.get("LOCALAPPDATA", os.path.expanduser(r"~\AppData\Local")), "Programs", APP_NAME)
    os.makedirs(install_dir, exist_ok=True)

    destination_exe = os.path.join(install_dir, "CryptoProg.exe")
    shutil.copy2(source_exe, destination_exe)

    desktop_dir = os.path.join(os.path.expanduser("~"), "Desktop")
    os.makedirs(desktop_dir, exist_ok=True)
    desktop_exe = os.path.join(desktop_dir, "CryptoProg.exe")
    if not os.path.exists(desktop_exe):
        shutil.copy2(source_exe, desktop_exe)

    messagebox.showinfo(
        "Installation terminée",
        f"CryptoProg a été installé dans :\n{install_dir}\n\nUne copie a aussi été placée sur le bureau."
    )


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    install_app()
    root.destroy()
