import customtkinter as ctk
import os
import json


def _path():
    root = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(root, "settings", "settings.json")


def _ensure():
    p = _path()
    os.makedirs(os.path.dirname(p), exist_ok=True)
    if not os.path.exists(p):
        with open(p, "w", encoding="utf-8") as f:
            json.dump({"appearance": "dark", "theme": "blue"}, f)


def _load():
    try:
        with open(_path(), "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"appearance": "dark", "theme": "blue"}


def _save(s):
    with open(_path(), "w", encoding="utf-8") as f:
        json.dump(s, f, indent=2)


def open_settings(parent):
    _ensure()
    cfg = _load()

    win = ctk.CTkToplevel(parent)
    win.title("Settings")
    win.geometry("400x220")

    frame = ctk.CTkFrame(win)
    frame.pack(fill="both", expand=True, padx=12, pady=12)

    ctk.CTkLabel(frame, text="Appearance Mode:").pack(anchor="w")
    appearance_var = ctk.StringVar(value=cfg.get("appearance", "dark"))
    appearance_menu = ctk.CTkOptionMenu(frame, values=["dark", "light", "system"], variable=appearance_var)
    appearance_menu.pack(fill="x", pady=(0, 8))

    ctk.CTkLabel(frame, text="Color Theme:").pack(anchor="w")
    theme_var = ctk.StringVar(value=cfg.get("theme", "blue"))
    theme_menu = ctk.CTkOptionMenu(frame, values=["blue", "green", "dark-blue"], variable=theme_var)
    theme_menu.pack(fill="x", pady=(0, 8))

    btn_frame = ctk.CTkFrame(frame)
    btn_frame.pack(fill="x", pady=8)


    def apply_settings():
        appearance = appearance_var.get()
        theme = theme_var.get()
        try:
            ctk.set_appearance_mode(appearance)
            ctk.set_default_color_theme(theme)
        except Exception:
            # ignore invalid values
            pass
        cfg["appearance"] = appearance
        cfg["theme"] = theme
        _save(cfg)


    ctk.CTkButton(btn_frame, text="Apply", command=apply_settings).pack(side="right", padx=6)
    ctk.CTkButton(btn_frame, text="Close", command=win.destroy).pack(side="right")

    return win
