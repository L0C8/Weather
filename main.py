from utils import check_runtime_environment
from gui import WeatherAppGUI

if __name__ == "__main__":
    check_runtime_environment()
    app = WeatherAppGUI()
    app.mainloop()
    print(f"Using API key: {api_key}")