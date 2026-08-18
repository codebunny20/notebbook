import customtkinter as ctk
import tkinter as tk
import os
import json


def _data_path():
    root = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(root, "data", "tasks.json")


def _ensure_data():
    path = _data_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump([], f)


def _load_tasks():
    path = _data_path()
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def _save_tasks(tasks):
    path = _data_path()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)


def open_tasks(parent):
    _ensure_data()
    tasks = _load_tasks()

    win = ctk.CTkToplevel(parent)
    win.title("Tasks")
    win.geometry("700x450")

    left = ctk.CTkFrame(win)
    left.pack(side="left", fill="y", padx=8, pady=8)

    right = ctk.CTkFrame(win)
    right.pack(side="right", fill="both", expand=True, padx=8, pady=8)

    tk.Label(left, text="Tasks").pack()
    listbox = tk.Listbox(left, width=40)
    listbox.pack(fill="y", expand=True)

    def _display_tasks():
        listbox.delete(0, "end")
        for t in tasks:
            prefix = "[x] " if t.get("done") else "[ ] "
            listbox.insert("end", prefix + t.get("title", "Untitled"))


    title_entry = ctk.CTkEntry(right)
    title_entry.pack(fill="x", pady=(0, 6))

    done_var = tk.BooleanVar()
    done_check = ctk.CTkCheckBox(right, text="Completed", variable=done_var)
    done_check.pack(anchor="w", pady=(0, 6))

    btn_frame = ctk.CTkFrame(right)
    btn_frame.pack(fill="x", pady=8)


    def on_select(evt=None):
        sel = listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        task = tasks[idx]
        title_entry.delete(0, "end")
        title_entry.insert(0, task.get("title", ""))
        done_var.set(bool(task.get("done", False)))


    def new_task():
        title_entry.delete(0, "end")
        done_var.set(False)
        listbox.selection_clear(0, "end")


    def save_task():
        t = title_entry.get().strip() or "Untitled"
        d = bool(done_var.get())
        sel = listbox.curselection()
        if sel:
            idx = sel[0]
            tasks[idx]["title"] = t
            tasks[idx]["done"] = d
        else:
            tasks.append({"title": t, "done": d})
        _save_tasks(tasks)
        _display_tasks()


    def delete_task():
        sel = listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        del tasks[idx]
        _save_tasks(tasks)
        _display_tasks()
        new_task()


    def toggle_done():
        sel = listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        tasks[idx]["done"] = not bool(tasks[idx].get("done", False))
        _save_tasks(tasks)
        _display_tasks()
        listbox.selection_set(idx)


    listbox.bind("<<ListboxSelect>>", on_select)

    ctk.CTkButton(btn_frame, text="New", command=new_task).pack(side="left", padx=6)
    ctk.CTkButton(btn_frame, text="Save", command=save_task).pack(side="left", padx=6)
    ctk.CTkButton(btn_frame, text="Delete", command=delete_task).pack(side="left", padx=6)
    ctk.CTkButton(btn_frame, text="Toggle Done", command=toggle_done).pack(side="left", padx=6)
    ctk.CTkButton(btn_frame, text="Close", command=win.destroy).pack(side="right", padx=6)

    _display_tasks()

    return win

