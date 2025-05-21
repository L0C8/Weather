import customtkinter as ctk
import random
import tkinter as tk
from datetime import datetime

class WeatherAppGUI:
    def __init__(self):
        ctk.set_appearance_mode("System")
        self.root = ctk.CTk()
        self.root.geometry("320x240")
        self.root.title("Weather")

        # Create a top Canvas block for the weather gradient
        self.weather_canvas = tk.Canvas(self.root, width=320, height=80, highlightthickness=0)
        self.weather_canvas.pack(fill="x")

        # Below weather gradient, place a normal frame for the rest of the GUI
        self.body_frame = ctk.CTkFrame(self.root, fg_color="white")
        self.body_frame.pack(fill="both", expand=True)

        self.label = ctk.CTkLabel(self.body_frame, text="Loading weather...", text_color="black")
        self.label.pack(pady=10)

        self.refresh_button = ctk.CTkButton(self.body_frame, text="Randomize Weather", command=self.update_weather)
        self.refresh_button.pack(pady=10)

        self.update_weather()

    def get_gradient_colors(self, weather_condition: str, hour: int | None = None) -> tuple[str, str]:
        if hour is None:
            hour = datetime.now().hour

        weather_condition = weather_condition.lower()

        if "snow" in weather_condition:
            return ("#ffffff", "#add8e6")  # white to light blue
        elif "rain" in weather_condition or "drizzle" in weather_condition:
            return ("#808080", "#1e90ff")  # grey to blue
        elif 6 <= hour < 15:
            return ("#87ceeb", "#ffffff")  # blue to white
        elif 15 <= hour < 19:
            return ("#f3904f", "#3b4371")  # Sunset look
        else:
            return ("#808080", "#000000")  # grey to black

    def draw_gradient(self, canvas, start_color, end_color):
        steps = 80
        for i in range(steps):
            r1, g1, b1 = canvas.winfo_rgb(start_color)
            r2, g2, b2 = canvas.winfo_rgb(end_color)
            r = int(r1 + (r2 - r1) * i / steps) >> 8
            g = int(g1 + (g2 - g1) * i / steps) >> 8
            b = int(b1 + (b2 - b1) * i / steps) >> 8
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            canvas.create_rectangle(0, i, 320, i + 1, outline="", fill=hex_color)

    def update_weather(self):
        test_conditions = [
            ("sunny", 8),      # Morning
            ("sunny", 16),     # Late Afternoon
            ("sunny", 21),     # Night
            ("rain", 10),      # Rainy Day
            ("snow", 11)       # Snowy Day
        ]
        condition, hour = random.choice(test_conditions)
        self.label.configure(text=f"Condition: {condition}, Hour: {hour}:00")

        gradient_start, gradient_end = self.get_gradient_colors(condition, hour)

        self.weather_canvas.delete("all")
        self.draw_gradient(self.weather_canvas, gradient_start, gradient_end)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = WeatherAppGUI()
    app.run()
