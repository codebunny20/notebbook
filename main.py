import customtkinter
import json
from gui import notesgui, tasksgui, journalgui, settingsgui

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.pin_state = False  # Initialize pin state
        self.title("Notebook")
        self.geometry("500x400")

        customtkinter.CTkLabel(self, text="Welcome to your notebook", font=("Arial", 20)).pack(pady=20)

        # Create a frame to hold main action buttons and arrange in a grid
        btn_frame = customtkinter.CTkFrame(self)
        btn_frame.pack(pady=10, padx=12, fill="x")

        notes_btn = customtkinter.CTkButton(
            btn_frame, text="Open Notes", command=lambda: notesgui.open_notes(self) # type: ignore
        )
        tasks_btn = customtkinter.CTkButton(
            btn_frame, text="Open Tasks", command=lambda: tasksgui.open_tasks(self) # type: ignore
        )
        settings_btn = customtkinter.CTkButton(
            btn_frame, text="Open Settings", command=lambda: settingsgui.open_settings(self) # type: ignore
        )
        journal_btn = customtkinter.CTkButton(
            btn_frame, text="Open Journal", command=lambda: journalgui.open_journal(self) # type: ignore
        )

        # Place buttons in a 2x2 grid for a cleaner layout
        notes_btn.grid(row=0, column=0, padx=8, pady=8, sticky="ew")
        tasks_btn.grid(row=0, column=1, padx=8, pady=8, sticky="ew")
        settings_btn.grid(row=1, column=0, padx=8, pady=8, sticky="ew")
        journal_btn.grid(row=1, column=1, padx=8, pady=8, sticky="ew")

        # Make columns expand evenly
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)

        # Bottom bar for auxiliary actions (Pin on the right)
        bottom_bar = customtkinter.CTkFrame(self)
        bottom_bar.pack(side="bottom", fill="x", padx=12, pady=12)

        customtkinter.CTkButton(
            bottom_bar,
            text="Pin Window",
            command=self.toggle_pin
        ).pack(side="right")

    def toggle_pin(self):
        self.pin_state = not self.pin_state
        self.attributes("-topmost", self.pin_state)

        if self.pin_state:
            self.title("Notebook - Pinned")
        else:
            self.title("Notebook")


    def open_window(self, title, message):
        win = customtkinter.CTkToplevel(self)  # child window
        win.title(title)
        win.geometry("500x400")
        customtkinter.CTkLabel(win, text=message, font=("Arial", 16)).pack(pady=30)
        customtkinter.CTkButton(win, text="Close", command=win.destroy).pack(pady=10)

    # notes window
    def open_notes_window(self):
        self.open_window("Notes", "This is the Notes window")

    # tasks window
    def open_tasks_window(self):
        self.open_window("Tasks", "This is the Tasks window")

    # journal window
    def open_journal_window(self):
        self.open_window("Journal", "This is the Journal window")

        # settings window and gui
    def open_settings_window(self):
        self.open_window("Settings", "This is the Settings window")

    
        

if __name__ == "__main__":
    app = App()
    app.mainloop()