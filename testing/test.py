import customtkinter

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Notebook")
        self.geometry("500x400")

        customtkinter.CTkLabel(
            self, text="Welcome to your notebook", font=("Arial", 20)
        ).pack(pady=20)

        # Each button opens a different window
        customtkinter.CTkButton(
            self, text="Open Notes", command=lambda: self.open_window("Notes", "This is the Notes window")
        ).pack(pady=8)

        customtkinter.CTkButton(
            self, text="Open Tasks", command=lambda: self.open_window("Tasks", "This is the Tasks window")
        ).pack(pady=8)

        customtkinter.CTkButton(
            self, text="Open Settings", command=lambda: self.open_window("Settings", "This is the Settings window")
        ).pack(pady=8)

    def open_window(self, title, message):
        win = customtkinter.CTkToplevel(self)  # child window
        win.title(title)
        win.geometry("320x200")
        customtkinter.CTkLabel(win, text=message, font=("Arial", 16)).pack(pady=30)
        customtkinter.CTkButton(win, text="Close", command=win.destroy).pack(pady=10)


if __name__ == "__main__":
    app = App()
    app.mainloop()