import os
import configparser

THEME_FILE_PATH = "data/themes.ini"
SETTINGS_FILE_PATH = "data/settings.ini"

def check_runtime_environment():
    ensure_theme_file()
    ensure_settings_file()

def ensure_settings_file():
    if not os.path.exists(SETTINGS_FILE_PATH):
        config = configparser.ConfigParser()
        config["User"] = {"theme": "Dark"}
        with open(SETTINGS_FILE_PATH, "w") as configfile:
            config.write(configfile)

def ensure_theme_file():
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(THEME_FILE_PATH):
        with open(THEME_FILE_PATH, "w") as f:
            f.write("""[Dark]
bg = #1e1e1e
fg = #e0e0e0
accent = #61dafb
button_bg = #333333
button_fg = #ffffff
headline = #dddddd

[Light]
bg = #ffffff
fg = #000000
accent = #007acc
button_bg = #f0f0f0
button_fg = #000000
headline = #222222

[CyberGreen]
bg = #0d0f0d
fg = #00ff9c
accent = #33ffcc
button_bg = #1e1e1e
button_fg = #00ff9c
headline = #00ffaa

[MidnightPurple]
bg = #1a1b41
fg = #e0e0f8
accent = #c084f5
button_bg = #292b5e
button_fg = #ffffff
headline = #e2c6ff

[SoftSunrise]
bg = #fff3e0
fg = #4e342e
accent = #ff8a65
button_bg = #ffe0b2
button_fg = #4e342e
headline = #bf360c
""")

def get_saved_theme():
    if not os.path.exists(SETTINGS_FILE_PATH):
        return "Dark" 
    config = configparser.ConfigParser()
    config.read(SETTINGS_FILE_PATH)
    return config.get("User", "theme", fallback="Dark")

def get_theme_data(theme_name):
    config = configparser.ConfigParser()
    config.read(THEME_FILE_PATH)
    if theme_name in config:
        return dict(config[theme_name])
    return {}