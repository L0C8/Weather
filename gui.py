import tkinter as tk
from tkinter import ttk
from services import fetch_weather, get_timezone_and_time

class WeatherAppGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Weather App")
        self.geometry("300x200")
        self.configure(bg="#ffffff")

        self.label = tk.Label(self, text="Weather Info:", bg="#ffffff", fg="#000000")
        self.label.pack(pady=10)

        self.result_label = tk.Label(self, text="", bg="#ffffff", fg="#000000", wraplength=280, justify="left")
        self.result_label.pack(pady=10)

        self.fetch_button = ttk.Button(self, text="Fetch Weather", command=self.call_fetch_weather)
        self.fetch_button.pack(pady=10)

    def call_fetch_weather(self):
        result = fetch_weather()
        get_timezone_and_time()
        self.result_label.config(text=result)
