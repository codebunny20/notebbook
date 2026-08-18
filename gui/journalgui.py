import customtkinter as ctk
import tkinter as tk
import os
import json
from datetime import datetime


def _data_path():
    root = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(root, "data", "journal.json")


def _ensure_data():
    path = _data_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump([], f)


def _load_entries():
    path = _data_path()
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def _save_entries(entries):
    path = _data_path()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2)


def open_journal(parent):
    _ensure_data()
    entries = _load_entries()

    win = ctk.CTkToplevel(parent)
    win.title("Journal")
    win.geometry("800x500")

    left = ctk.CTkFrame(win)
    left.pack(side="left", fill="y", padx=8, pady=8)

    right = ctk.CTkFrame(win)
    right.pack(side="right", fill="both", expand=True, padx=8, pady=8)

    tk.Label(left, text="Entries").pack()
    listbox = tk.Listbox(left, width=30)
    listbox.pack(fill="y", expand=True)

    def _refresh():
        listbox.delete(0, "end")
        for e in entries:
            listbox.insert("end", e.get("date", ""))


    title_label = ctk.CTkLabel(right, text="Date")
    title_label.pack(anchor="w")
    date_var = ctk.CTkEntry(right)
    date_var.pack(fill="x", pady=(0, 6))

    content = ctk.CTkTextbox(right, wrap="word")
    content.pack(fill="both", expand=True)

    btn_frame = ctk.CTkFrame(right)
    btn_frame.pack(fill="x", pady=8)


    def on_select(evt=None):
        sel = listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        entry = entries[idx]
        date_var.delete(0, "end")
        date_var.insert(0, entry.get("date", ""))
        content.delete("0.0", "end")
        content.insert("0.0", entry.get("text", ""))


    def new_entry():
        date_var.delete(0, "end")
        date_var.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M"))
        content.delete("0.0", "end")
        listbox.selection_clear(0, "end")


    def save_entry():
        d = date_var.get().strip() or datetime.now().strftime("%Y-%m-%d %H:%M")
        t = content.get("0.0", "end").rstrip()
        sel = listbox.curselection()
        if sel:
            idx = sel[0]
            entries[idx]["date"] = d
            entries[idx]["text"] = t
        else:
            entries.append({"date": d, "text": t})
        _save_entries(entries)
        _refresh()


    def delete_entry():
        sel = listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        del entries[idx]
        _save_entries(entries)
        _refresh()
        new_entry()


    listbox.bind("<<ListboxSelect>>", on_select)

    ctk.CTkButton(btn_frame, text="New", command=new_entry).pack(side="left", padx=6)
    ctk.CTkButton(btn_frame, text="Save", command=save_entry).pack(side="left", padx=6)
    ctk.CTkButton(btn_frame, text="Delete", command=delete_entry).pack(side="left", padx=6)
    ctk.CTkButton(btn_frame, text="Close", command=win.destroy).pack(side="right", padx=6)

    _refresh()

    return win

