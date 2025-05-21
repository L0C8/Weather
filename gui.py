import customtkinter as ctk
from utils import ensure_theme_file, get_saved_theme
import configparser

THEME_FILE_PATH = "data/themes.ini"

class WeatherAppGUI:
    def __init__(self):
        ensure_theme_file()
        self.theme_name = get_saved_theme()
        self.theme = self.load_theme(self.theme_name)

        ctk.set_appearance_mode("System")
        self.root = ctk.CTk()
        self.root.geometry("320x240")
        self.root.title("Theme Test")

        self.frame = ctk.CTkFrame(self.root, fg_color=self.theme.get("bg", "#222222"))
        self.frame.pack(fill="both", expand=True)

        self.label = ctk.CTkLabel(
            self.frame,
            text=f"Loaded Theme: {self.theme_name}",
            text_color=self.theme.get("fg", "#ffffff")
        )
        self.label.pack(pady=100)

    def load_theme(self, theme_name):
        config = configparser.ConfigParser()
        config.read(THEME_FILE_PATH)
        if theme_name in config:
            return dict(config[theme_name])
        return {}

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = WeatherAppGUI()
    app.run()
