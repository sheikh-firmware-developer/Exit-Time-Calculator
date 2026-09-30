import os
import json
import winreg

CONFIG_FILE = "config.json"

DEFAULT_SETTINGS = {
    "work_hours": "8.5",
    "intime_start": "08:30 AM",
    "intime_end": "10:00 AM",
    "strict_mode": True,
    "short_leave_enabled": False,
    "short_leave_hours": "2.0",
    "short_leave_position": "End",
    "theme": "System"
}

THEMES = {
    "Light": {
        "bg": "#ffffff", "surface": "#f8fafc", "border": "#e2e8f0",
        "text": "#0f172a", "muted": "#64748b", "accent": "#0ea5e9",
        "entry_bg": "#f1f5f9", "green": "#10b981", "red": "#ef4444"
    },
    "Dark": {
        "bg": "#0f172a", "surface": "#1e293b", "border": "#334155",
        "text": "#f8fafc", "muted": "#94a3b8", "accent": "#38bdf8",
        "entry_bg": "#1e293b", "green": "#34d399", "red": "#f87171"
    }
}

class SettingsModel:
    def __init__(self):
        self.settings = self.load_settings()

    def load_settings(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    return json.load(f)
            except Exception:
                return DEFAULT_SETTINGS.copy()
        return DEFAULT_SETTINGS.copy()

    def save_settings(self, new_settings):
        self.settings = new_settings
        try:
            with open(CONFIG_FILE, "w") as f:
                json.dump(self.settings, f, indent=4)
            return True
        except Exception:
            return False

    def get_windows_system_theme(self):
        try:
            registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
            key = winreg.OpenKey(registry, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            return "Light" if value == 1 else "Dark"
        except Exception:
            return "Dark"

    def get_active_palette(self):
        theme_choice = self.settings.get("theme", "System")
        if theme_choice == "System":
            theme_choice = self.get_windows_system_theme()
        return THEMES.get(theme_choice, THEMES["Dark"])
