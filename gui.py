import customtkinter as ctk
from services import fetch_weather

class WeatherAppGUI:
    def __init__(self):
        ctk.set_appearance_mode("System")
        self.root = ctk.CTk()
        self.root.geometry("320x240")
        self.root.title("Weather")

        self.label = ctk.CTkLabel(self.root, text="Loading weather...")
        self.label.pack(pady=20)

        self.refresh_button = ctk.CTkButton(self.root, text="Refresh", command=self.update_weather)
        self.refresh_button.pack(pady=10)

        self.update_weather()

    def update_weather(self):
        weather_text = fetch_weather()
        self.label.configure(text=weather_text)

    def run(self):
        self.root.mainloop()