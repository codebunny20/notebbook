import customtkinter as ctk
import tkinter as tk
import os
import json


def _data_path():
    root = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(root, "data", "notes.json")


def _ensure_data():
    path = _data_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump([], f)


def _load_notes():
    path = _data_path()
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def _save_notes(notes):
    path = _data_path()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(notes, f, indent=2)


def open_notes(parent):
    _ensure_data()
    notes = _load_notes()

    win = ctk.CTkToplevel(parent)
    win.title("Notes")
    win.geometry("800x500")

    left = ctk.CTkFrame(win)
    left.pack(side="left", fill="y", padx=8, pady=8)

    right = ctk.CTkFrame(win)
    right.pack(side="right", fill="both", expand=True, padx=8, pady=8)

    tk.Label(left, text="Notes").pack()
    listbox = tk.Listbox(left, width=30)
    listbox.pack(fill="y", expand=True)

    for n in notes:
        listbox.insert("end", n.get("title", "Untitled"))

    title_entry = ctk.CTkEntry(right)
    title_entry.pack(fill="x", pady=(0, 6))

    content = ctk.CTkTextbox(right, wrap="word")
    content.pack(fill="both", expand=True)

    btn_frame = ctk.CTkFrame(right)
    btn_frame.pack(fill="x", pady=8)


    def on_select(evt=None):
        sel = listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        note = notes[idx]
        title_entry.delete(0, "end")
        title_entry.insert(0, note.get("title", ""))
        content.delete("0.0", "end")
        content.insert("0.0", note.get("content", ""))


    def new_note():
        title_entry.delete(0, "end")
        content.delete("0.0", "end")
        listbox.selection_clear(0, "end")


    def save_note():
        t = title_entry.get().strip() or "Untitled"
        c = content.get("0.0", "end").rstrip()
        sel = listbox.curselection()
        if sel:
            idx = sel[0]
            notes[idx]["title"] = t
            notes[idx]["content"] = c
            listbox.delete(idx)
            listbox.insert(idx, t)
            listbox.selection_set(idx)
        else:
            notes.append({"title": t, "content": c})
            listbox.insert("end", t)
            listbox.selection_clear(0, "end")

        _save_notes(notes)


    def delete_note():
        sel = listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        del notes[idx]
        listbox.delete(idx)
        _save_notes(notes)
        new_note()


    listbox.bind("<<ListboxSelect>>", on_select)

    ctk.CTkButton(btn_frame, text="New", command=new_note).pack(side="left", padx=6)
    ctk.CTkButton(btn_frame, text="Save", command=save_note).pack(side="left", padx=6)
    ctk.CTkButton(btn_frame, text="Delete", command=delete_note).pack(side="left", padx=6)
    ctk.CTkButton(btn_frame, text="Close", command=win.destroy).pack(side="right", padx=6)

    return win

