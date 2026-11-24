# -*- coding: utf-8 -*-
"""
BTD6 Money Cheat - launcher.
Двойной клик -> сам скачает мод-загрузчик NML, установит его в папку игры
и запустит BTD6 с читом денег (в игре кнопка F8 = +$10 000).
Требования: Windows 10/11 и установленный Python 3 (https://python.org).
"""
import json
import os
import shutil
import subprocess
import sys
import tkinter as tk
import urllib.request
import zipfile
import winreg
from tkinter import filedialog, messagebox

NML_URL = "https://github.com/Natechillton/Mod-Loader/releases/latest/download/BTD6.zip"
HERE = os.path.dirname(os.path.abspath(__file__))
MOD_ZIP = os.path.join(HERE, "MoneyCheat.zip")
CACHE_DIR = os.path.join(HERE, ".cache")


def find_game_dir():
    """Пытаемся найти папку игры через реестр Steam."""
    candidates = []
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam")
        steam_path, _ = winreg.QueryValueEx(key, "SteamPath")
        lib = os.path.join(steam_path, "steamapps", "libraryfolders.vdf")
        roots = [os.path.join(steam_path, "steamapps", "common")]
        if os.path.exists(lib):
            with open(lib, encoding="utf-8", errors="ignore") as f:
                for line in f:
                    if '"path"' in line:
                        p = line.split('"path"')[1].strip().strip('"').replace('\\\\', '\\')
                        roots.append(os.path.join(p, "steamapps", "common"))
        for root in roots:
            for name in ("BloonTDS6", "BloonsTD6", "BTD6"):
                d = os.path.join(root, name)
                if os.path.exists(os.path.join(d, "BloonsTD6.exe")):
                    candidates.append(d)
    except OSError:
        pass
    # типовые пути
    for d in (r"C:\Program Files (x86)\Steam\steamapps\common\BloonTDS6",
              r"C:\Games\BloonTDS6"):
        if os.path.exists(os.path.join(d, "BloonsTD6.exe")) and d not in candidates:
            candidates.append(d)
    return candidates[0] if candidates else None


def ask_dir():
    d = filedialog.askdirectory(title="Выберите папку игры BloonsTD6 (где BloonsTD6.exe)")
    if d and os.path.exists(os.path.join(d, "BloonsTD6.exe")):
        return d
    messagebox.showerror("Ошибка", "В этой папке нет BloonsTD6.exe. Выберите правильную папку.")
    return ask_dir()


def download_nml():
    zip_path = os.path.join(CACHE_DIR, "NML.zip")
    loader_dir = os.path.join(CACHE_DIR, "NML")
    if os.path.exists(os.path.join(loader_dir, "winhttp.dll")):
        return loader_dir
    os.makedirs(CACHE_DIR, exist_ok=True)
    status.config(text="Скачиваю мод-загрузчик NML (~2 МБ)...")
    req = urllib.request.Request(NML_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r, open(zip_path, "wb") as f:
        f.write(r.read())
    with zipfile.ZipFile(zip_path) as z:
        z.extractall(loader_dir)
    return loader_dir


def install(game_dir, loader_dir):
    status.config(text="Устанавливаю в: " + game_dir)
    for fn in os.listdir(loader_dir):
        src = os.path.join(loader_dir, fn)
        dst = os.path.join(game_dir, fn)
        if os.path.isdir(src):
            shutil.copytree(src, dst, dirs_exist_ok=True)
        else:
            shutil.copy2(src, dst)
    mods = os.path.join(game_dir, "Mods")
    os.makedirs(mods, exist_ok=True)
    shutil.copy2(MOD_ZIP, os.path.join(mods, "MoneyCheat.zip"))
    # включаем мод в settings.json NML
    settings = os.path.join(game_dir, "BTDTools", "settings.json")
    try:
        cfg = {}
        if os.path.exists(settings):
            with open(settings, encoding="utf-8") as f:
                cfg = json.load(f)
        enabled = cfg.setdefault("EnabledMods", {})
        enabled["Money Cheat"] = True
        os.makedirs(os.path.dirname(settings), exist_ok=True)
        with open(settings, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2)
    except Exception:
        pass  # если формат другой — включится вручную галочкой в меню модов


def run():
    try:
        game_dir = find_game_dir()
        if not game_dir or not messagebox.askyesno(
                "Папка игры",
                "Найдена папка игры:\n%s\nУстановить мод туда?" % game_dir if game_dir
                else "Папка игры не найдена. Укажите вручную."):
            if not game_dir:
                game_dir = ask_dir()
            else:
                game_dir = ask_dir()
        loader_dir = download_nml()
        install(game_dir, loader_dir)
        status.config(text="Готово! Запускаю игру...")
        subprocess.Popen([os.path.join(game_dir, "BloonsTD6.exe")], cwd=game_dir)
        status.config(text="Игра запущена. В игре нажми F8 = +$10 000.")
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))
        status.config(text="Ошибка. Можно установить вручную (см. README.md).")


root = tk.Tk()
root.title("BTD6 Money Cheat Launcher")
root.geometry("420x140")
tk.Label(root, text="BTD6 Money Cheat", font=("Segoe UI", 14, "bold")).pack(pady=10)
btn = tk.Button(root, text="Установить и запустить", command=run, height=2, width=30)
btn.pack()
status = tk.Label(root, text="Нажми кнопку. Нужен интернет для первой загрузки.", wraplength=400)
status.pack(pady=8)
root.mainloop()
