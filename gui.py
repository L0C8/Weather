import customtkinter as ctk
from utils import get_theme_data, get_saved_theme

class WeatherAppGUI:
    def __init__(self, theme_name="Dark"):
        self.theme_name = get_saved_theme()
        self.theme = get_theme_data(self.theme_name)

        ctk.set_appearance_mode("System")
        self.root = ctk.CTk()
        self.root.geometry("320x240")
        self.root.title("Theme Test")

        self.frame = ctk.CTkFrame(self.root, fg_color=self.theme.get("bg", "#ffffff"), corner_radius=0)
        self.frame.pack(fill="both", expand=True)

        self.label = ctk.CTkLabel(
            self.frame,
            text=f"Loaded Theme: {self.theme_name}",
            text_color=self.theme.get("fg", "#000000"),
            corner_radius=0
        )
        self.label.pack(pady=100)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = WeatherAppGUI()  
    app.run()