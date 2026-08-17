import customtkinter

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("notebook")
        self.geometry("500x400")

        # Create a label
        self.label = customtkinter.CTkLabel(self, text="welcome to your note book", font=("Arial", 20))
        self.label.pack(pady=20)

        # Create a button
        self.button = customtkinter.CTkButton(self, text="Click Me", command=self.on_button_click)
        self.button.pack(pady=10)

        self.entry = customtkinter.CTkButton(self, text="Click Me", command=self.on_button_click)
        self.entry.pack(pady=10)

        self.entry = customtkinter.CTkButton(self, text="Click Me", command=self.on_button_click)
        self.entry.pack(pady=10)

        self.entry = customtkinter.CTkButton(self, text="Click Me", command=self.on_button_click)
        self.entry.pack(pady=10)

        self.entry = customtkinter.CTkButton(self, text="Click Me", command=self.on_button_click)
        self.entry.pack(pady=10)


    def on_button_click(self):
        self.label.configure(text="Button Clicked!")
        print("Button was clicked!")

if __name__ == "__main__":
    app = App()
    app.mainloop()